#!/usr/bin/env python3
"""Git Safety PreToolUse Hook for Claude Code。

共享配置统一使用 `matcher: "Bash"`，由脚本内部识别是否为 git commit / push。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime

CONFLICT_MARKER_PATTERN = re.compile(r"(?m)^(<<<<<<<|=======|>>>>>>>)")


def configure_stderr() -> None:
    """将 stderr 调整为 UTF-8，避免 Windows 控制台乱码。"""
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


def load_payload() -> dict:
    """读取 hook 输入。"""
    raw_text = ""
    try:
        raw_text = sys.stdin.read()
    except OSError:
        raw_text = ""
    if not raw_text.strip():
        raw_text = os.getenv("CLAUDE_TOOL_INPUT", "").strip()
    if not raw_text:
        return {}
    try:
        payload = json.loads(raw_text)
        return payload if isinstance(payload, dict) else {}
    except json.JSONDecodeError:
        return {}


def run_git(*args: str, cwd: str | None = None) -> tuple[str, int]:
    """执行 git 命令，返回 (stdout, returncode)。"""
    try:
        r = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return r.stdout.strip(), r.returncode
    except Exception:
        return "", 1


def has_merge_conflict_marker(file_path: str) -> bool:
    """只识别真实的 Git 冲突标记行，避免误伤示例文本。"""
    try:
        content = open(file_path, encoding="utf-8", errors="replace").read()
    except OSError:
        return False
    return bool(CONFLICT_MARKER_PATTERN.search(content))


def is_git_write_op(tool_input: dict) -> tuple[bool, str]:
    """判断命令是否为 git commit / push / add+commit 链。"""
    cmd = tool_input.get("command", "")
    patterns = [
        r"\bgit\s+commit\b",
        r"\bgit\s+push\b",
        r"\bgit\s+add\b.*&&.*\bgit\s+commit\b",
    ]
    for p in patterns:
        if re.search(p, cmd):
            return True, cmd
    return False, cmd


# ── 工作区分析 ──────────────────────────────────────────────

def analyze_workspace(cwd: str | None = None) -> dict:
    """深度分析工作区状态，含 worktree 感知。"""
    ws: dict = {}

    # 1. 文件状态细分（staged / unstaged / untracked）
    status_out, _ = run_git("status", "--porcelain", cwd=cwd)
    lines = [l for l in status_out.splitlines() if l.strip()]
    ws["staged"] = [l[3:].strip() for l in lines if l[0] in "AMDR" and l[0] != " "]
    ws["unstaged"] = [l[3:].strip() for l in lines if l[1] in "MD"]
    ws["untracked"] = [l[3:].strip() for l in lines if l.startswith("??")]
    ws["staged_count"] = len(ws["staged"])
    ws["unstaged_count"] = len(ws["unstaged"])
    ws["untracked_count"] = len(ws["untracked"])
    ws["total_dirty"] = len(lines)

    # 2. 最近 commit 时间
    last_ts, rc = run_git("log", "-1", "--format=%ct", cwd=cwd)
    ws["last_commit_ts"] = int(last_ts) if rc == 0 and last_ts else 0

    # 3. mtime 跨度分析（多工具交替修改检测）
    if ws["unstaged"]:
        mtimes = []
        for fname in ws["unstaged"][:20]:
            fpath = os.path.join(cwd or ".", fname)
            try:
                mtimes.append(int(os.path.getmtime(fpath)))
            except OSError:
                pass
        span = (max(mtimes) - min(mtimes)) if mtimes else 0
        ws["mtime_span_seconds"] = span
        ws["mtime_span_minutes"] = round(span / 60, 1)
    else:
        ws["mtime_span_seconds"] = 0
        ws["mtime_span_minutes"] = 0

    # 4. 冲突标记检测
    conflict_files = []
    all_changed = ws["staged"] + ws["unstaged"]
    for fname in all_changed:
        if not fname.endswith(
            (".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".java", ".md", ".yaml", ".toml")
        ):
            continue
        fpath = os.path.join(cwd or ".", fname)
        if has_merge_conflict_marker(fpath):
            conflict_files.append(fname)
    ws["conflict_files"] = conflict_files

    # 5. stash 积压
    stash_out, _ = run_git("stash", "list", cwd=cwd)
    ws["stash_count"] = len([l for l in stash_out.splitlines() if l.strip()])

    # 6. 当前分支
    branch, _ = run_git("branch", "--show-current", cwd=cwd)
    ws["branch"] = branch or "HEAD"

    # 7. 远端差异
    ahead_s, _ = run_git("rev-list", "@{u}..HEAD", "--count", cwd=cwd)
    behind_s, _ = run_git("rev-list", "HEAD..@{u}", "--count", cwd=cwd)
    ws["ahead"] = int(ahead_s) if ahead_s.isdigit() else 0
    ws["behind"] = int(behind_s) if behind_s.isdigit() else 0

    # 8. worktree 感知
    wt_out, _ = run_git("worktree", "list", "--porcelain", cwd=cwd)
    wt_paths = [l.split(" ", 1)[-1] for l in wt_out.splitlines() if l.startswith("worktree ")]
    ws["worktree_count"] = len(wt_paths)
    ws["in_worktree"] = any(
        (cwd or "").rstrip("/") == p.rstrip("/") and "(bare)" not in wt_out
        for p in wt_paths[1:]  # index 0 是主仓库
    )
    ws["is_bare_project"] = (
        os.path.isfile(os.path.join(os.path.dirname(cwd or "."), ".git"))
        or os.path.isdir(os.path.join(cwd or ".", ".bare"))
    )

    return ws


# ── 风险评分 ────────────────────────────────────────────────

def risk_level(ws: dict) -> tuple[str, list[dict]]:
    """计算风险等级，返回 (level, issues)。
    每个 issue = {"icon": str, "key": str, "text": str}
    """
    issues: list[dict] = []
    score = 0

    if ws["conflict_files"]:
        score += 100
        issues.append({"icon": "X", "key": "conflict",
            "text": f"冲突标记未解决: {ws['conflict_files']}"})

    if ws["behind"] > 0:
        score += 40
        issues.append({"icon": "!", "key": "behind",
            "text": f"本地落后远端 {ws['behind']} 个提交，push 会被拒绝"})

    if ws["staged_count"] > 0 and ws["unstaged_count"] > 0:
        score += 10
        issues.append({"icon": "!", "key": "partial_stage",
            "text": f"已暂存 {ws['staged_count']} 个 + 未暂存 {ws['unstaged_count']} 个"
                    " — 直接 commit 只提交已暂存部分，未暂存改动可能遗漏"})

    if ws["mtime_span_minutes"] > 3:
        score += 25
        issues.append({"icon": "?", "key": "multi_tool",
            "text": f"未暂存文件修改时间跨度 {ws['mtime_span_minutes']} 分钟，"
                    "疑似多工具/手动交替修改"})

    if ws["stash_count"] >= 2:
        score += 10
        issues.append({"icon": "i", "key": "stash",
            "text": f"积压 {ws['stash_count']} 个 stash，工作区切换频繁"})

    # stash 跨 worktree 共享风险
    if ws.get("in_worktree") and ws["stash_count"] > 0:
        score += 15
        issues.append({"icon": "!", "key": "stash_shared",
            "text": f"stash 跨 worktree 共享！当前 {ws['stash_count']} 个 stash "
                    "可被其他 worktree 的工具误 pop，多工具并发时避免使用 stash"})

    if ws["untracked_count"] > 5:
        score += 8
        issues.append({"icon": "i", "key": "untracked",
            "text": f"{ws['untracked_count']} 个未跟踪文件，确认是否需要纳入"})

    if score >= 60:
        return "HIGH", issues
    elif score >= 25:
        return "MEDIUM", issues
    return "LOW", issues


# ── 场景化建议 ──────────────────────────────────────────────

def build_message(ws: dict, level: str, issues: list[dict], cmd: str) -> str:
    """根据 worktree 状态和风险等级生成场景化建议。"""
    branch = ws["branch"]
    now = datetime.now().strftime("%H:%M:%S")
    level_label = {"HIGH": "HIGH", "MEDIUM": "MEDIUM", "LOW": "LOW"}.get(level, level)

    lines = [
        "=" * 60,
        f"Git Safety Check [{now}]  分支: {branch}  风险: {level_label}",
        "=" * 60,
        "",
    ]

    # 文件状态摘要
    lines.append(f"文件状态: {ws['staged_count']} staged / {ws['unstaged_count']} unstaged / {ws['untracked_count']} untracked")
    if ws["in_worktree"]:
        lines.append(f"Worktree: 已隔离 (共 {ws['worktree_count']} 个 worktree)")
    elif ws["is_bare_project"]:
        lines.append("Worktree: bare repo 项目")
    lines.append("")

    # 问题列表
    if issues:
        lines.append("检测到的问题:")
        for i in issues:
            lines.append(f"  [{i['icon']}] {i['text']}")
        lines.append("")

    # 场景化建议
    lines.append("建议处理方案:")

    has_conflict = any(i["key"] == "conflict" for i in issues)
    has_multi_tool = any(i["key"] == "multi_tool" for i in issues)
    has_behind = any(i["key"] == "behind" for i in issues)
    has_partial = any(i["key"] == "partial_stage" for i in issues)
    has_stash_shared = any(i["key"] == "stash_shared" for i in issues)

    # 冲突 → 必须先解决
    if has_conflict:
        lines += [
            "  1. [必须] 解决所有冲突标记:",
            "     搜索 <<<<<<< 标记，决定保留哪段代码",
            "     git add <已解决的文件>",
            "     git commit",
        ]

    # 多工具混杂 + 不在 worktree → 推荐 worktree 隔离
    if has_multi_tool and not ws["in_worktree"]:
        if ws["is_bare_project"]:
            lines += [
                "  1. [推荐] 用新 worktree 隔离当前改动:",
                "     cd ..  # 回到项目根目录",
                f"     git worktree add -b fix/claude-{now.replace(':','')} claude-fix {branch}",
                "     # 把改动 stash 后 pop 到新 worktree",
                f"     cd {branch} && git stash",
                "     cd ../claude-fix && git stash pop",
                "     git add <确认的文件> && git commit -m 'fix: ...'",
            ]
        else:
            lines += [
                "  1. [推荐] 创建临时 worktree 隔离改动:",
                f"     git stash push -m 'claude-changes-{now.replace(':','')}'",
                f"     git worktree add worktrees/claude-fix -b fix/claude-temp {branch}",
                "     cd worktrees/claude-fix && git stash pop",
                "     # 在隔离环境审查 + 提交，完成后:",
                "     # git worktree remove worktrees/claude-fix",
            ]
    elif has_multi_tool and ws["in_worktree"]:
        lines += [
            "  (已在 worktree 中，工作区隔离良好，谨慎检查后可继续)",
        ]

    # stash 跨 worktree 共享风险 → 推荐用 patch 替代
    if has_stash_shared:
        lines += [
            "  [注意] stash 在所有 worktree 间共享，多工具并发时 stash pop 可能拿到其他工具的改动！",
            "     推荐用 patch 文件代替 stash：",
            "     git diff > /tmp/my-changes.patch   # 导出改动",
            "     git apply /tmp/my-changes.patch    # 在目标 worktree 应用",
        ]

    # 暂存不完整 → 分批提交
    if has_partial and not has_multi_tool:
        lines += [
            "  1. 不要用 git add .，改为按模块分批暂存:",
            "     git diff --stat",
            "     git add <文件1> <文件2>",
            "     git diff --staged",
            "     git commit -m '针对性描述'",
        ]

    # 远端落后 → 先 rebase
    if has_behind:
        lines += [
            f"  2. 先同步远端再推送:",
            "     git fetch origin",
            f"     git rebase origin/{branch}",
        ]

    # HIGH 时额外备份建议
    if level == "HIGH":
        if ws["in_worktree"]:
            lines += [
                "",
                "  保险起见先备份（worktree 内避免用 stash，用 patch）：",
                f"     git diff > /tmp/safety-{now.replace(':','')}.patch",
                "     # 出问题可用 git apply 恢复",
            ]
        else:
            lines += [
                "",
                "  保险起见先备份:",
                f"     git stash push -m 'safety-{now.replace(':','')}'",
                "     # 出问题可用 git stash pop 恢复",
            ]

    # 已在 worktree 中且 LOW/MEDIUM
    if ws["in_worktree"] and level != "HIGH":
        lines += [
            "",
            f"  当前已在 worktree ({branch}) 中，工作区隔离良好。",
        ]

    lines += [
        "",
        f"即将执行: {cmd}",
        "=" * 60,
    ]

    if level == "HIGH":
        lines.append("操作已暂停，请按上述步骤处理后再继续。")
    else:
        lines.append("已放行，但请先阅读上述警告。")

    return "\n".join(lines)


def main() -> int:
    configure_stderr()
    data = load_payload()
    tool_input = data.get("tool_input", data)
    is_dangerous, cmd = is_git_write_op(tool_input)
    if not is_dangerous:
        return 0

    cwd = tool_input.get("cwd") or os.getcwd()
    ws = analyze_workspace(cwd)
    level, issues = risk_level(ws)

    if level == "LOW" and not issues:
        return 0

    msg = build_message(ws, level, issues, cmd)
    print(msg, file=sys.stderr)

    if level == "HIGH":
        return 2  # 阻断
    return 0  # MEDIUM 放行但警告


if __name__ == "__main__":
    raise SystemExit(main())
