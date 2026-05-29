#!/usr/bin/env python3
"""PostToolUse hook: git commit 后保底写入 changelog 草稿。

保底逻辑：如果 AI 没有手动生成完整双轨 changelog，此 hook 确保至少有一行
简要记录写入 docs/changes/changelog-draft.md。

双轨 changelog 规范见 workflows.md「Changelog 自动生成规则」。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(command_args: list[str], workdir: Path) -> subprocess.CompletedProcess:
    """执行命令并返回结果。"""
    return subprocess.run(
        command_args,
        cwd=str(workdir),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def get_project_dir() -> Path:
    """获取项目目录，优先读取环境变量。"""
    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if project_dir_text:
        return Path(project_dir_text).resolve()
    return Path.cwd().resolve()


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


def is_git_commit_event(payload: dict) -> bool:
    """判断当前 PostToolUse 是否来自 git commit。"""
    tool_name = payload.get("tool_name", "")
    if tool_name != "Bash":
        return False
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return False
    command_text = str(tool_input.get("command", ""))
    return bool(re.search(r"\bgit\s+commit\b", command_text))


def get_last_commit(project_dir: Path) -> tuple[str, str] | tuple[None, None]:
    """读取最近一次提交 hash 与主题。"""
    hash_result = run_command(["git", "log", "-1", "--pretty=%H"], project_dir)
    subject_result = run_command(["git", "log", "-1", "--pretty=%s"], project_dir)
    if hash_result.returncode != 0 or subject_result.returncode != 0:
        return None, None
    commit_hash = hash_result.stdout.strip()
    commit_subject = subject_result.stdout.strip()
    if not commit_hash or not commit_subject:
        return None, None
    return commit_hash, commit_subject


def get_next_seq(changes_dir: Path) -> int:
    """扫描 docs/changes/ 下已有文件，返回下一个序号。"""
    max_seq = 0
    if changes_dir.exists():
        for f in changes_dir.iterdir():
            if f.is_file() and f.suffix == ".md" and f.name not in ("README.md", "CHANGELOG.md"):
                try:
                    seq = int(f.name.split("-")[0])
                    max_seq = max(max_seq, seq)
                except (ValueError, IndexError):
                    pass
    return max_seq + 1


def build_draft_line(commit_hash: str, commit_subject: str) -> str:
    """构建 changelog 草稿条目。"""
    time_text = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"- {time_text} [{commit_hash[:7]}] {commit_subject}"


def main() -> int:
    """脚本入口。"""
    parser = argparse.ArgumentParser(description="追加 changelog 草稿条目")
    parser.add_argument("--dry-run", action="store_true", help="仅打印条目，不写文件")
    args = parser.parse_args()
    payload = load_payload()
    if payload and not is_git_commit_event(payload):
        return 0

    project_dir = get_project_dir()
    if not project_dir.exists():
        print(f"[SKIP] 项目目录不存在: {project_dir}")
        return 0

    git_check = run_command(["git", "rev-parse", "--is-inside-work-tree"], project_dir)
    if git_check.returncode != 0:
        print(f"[SKIP] 非 Git 仓库: {project_dir}")
        return 0

    commit_hash, commit_subject = get_last_commit(project_dir)
    if not commit_hash or not commit_subject:
        print("[SKIP] 未读取到提交信息")
        return 0

    # 新路径：docs/changes/
    changes_dir = project_dir / "docs" / "changes"
    changes_dir.mkdir(parents=True, exist_ok=True)
    draft_path = changes_dir / "changelog-draft.md"

    draft_line = build_draft_line(commit_hash, commit_subject)

    # 检查是否已有完整双轨文档（人看版）
    seq = get_next_seq(changes_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")
    expected_full = changes_dir / f"{seq:04d}-{date_str}-{commit_hash[:7]}-*.md"

    # 检查是否已有对应编号的完整文档
    has_full_doc = False
    if changes_dir.exists():
        for f in changes_dir.iterdir():
            if f.is_file() and commit_hash[:7] in f.name and f.name not in ("README.md", "CHANGELOG.md", "changelog-draft.md"):
                has_full_doc = True
                break

    if has_full_doc:
        print(f"[OK] 已有完整双轨文档，跳过草稿保底")
        return 0

    if draft_path.exists():
        existing_lines = draft_path.read_text(encoding="utf-8").splitlines()
        if existing_lines and existing_lines[-1].strip() == draft_line.strip():
            print("[SKIP] 草稿已是最新，不重复追加")
            return 0
    else:
        existing_lines = [
            "# Changelog Draft（保底）",
            "",
            "> 此文件由 PostToolUse hook 自动生成。如果 AI 已生成完整双轨文档，此文件可忽略。",
            "> 完整版见同目录下 序号-日期-hash-标题.md 文件。",
            "",
        ]

    if args.dry_run:
        print(f"[DRY-RUN] 将追加条目: {draft_line}")
        return 0

    new_lines = existing_lines + [draft_line]
    draft_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"[OK] 已更新 {draft_path}（保底记录，AI 应生成完整双轨文档）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
