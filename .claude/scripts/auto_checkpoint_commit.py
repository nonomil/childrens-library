#!/usr/bin/env python3
"""自动 checkpoint 提交脚本。

Stop hook 只做保底自动提交，不在 hook 阶段触发交互式选择。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

# --- 阈值配置 ---
MAX_CHANGED_FILES_AUTO = 30          # 放宽到 30 个文件（原 10 过于保守）
MAX_STREAK_AGE_MINUTES = 120
SESSION_RECENT_MINUTES = 30          # 30 分钟内的改动视为"本次会话"
BACKUP_BRANCH_PREFIX = "backup/auto-before-checkpoint"
BACKUP_DIR_NAME = ".claude/backups"
CONFLICT_MARKER_PATTERN = re.compile(r"(?m)^(<<<<<<<|=======|>>>>>>>)")


def run_git(*args: str, workdir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(workdir),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def configure_streams() -> None:
    """将标准流调整为 UTF-8，避免 Windows 控制台编码问题。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


def get_project_dir() -> Path:
    text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if text:
        return Path(text).resolve()
    return Path.cwd().resolve()


def read_git_strategy(project_dir: Path) -> str:
    """读取 git_strategy 偏好，缺失或非法时返回默认值 'auto_commit'。"""
    pref_path = project_dir / ".claude" / "preferences.json"
    valid = {"auto_commit", "ask", "skip"}
    try:
        with open(pref_path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("profile") == "minimal":
            return "skip"
        val = data.get("git_strategy", "auto_commit")
        if val not in valid:
            print(f"[WARN] git_strategy='{val}' 不合法，使用默认 'auto_commit'")
            return "auto_commit"
        return val
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return "auto_commit"


def is_git_repo(d: Path) -> bool:
    r = run_git("rev-parse", "--is-inside-work-tree", workdir=d)
    return r.returncode == 0 and r.stdout.strip() == "true"


def detect_worktree(d: Path) -> dict:
    """检测 worktree 状态。返回 {in_worktree, worktree_count, is_bare_project}。"""
    info = {"in_worktree": False, "worktree_count": 0, "is_bare_project": False}

    r = run_git("worktree", "list", "--porcelain", workdir=d)
    if r.returncode != 0:
        return info

    wt_lines = r.stdout.strip().splitlines()
    wt_paths = [
        l.split(" ", 1)[-1]
        for l in wt_lines
        if l.startswith("worktree ")
    ]
    info["worktree_count"] = len(wt_paths)

    # 判断当前目录是否在某个 worktree 中（排除 bare repo 本身）
    cwd_str = str(d).rstrip("/\\")
    for p in wt_paths[1:]:  # index 0 通常是主仓库或 bare
        if p.rstrip("/\\") == cwd_str:
            info["in_worktree"] = True
            break

    # 检测是否 bare repo 项目（父目录有 .git 文件或当前目录有 .bare）
    parent = d.parent
    info["is_bare_project"] = (
        (parent / ".git").is_file() or (d / ".bare").is_dir()
    )

    return info


def get_current_branch(d: Path) -> str:
    r = run_git("branch", "--show-current", workdir=d)
    return r.stdout.strip() or "HEAD"


def get_changed_files(d: Path) -> list[str]:
    r = run_git("status", "--porcelain", workdir=d)
    if r.returncode != 0:
        return []
    files = []
    for line in r.stdout.strip().splitlines():
        if line.strip():
            parts = line[3:].strip()
            if parts:
                files.append(parts)
    return files


def get_recent_commits_authors(d: Path, count: int = 5) -> list[str]:
    r = run_git("log", f"-{count}", "--format=%an", workdir=d)
    if r.returncode != 0:
        return []
    return [a.strip() for a in r.stdout.strip().splitlines() if a.strip()]


def get_oldest_unstaged_age_minutes(d: Path) -> float | None:
    files = get_changed_files(d)
    if not files:
        return None
    now_ts = datetime.now().timestamp()
    oldest = 0.0
    for f in files:
        fp = d / f
        try:
            if fp.exists():
                age = now_ts - fp.stat().st_mtime
                if age > oldest:
                    oldest = age
        except OSError:
            continue
    return oldest / 60.0 if oldest > 0 else None


def has_merge_conflict_marker(file_path: Path) -> bool:
    """只识别真实的 Git 冲突标记行，避免误伤文档示例或脚本源码字符串。"""
    try:
        content_text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return bool(CONFLICT_MARKER_PATTERN.search(content_text))


def analyze_workspace(d: Path, wt_info: dict | None = None) -> dict:
    changed = get_changed_files(d)
    if not changed:
        return {"status": "clean", "changed_files": [], "warnings": []}

    warnings: list[str] = []
    in_wt = wt_info and wt_info.get("in_worktree", False)

    # --- 本次会话改动检测 ---
    # 如果所有改动文件都在 SESSION_RECENT_MINUTES 内修改过，视为本次会话产出
    age = get_oldest_unstaged_age_minutes(d)
    all_recent = age is not None and age <= SESSION_RECENT_MINUTES

    # worktree 内放宽文件数阈值（worktree 已提供隔离）
    file_threshold = MAX_CHANGED_FILES_AUTO * 2 if in_wt else MAX_CHANGED_FILES_AUTO
    # 本次会话改动进一步放宽阈值（本次任务产出，不是累积脏文件）
    if all_recent:
        file_threshold = MAX_CHANGED_FILES_AUTO * 5

    if len(changed) > file_threshold:
        warnings.append(f"变更文件过多 ({len(changed)} 个 > {file_threshold})")

    authors = get_recent_commits_authors(d)
    unique_authors = set(authors)
    if len(unique_authors) > 1:
        warnings.append(f"最近提交来自多个作者: {', '.join(unique_authors)}")

    non_claude = [f for f in changed if not f.startswith(".claude/")]
    claude = [f for f in changed if f.startswith(".claude/")]
    if non_claude and claude:
        warnings.append(
            f"混合变更: .claude/ 内 {len(claude)} 个 + 其他 {len(non_claude)} 个"
        )

    if age is not None and age > MAX_STREAK_AGE_MINUTES:
        warnings.append(f"存在陈旧变更 (> {MAX_STREAK_AGE_MINUTES} 分钟未提交)")

    # 冲突标记检测
    for f in changed:
        if f.endswith((".py", ".js", ".ts", ".md", ".yaml", ".toml")):
            fp = d / f
            if fp.exists() and has_merge_conflict_marker(fp):
                warnings.append(f"发现冲突标记: {f}")

    status = "dirty" if warnings else "clean"
    return {
        "status": status,
        "changed_files": changed,
        "non_claude_changes": non_claude,
        "claude_changes": claude,
        "warnings": warnings,
        "all_recent": all_recent,
    }


def create_backup_branch(d: Path) -> str | None:
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    branch = f"{BACKUP_BRANCH_PREFIX}-{now}"
    r = run_git("branch", branch, workdir=d)
    return branch if r.returncode == 0 else None


def create_zip_backup(d: Path, changed_files: list[str]) -> str | None:
    """将变更文件打包为 zip 备份。返回 zip 路径或 None。"""
    backup_dir = d / BACKUP_DIR_NAME
    backup_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"checkpoint-backup-{now}.zip"
    zip_path = backup_dir / zip_name

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # 写入 manifest
            manifest = [
                f"Backup created: {datetime.now().isoformat()}",
                f"Branch: {get_current_branch(d)}",
                f"Files: {len(changed_files)}",
                "",
                "Changed files:",
            ]
            for f in changed_files:
                manifest.append(f"  {f}")
            zf.writestr("_manifest.txt", "\n".join(manifest))

            # 打包变更文件
            for f in changed_files:
                fp = d / f
                if fp.exists() and fp.is_file():
                    try:
                        zf.write(fp, f)
                    except OSError:
                        pass

        return str(zip_path)
    except Exception:
        return None


def _remind_lessons() -> None:
    """会话结束提醒：检查 lessons.md 是否需要更新。"""
    print()
    print("[提醒] 请确认本次会话是否需要更新 .claude/memory/lessons/：")
    print("  - 用户是否纠正过 AI 的错误？")
    print("  - Bug 修复是否完成？")
    print("  - 是否触发过模式升级？")
    print("  若有，请写入后再结束会话。")


def do_commit(d: Path, message: str) -> bool:
    add_r = run_git("add", "-A", workdir=d)
    if add_r.returncode != 0:
        print(f"[WARN] git add 失败: {add_r.stderr.strip()}")
        return False

    diff_r = run_git("diff", "--cached", "--quiet", workdir=d)
    if diff_r.returncode == 0:
        print("[SKIP] 无暂存改动，不提交")
        return False

    commit_r = run_git("commit", "-m", message, workdir=d)
    if commit_r.returncode != 0:
        print(f"[WARN] 提交失败: {commit_r.stderr.strip()}")
        return False

    print(commit_r.stdout.strip() or f"[OK] 已提交: {message}")
    return True


def main() -> int:
    configure_streams()
    parser = argparse.ArgumentParser(description="自动 checkpoint 提交（带安全检测 + zip 备份）")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="跳过脏工作区检测，强制提交")
    parser.add_argument("--no-zip", action="store_true", help="跳过 zip 备份")
    args = parser.parse_args()

    project_dir = get_project_dir()
    if not project_dir.exists():
        print(f"[SKIP] 项目目录不存在: {project_dir}")
        return 0

    if not is_git_repo(project_dir):
        print(f"[SKIP] 非 Git 仓库: {project_dir}")
        return 0

    git_strategy = read_git_strategy(project_dir)
    if git_strategy == "skip":
        print("[SKIP] git_strategy=skip，不自动提交")
        return 0
    if git_strategy == "ask":
        print("[INFO] git_strategy=ask，请在会话内确认是否提交")
        # Stop Hook 是异步的，无法交互询问，只输出提醒
        return 0

    wt_info = detect_worktree(project_dir)
    diag = analyze_workspace(project_dir, wt_info)

    # --- 干净状态 ---
    if diag["status"] == "clean":
        msg = f"checkpoint: {datetime.now().strftime('%H:%M')}"
        if wt_info.get("in_worktree"):
            msg += " [worktree]"
        if args.dry_run:
            print(f"[DRY-RUN] 干净提交: {msg}")
            _remind_lessons()
            return 0
        do_commit(project_dir, msg)
        _remind_lessons()
        return 0

    # --- 脏工作区：只告警，不阻断 Stop hook ---
    warnings = diag["warnings"]
    changed = diag["changed_files"]

    print()
    print("[SKIP]" + "=" * 58)
    print("[SKIP] 工作区存在需人工确认的风险，跳过自动 checkpoint")
    print("[SKIP]" + "=" * 58)
    print(f"[SKIP] 变更文件数: {len(changed)}")
    if wt_info.get("in_worktree"):
        print(f"[SKIP] Worktree: 已隔离 (共 {wt_info.get('worktree_count', 0)} 个)")
    for w in warnings:
        print(f"[SKIP] WARN {w}")
    print("[SKIP] 如需提交，请在会话中明确整理后手动执行。")

    backup_dir = project_dir / BACKUP_DIR_NAME
    if backup_dir.exists():
        old_zips = sorted(backup_dir.glob("checkpoint-backup-*.zip"))
        if old_zips:
            total_size = sum(f.stat().st_size for f in old_zips) / (1024 * 1024)
            print(f"[SKIP] 旧备份: {len(old_zips)} 个，占用 {total_size:.0f} MB")
            print(f"[SKIP] 路径: {backup_dir}")

    print("[SKIP]" + "=" * 59)
    print()

    if not args.force:
        return 0

    # 强制模式仅供人工命令使用
    print("[FORCE] 手动强制提交，执行中...")
    msg = f"checkpoint: {datetime.now().strftime('%H:%M')} (force, {len(changed)} files)"
    if args.dry_run:
        print(f"[DRY-RUN] 强制提交: {msg}")
        return 0
    do_commit(project_dir, msg)
    _remind_lessons()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
