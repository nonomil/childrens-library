/**
 * PreToolUse Hook: 两层防御删除安全守卫 v2
 *
 * Layer 1: 阻断（默认）— 检测到删除命令 → RC=2 阻断，无文件操作
 * Layer 2: 移动兜底 — 用户确认后（.delete-approved），先移动文件再放行
 *
 * 日志: .claude/logs/delete_safety.log (JSON Lines)
 * 备份: E:/Temp/CC_Deleted/YYYY-MM-DD_HHMMSS/（保留相对路径 + manifest.json）
 * 返回码: 0=放行, 2=阻断
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const BACKUP_ROOT = "E:/Temp/CC_Deleted";
const LOG_FILE = ".claude/logs/delete_safety.log";
const APPROVED_FILE = ".claude/state/.delete-approved";

// ── 日志 ──────────────────────────────────────────────────

function log(entry) {
  try {
    const projectDir = (
      process.env.CLAUDE_PROJECT_DIR || process.cwd()
    ).replace(/\\/g, "/");
    const logDir = path.join(projectDir, ".claude", "logs");
    const logPath = path.join(logDir, "delete_safety.log");
    fs.mkdirSync(logDir, { recursive: true });
    const line = JSON.stringify({
      timestamp: new Date().toISOString(),
      ...entry,
    }) + "\n";
    fs.appendFileSync(logPath, line, "utf-8");
  } catch {}
}

// ── 命令解析 ──────────────────────────────────────────────

/**
 * 将原始命令字符串拆分为顶层段落。
 * 按 && / || / ; / | 分割，只分析每个段落的命令部分。
 */
function splitSegments(cmd) {
  // 先去引号内容（用占位符保护）
  const placeholders = [];
  const protected_ = cmd.replace(/"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'/g, (m) => {
    placeholders.push(m);
    return `__PH${placeholders.length - 1}__`;
  });

  // 去注释
  const noComment = protected_.replace(/#.*$/gm, "");

  // 按控制操作符分割
  const raw = noComment.split(/\s*(?:&&|\|\||[;|])\s*/);
  return raw.map((seg) =>
    seg.replace(/__PH(\d+)__/g, (_, i) => placeholders[parseInt(i)])
  );
}

/**
 * 从一个段落中提取命令词（第一个非环境变量的词）。
 */
function getCommandWord(segment) {
  const trimmed = segment.trim();
  if (!trimmed) return null;

  // 跳过环境变量赋值 (VAR=value cmd ...)
  const words = [];
  let cur = "", q = null;
  for (const ch of trimmed) {
    if (q) {
      if (ch === q) q = null;
      cur += ch;
    } else if (ch === '"' || ch === "'") {
      q = ch;
      cur += ch;
    } else if (ch === " " || ch === "\t") {
      if (cur) { words.push(cur); cur = ""; }
    } else {
      cur += ch;
    }
  }
  if (cur) words.push(cur);

  // 跳过 VAR=value 模式
  for (const w of words) {
    if (/^[A-Za-z_][A-Za-z0-9_]*=/.test(w)) continue;
    // 去掉路径前缀，只取命令名
    return w.includes("/") ? w.split("/").pop() : w;
  }
  return null;
}

/**
 * 解析命令：返回 { cmd, subcmd, flags, targets } 或 null
 */
function parseSegment(segment) {
  const cmdWord = getCommandWord(segment);
  if (!cmdWord) return null;

  const lower = cmdWord.toLowerCase();

  // rm / rmdir
  if (lower === "rm" || lower === "rmdir") {
    return parseRmSegment(segment, cmdWord);
  }

  // git 子命令
  if (lower === "git") {
    return parseGitSegment(segment);
  }

  // Windows: del / rd — 只检测，不做文件操作
  if (lower === "del" || lower === "rd") {
    return { cmd: lower, subcmd: null, flags: [], targets: [], raw: segment };
  }

  return null;
}

function parseRmSegment(segment, cmdWord) {
  const args = splitArgsPreservingQuotes(segment);
  const flags = [], targets = [];
  let started = false, pastDoubleDash = false;
  for (const a of args) {
    if (!started) {
      if (a === cmdWord || a.endsWith("/" + cmdWord)) started = true;
      continue;
    }
    if (!pastDoubleDash && a === "--") { pastDoubleDash = true; continue; }
    if (!pastDoubleDash && /^-[rRfivdPW]+$/.test(a)) { flags.push(a); continue; }
    targets.push(a);
  }
  return { cmd: cmdWord, subcmd: null, flags, targets, raw: segment };
}

function parseGitSegment(segment) {
  const args = splitArgsPreservingQuotes(segment);
  let foundGit = false, subcmd = null;
  const flags = [], targets = [];
  for (const a of args) {
    if (!foundGit) {
      if (a === "git" || a.endsWith("/git")) foundGit = true;
      continue;
    }
    if (!subcmd) {
      subcmd = a;
      continue;
    }
    if (a.startsWith("-")) { flags.push(a); continue; }
    if (a === "--") continue;
    targets.push(a);
  }
  return { cmd: "git", subcmd, flags, targets, raw: segment };
}

