#!/usr/bin/env node
/**
 * drift-check.js
 * PostToolUse Hook — 局部死循环检测（Stuck Detection Only）
 *
 * 注册方式（.claude/settings.json PostToolUse）：
 *   { "matcher": "Edit|Write|MultiEdit|Bash", "hooks": [{ "type": "command", "command": "node .claude/hooks/drift-check.js", "timeout": 10 }] }
 *
 * 事件字段：tool_name / tool_input / tool_response（与仓库其他 Hook 一致）
 * 状态文件：~/.claude/drift-state-<project_hash>.json（按项目隔离）
 *
 * 方向漂移检测已移至 direction-reviewer skill（工件驱动，阶段门禁触发）。
 * 本 Hook 只负责机械检测 stuck 信号（重复错误 + 同文件反复编辑）。
 */

const fs   = require("fs");
const path = require("path");
const crypto = require("crypto");

// ── 配置（可按项目调整）────────────────────────────────
const CFG = {
  HOT_FILE_EDITS      : 5,    // 同一文件编辑次数触发 stuck
  REPEAT_ERROR_COUNT  : 3,    // 同一错误重复次数触发 stuck
  CB_COOLDOWN_CALLS   : 10,   // 断路后需要经过 N 次工具调用才进入 HALF_OPEN
  CB_STABLE_CALLS     : 2,    // HALF_OPEN 后需要连续 N 次无问题才恢复 CLOSED
};

// ── Reset 接口（P3 联动：direction-reviewer PASS 后可调用）──────────
// 用法：node drift-check.js --reset
// 删除状态文件，重置所有计数器
if (process.argv.includes("--reset")) {
  const HOME_DIR = process.env.USERPROFILE || process.env.HOME || "~";
  const PROJECT_DIR = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  const PROJECT_HASH = crypto.createHash("sha256").update(PROJECT_DIR).digest("hex").slice(0, 8);
  const STATE_FILE = path.join(HOME_DIR, ".claude", `drift-state-${PROJECT_HASH}.json`);
  try { fs.unlinkSync(STATE_FILE); } catch {}
  process.stdout.write(JSON.stringify({ type: "message", content: "drift-check reset: 状态已清除" }));
  process.exit(0);
}

// 按项目隔离状态文件，避免跨项目累计
const HOME_DIR = process.env.USERPROFILE || process.env.HOME || "~";
const PROJECT_DIR = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const PROJECT_HASH = crypto.createHash("sha256").update(PROJECT_DIR).digest("hex").slice(0, 8);
const STATE_FILE = path.join(HOME_DIR, ".claude", `drift-state-${PROJECT_HASH}.json`);

// 只对执行类 Bash 命令做错误检测，忽略 git status / git diff 等只读命令
const BASH_SKIP_PATTERNS = [
  /^git\s+(status|diff|log|branch|fetch|show|tag)/i,
  /^ls\b/i,
  /^cat\b/i,
  /^echo\b/i,
  /^which\b/i,
  /^node\s+--version/i,
  /^python\s+--version/i,
];

function isSkippableBash(command) {
  if (!command) return false;
  const cmd = command.trim();
  return BASH_SKIP_PATTERNS.some(p => p.test(cmd));
}

// ── 两阶段错误过滤：排除假阳性 ────────────────────────
const ERROR_EXCLUDE_PATTERNS = [
  /error[_-]?handling/i,
  /error[_-]?message/i,
  /on[_-]?error/i,
  /"error"\s*:/i,
  /\berrors?\s*=\s*\[\]/i,
  /no\s+errors?\s+found/i,
  /0\s+errors?/i,
  /error.*\.md/i,
];
const ERROR_MATCH_PATTERNS = [
  /(?:TypeError|SyntaxError|ReferenceError|ImportError|ModuleNotFoundError)[\s:]/i,
  /(?:Error|Exception|Traceback).*line\s+\d+/i,
  /FAILED\s+[\w/]+\.py/i,
  /AssertionError/i,
  /\bfailed\b.*\berror\b/i,
  /exit\s+code\s+[1-9]/i,
  /npm\s+ERR!/i,
  /\bCRITICAL\b|\bFATAL\b/i,
];

function extractRealError(text) {
  for (const pat of ERROR_EXCLUDE_PATTERNS) {
    if (pat.test(text)) return null;
  }
  for (const pat of ERROR_MATCH_PATTERNS) {
    const m = text.match(pat);
    if (m) return m[0].trim().slice(0, 60);
  }
  return null;
}

// ── 三状态 Circuit Breaker ────────────────────────────
function updateCircuitBreaker(state, hasNewIssue) {
  const cb = state.cb || { status: "CLOSED", openedAt: 0, stableCount: 0 };

  if (cb.status === "CLOSED") {
    if (hasNewIssue) {
      cb.status    = "OPEN";
      cb.openedAt  = state.toolCallCount;
      cb.stableCount = 0;
      state.recentErrors   = {};
      state.fileEditCounts = {};
    }
  } else if (cb.status === "OPEN") {
    const elapsed = state.toolCallCount - cb.openedAt;
    if (elapsed >= CFG.CB_COOLDOWN_CALLS) {
      cb.status = "HALF_OPEN";
      cb.stableCount = 0;
    }
  } else if (cb.status === "HALF_OPEN") {
    if (hasNewIssue) {
      cb.status    = "OPEN";
      cb.openedAt  = state.toolCallCount;
      cb.stableCount = 0;
    } else {
      cb.stableCount += 1;
      if (cb.stableCount >= CFG.CB_STABLE_CALLS) {
        cb.status = "CLOSED";
        cb.stableCount = 0;
      }
    }
  }

  state.cb = cb;
  return cb;
}

