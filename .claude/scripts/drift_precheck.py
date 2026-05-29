#!/usr/bin/env python3
"""drift_precheck.py

确定性预检：对比 allowed_paths 与 git diff，输出确定性结论。
direction-reviewer 在调用 LLM 前可先执行此脚本，覆盖 ~70% 正常场景。

用法：
  python .claude/scripts/drift_precheck.py --allowed-paths "file1.py" "dir/" ...

输出：
  JSON: {"status": "PASS"|"UNCERTAIN"|"BLOCK", "reason": "...", "files_outside": [...]}
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def get_project_dir() -> Path:
    import os
    text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    return Path(text).resolve() if text else Path.cwd().resolve()


def get_modified_files(project_dir: Path) -> list[str] | None:
    """获取 git diff 中已修改的文件列表。返回 None 表示 git 不可用。"""
    encoding = "utf-8"
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, cwd=project_dir, timeout=10,
        )
        if result.returncode != 0:
            return None
        stdout = result.stdout.decode(encoding, errors="replace")

        result2 = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, cwd=project_dir, timeout=10,
        )
        stdout2 = result2.stdout.decode(encoding, errors="replace")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None

    files = set(stdout.strip().splitlines() + stdout2.strip().splitlines())
    return sorted(f for f in files if f)


def normalize_path(p: str) -> str:
    """归一化路径分隔符为 /（统一 Windows/Unix）。"""
    return p.replace("\\", "/")


def is_under_allowed_path(file_path: str, allowed_paths: list[str]) -> bool:
    """判断文件是否在 allowed_paths 列表内（路径分隔符归一化后比较）。"""
    normalized_file = normalize_path(file_path)
    for allowed in allowed_paths:
        normalized_allowed = normalize_path(allowed)
        if normalized_file == normalized_allowed:
            return True
        if normalized_allowed.endswith("/"):
            if normalized_file.startswith(normalized_allowed):
                return True
        elif normalized_file.startswith(normalized_allowed + "/"):
            return True
    return False


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="方向漂移确定性预检")
    parser.add_argument("--allowed-paths", nargs="*", default=[], help="允许修改的文件/目录列表")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    # Windows UTF-8
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

    project_dir = get_project_dir()
    modified_files = get_modified_files(project_dir)

    # Git 不可用 → 不做假设，交给 LLM 判断
    if modified_files is None:
        result = {
            "status": "UNCERTAIN",
            "reason": "git 不可用或非 git 仓库，需 LLM 判断",
            "files_outside": [],
        }
    elif not modified_files:
        result = {"status": "PASS", "reason": "无修改文件", "files_outside": []}
    elif not args.allowed_paths:
        result = {
            "status": "UNCERTAIN",
            "reason": "无 allowed_paths，需 LLM 判断",
            "files_outside": modified_files,
        }
    else:
        outside = [f for f in modified_files if not is_under_allowed_path(f, args.allowed_paths)]
        if not outside:
            result = {
                "status": "PASS",
                "reason": "所有修改文件在 allowed_paths 内",
                "files_outside": [],
            }
        else:
            result = {
                "status": "UNCERTAIN",
                "reason": f"{len(outside)} 个文件超出 allowed_paths，需 LLM 判断",
                "files_outside": outside,
            }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status_emoji = {"PASS": "✅", "UNCERTAIN": "❓", "BLOCK": "🚫"}
        print(f"{status_emoji.get(result['status'], '?')} drift_precheck: {result['status']}")
        print(f"  原因: {result['reason']}")
        if result["files_outside"]:
            print(f"  超出文件: {', '.join(result['files_outside'][:8])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