function splitArgsPreservingQuotes(str) {
  const args = [];
  let cur = "", q = null;
  for (const ch of str) {
    if (q) {
      if (ch === q) q = null;
      cur += ch;
    } else if (ch === '"' || ch === "'") {
      q = ch;
    } else if (ch === " " || ch === "\t" || ch === "\n") {
      if (cur) { args.push(cur); cur = ""; }
    } else {
      cur += ch;
    }
  }
  if (cur) args.push(cur);
  return args;
}

// ── 检测逻辑 ──────────────────────────────────────────────

/**
 * 检测结果: { type: 'allow'|'block'|'move', reason, parsed }
 */
function detectDeletion(cmd) {
  if (!cmd || !cmd.trim()) return { type: "allow", reason: "empty", parsed: null };

  const segments = splitSegments(cmd);
  for (const seg of segments) {
    const parsed = parseSegment(seg);
    if (!parsed) continue;

    // ── rm / rmdir ──
    if (parsed.cmd === "rm" || parsed.cmd === "rmdir") {
      // 安全 flag 放行（可能在 flags 或 targets 中）
      const allArgs = [...parsed.flags, ...parsed.targets];
      if (allArgs.some((a) => /^--(help|version)$/.test(a))) {
        continue; // 不是真正的删除
      }
      return { type: "block", reason: `${parsed.cmd} command`, parsed };
    }

    // ── git clean ──
    if (parsed.cmd === "git" && parsed.subcmd === "clean") {
      // dry-run 放行
      if (parsed.flags.some((f) => /^-(n|-dry-run)$/.test(f))) {
        continue;
      }
      return { type: "block", reason: "git clean", parsed };
    }

    // ── git rm ──
    if (parsed.cmd === "git" && parsed.subcmd === "rm") {
      // --cached 放行（只改索引，不删工作区文件）
      if (parsed.flags.includes("--cached")) continue;
      // dry-run 放行
      if (parsed.flags.some((f) => /^-(n|-dry-run)$/.test(f))) continue;
      return { type: "block", reason: "git rm", parsed };
    }

    // ── del / rd（Windows）─ 标记为 block 但不做文件操作 ──
    if (parsed.cmd === "del" || parsed.cmd === "rd") {
      return { type: "block", reason: `${parsed.cmd} (Windows)`, parsed };
    }
  }

  return { type: "allow", reason: "no_deletion_detected", parsed: null };
}

// ── Layer 2: 文件移动 ─────────────────────────────────────

function resolveP(target, cwd) {
  if (path.isAbsolute(target)) return path.resolve(target);
  return path.resolve(cwd || ".", target);
}

function timestamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}_${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

function moveWithStructure(files, cwd, backupDir) {
  const manifest = [];
  const moved = [], errors = [];
  const projectDir = (process.env.CLAUDE_PROJECT_DIR || process.cwd()).replace(/\\/g, "/");

  for (const f of files) {
    if (!fs.existsSync(f)) {
      errors.push(`[skip] not found: ${f}`);
      continue;
    }
    // 保留相对路径结构
    const rel = path.relative(projectDir, f) || path.basename(f);
    const dst = path.join(backupDir, rel);
    const dstDir = path.dirname(dst);
    try {
      fs.mkdirSync(dstDir, { recursive: true });
      // 同名冲突处理
      let finalDst = dst;
      if (fs.existsSync(dst)) {
        const ext = path.extname(dst);
        const stem = path.basename(dst, ext);
        finalDst = path.join(dstDir, `${stem}_${Date.now()}${ext}`);
      }
      fs.renameSync(f, finalDst);
      moved.push(f);
      manifest.push({ original: f, backup: finalDst, relative: rel });
    } catch (e) {
      errors.push(`[fail] ${f}: ${e.message}`);
    }
  }

  // 写 manifest.json
  if (manifest.length > 0) {
    try {
      fs.writeFileSync(
        path.join(backupDir, "manifest.json"),
        JSON.stringify({
          timestamp: new Date().toISOString(),
          projectDir,
          cwd,
          command: "",
          files: manifest,
        }, null, 2),
        "utf-8"
      );
    } catch {}
  }

  return { moved, errors, manifest };
}

function expandGlob(pattern, cwd) {
  const dir = path.dirname(pattern);
  const base = path.basename(pattern);
  const absDir = resolveP(dir, cwd);
  if (!fs.existsSync(absDir)) return [];
  const re = new RegExp(
    "^" + base.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*").replace(/\?/g, ".") + "$"
  );
  try {
    return fs.readdirSync(absDir).filter((f) => re.test(f)).map((f) => path.join(absDir, f));
  } catch { return []; }
}

function collectTargetFiles(parsed, cwd) {
  const files = [];
  if (parsed.cmd === "git" && parsed.subcmd === "clean") {
    // 枚举 untracked 文件
    try {
      const out = execSync("git ls-files --others --exclude-standard", {
        cwd, encoding: "utf-8", stdio: ["pipe", "pipe", "pipe"],
      });
      for (const line of out.split("\n")) {
        const rel = line.trim();
        if (rel) {
          const full = resolveP(rel, cwd);
          if (fs.existsSync(full)) files.push(full);
        }
      }
    } catch {}
    return files;
  }

  for (const t of parsed.targets) {
    if (/[*?]/.test(t)) {
      files.push(...expandGlob(t, cwd));
    } else {
      files.push(resolveP(t, cwd));
    }
  }
  return files;
}

// ── .delete-approved 检查 ─────────────────────────────────

function checkApproved(cmd, cwd) {
  const projectDir = (process.env.CLAUDE_PROJECT_DIR || process.cwd()).replace(/\\/g, "/");
  const approvedPath = path.join(projectDir, APPROVED_FILE);
  if (!fs.existsSync(approvedPath)) return false;
  try {
    const data = JSON.parse(fs.readFileSync(approvedPath, "utf-8"));
    // 简单匹配：approved command 是当前命令的子串，或匹配命令关键词
    const approvedCmd = (data.command || "").trim();
    if (!approvedCmd) return false;
    // 检查过期（5分钟）
    const approvedAt = new Date(data.approved_at);
    if (Date.now() - approvedAt.getTime() > 5 * 60 * 1000) return false;
    // 检查命令匹配
    return cmd.includes(approvedCmd) || approvedCmd.includes(cmd.trim());
  } catch { return false; }
}

// ── 主逻辑 ────────────────────────────────────────────────

function main() {
  let input;
  try { input = loadPayload(); } catch { input = {}; }

  const ti = input.tool_input || input;
  const cmd = ti.command || "";
  const cwd = ti.cwd || process.cwd();

  // 检测
  const result = detectDeletion(cmd);

  if (result.type === "allow") {
    process.exit(0);
  }

  // ── Layer 1: 阻断 ──────────────────────────────────
  const isApproved = checkApproved(cmd, cwd);

  if (!isApproved) {
    const msg =
      `[delete_safety_guard] BLOCKED: ${result.reason}\n` +
      `  Command: ${cmd}\n` +
      `  To proceed: say "confirm delete" to authorize this command.\n` +
      `  This block was logged for security review.\n`;

    log({ action: "blocked", reason: result.reason, command: cmd, cwd });
    process.stderr.write(msg);
    process.exit(2);
  }

  // ── Layer 2: 确认后移动文件 ─────────────────────────
  if (!result.parsed || result.parsed.targets.length === 0 && !(result.parsed.cmd === "git" && result.parsed.subcmd === "clean")) {
    // 解析不出目标 → 阻断但不移动
    const msg =
      `[delete_safety_guard] BLOCKED (unparseable targets, even with approval).\n` +
      `  Command: ${cmd}\n` +
      `  Cannot safely move files. Please handle manually.\n`;
    log({ action: "blocked_unparseable", reason: result.reason, command: cmd, cwd });
    process.stderr.write(msg);
    process.exit(2);
  }

  const ts = timestamp();
  const backupDir = path.join(BACKUP_ROOT, ts);
  const targetFiles = collectTargetFiles(result.parsed, cwd);

  if (targetFiles.length === 0) {
    // 没有实际文件需要移动 → 直接放行
    log({ action: "approved_no_files", reason: result.reason, command: cmd, cwd });
    process.stderr.write(
      `[delete_safety_guard] Approved (no target files found to move).\n`
    );
    // 清理 .delete-approved
    try {
      const projectDir = (process.env.CLAUDE_PROJECT_DIR || process.cwd()).replace(/\\/g, "/");
      fs.unlinkSync(path.join(projectDir, APPROVED_FILE));
    } catch {}
    process.exit(0);
  }

  // 执行移动
  const { moved, errors, manifest } = moveWithStructure(targetFiles, cwd, backupDir);

  // 更新 manifest 中的 command
  try {
    const mf = path.join(backupDir, "manifest.json");
    const data = JSON.parse(fs.readFileSync(mf, "utf-8"));
    data.command = cmd;
    fs.writeFileSync(mf, JSON.stringify(data, null, 2), "utf-8");
  } catch {}

  const msg =
    `[delete_safety_guard] APPROVED → Files moved to safe location:\n` +
    `  Backup: ${backupDir}\n` +
    `  Moved ${moved.length} file(s), ${errors.length} error(s)\n` +
    `  Manifest: ${path.join(backupDir, "manifest.json")}\n` +
    `  Original command now proceeding.\n`;

  log({
    action: "moved",
    reason: result.reason,
    command: cmd,
    cwd,
    backupDir,
    fileCount: moved.length,
    errors: errors.length,
  });

  process.stderr.write(msg);

  // 清理 .delete-approved（一次性使用）
  try {
    const projectDir = (process.env.CLAUDE_PROJECT_DIR || process.cwd()).replace(/\\/g, "/");
    fs.unlinkSync(path.join(projectDir, APPROVED_FILE));
  } catch {}

  process.exit(0); // 放行原始命令（文件已移走）
}

function loadPayload() {
  const raw = fs.readFileSync(0, "utf-8").trim();
  if (!raw) return {};
  try {
    const p = JSON.parse(raw);
    return typeof p === "object" && p !== null ? p : {};
  } catch { return {}; }
}

main();