// ── 读写状态 ──────────────────────────────────────────
function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, "utf8")); }
  catch {
    return {
      toolCallCount: 0, modifiedFiles: [],
      fileEditCounts: {}, recentErrors: {},
      cb: { status: "CLOSED", openedAt: 0, stableCount: 0 }
    };
  }
}
function saveState(s) {
  fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(s, null, 2));
}

// ── 主逻辑 ────────────────────────────────────────────
function main() {
  let raw = "";
  process.stdin.on("data", c => (raw += c));
  process.stdin.on("end", () => {
    let event = {};
    try { event = JSON.parse(raw); } catch {}

    // 兼容两种 payload 格式（tool_name / tool_input / tool_response）
    const toolName  = event.tool_name  || event.tool  || "";
    const toolInput = event.tool_input || event.params || {};
    const toolResponse = event.tool_response || event.output || "";

    const state = loadState();
    state.toolCallCount  = (state.toolCallCount || 0) + 1;
    state.fileEditCounts = state.fileEditCounts || {};
    state.recentErrors   = state.recentErrors   || {};

    // 追踪文件编辑（Edit / Write / MultiEdit）
    if (["Write", "Edit", "MultiEdit"].includes(toolName)) {
      const input = (typeof toolInput === "string") ? JSON.parse(toolInput || "{}") : toolInput;
      const f = input.path || input.file_path || "";
      if (f) {
        state.fileEditCounts[f] = (state.fileEditCounts[f] || 0) + 1;
        if (!state.modifiedFiles) state.modifiedFiles = [];
        if (!state.modifiedFiles.includes(f)) state.modifiedFiles.push(f);
      }
    }

    // 两阶段过滤提取真实错误（仅执行类 Bash 命令）
    if (toolName === "Bash") {
      const input = (typeof toolInput === "string") ? JSON.parse(toolInput || "{}") : toolInput;
      const command = input.command || "";
      if (!isSkippableBash(command)) {
        const responseText = (typeof toolResponse === "string")
          ? toolResponse
          : JSON.stringify(toolResponse || "");
        const err = extractRealError(responseText);
        if (err) state.recentErrors[err] = (state.recentErrors[err] || 0) + 1;
      }
    }

    // 判断 stuck
    const stuckReasons = [];
    const hotFiles = Object.entries(state.fileEditCounts)
      .filter(([, n]) => n >= CFG.HOT_FILE_EDITS)
      .map(([f, n]) => `${path.basename(f)}(×${n})`);
    if (hotFiles.length) stuckReasons.push(`同一文件反复编辑：${hotFiles.join(", ")}`);

    const hotErrors = Object.entries(state.recentErrors)
      .filter(([, n]) => n >= CFG.REPEAT_ERROR_COUNT)
      .map(([e, n]) => `"${e}"(×${n})`);
    if (hotErrors.length) stuckReasons.push(`重复错误未解决：${hotErrors.join(", ")}`);

    // Circuit Breaker：只由 stuck 驱动
    const cbHasIssue = stuckReasons.length > 0;
    const prevStatus = (state.cb || {}).status || "CLOSED";
    const cb = updateCircuitBreaker(state, cbHasIssue);
    saveState(state);

    // CLOSED → 正常输出告警（含首次从 CLOSED→OPEN 的转换）
    if (prevStatus === "CLOSED") {
      if (stuckReasons.length > 0) {
        process.stdout.write(JSON.stringify({
          type: "message",
          content: [
            `🔴 stuck-check（${stuckReasons.join(" / ")}）`,
            `请停止当前方向：① 用一句话说清卡点`,
            `② 判断根因在哪一层（架构/接口/数据/假设）`,
            `③ 给用户 2-3 个跳出方案，等确认后再继续`,
          ].join("\n"),
          suggested_action: "trigger_direction_review",
          _comment: "P3 联动：提示 CC 手动调用 direction-reviewer skill（Hook 无法直接调 skill）",
        }));
      }
      return;
    }

    // OPEN：静默等待，不输出（防止告警风暴）
    if (cb.status === "OPEN") return;
    // HALF_OPEN：只报 stuck
    if (cb.status === "HALF_OPEN" && stuckReasons.length === 0) return;

    if (stuckReasons.length > 0) {
      process.stdout.write(JSON.stringify({
        type: "message",
        content: [
          `🔴 stuck-check（${stuckReasons.join(" / ")}）`,
          `请停止当前方向：① 用一句话说清卡点`,
          `② 判断根因在哪一层（架构/接口/数据/假设）`,
          `③ 给用户 2-3 个跳出方案，等确认后再继续`,
          `⚠️ 仍在 HALF_OPEN 观察期，请谨慎继续`,
        ].join("\n"),
      }));
    }
  });
}

main();
