#!/usr/bin/env python3
"""写入新鲜的 .gate-approved 文件，自动使用当前时间戳。

用法:
    python .claude/scripts/write_gate.py "任务描述" [executor] [mode]
    python .claude/scripts/write_gate.py --check   # 仅检查当前 gate 状态

示例:
    python .claude/scripts/write_gate.py "codex-review-eval"
    python .claude/scripts/write_gate.py "codex-review-eval" claude-code codex-review
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


def get_project_dir() -> Path:
    """获取项目目录。"""
    import os
    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if project_dir_text:
        return Path(project_dir_text).resolve()
    return Path(__file__).resolve().parent.parent.parent


def write_gate(task: str, executor: str = "claude-code", mode: str = "codex-review") -> Path:
    """写入 gate 文件，返回路径。"""
    project_dir = get_project_dir()
    gate_file = project_dir / ".claude" / "state" / ".gate-approved"
    gate_file.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "task": task,
        "approved_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "executor": executor,
        "mode": mode,
    }
    gate_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return gate_file


def check_gate() -> None:
    """检查当前 gate 状态。"""
    project_dir = get_project_dir()
    gate_file = project_dir / ".claude" / "state" / ".gate-approved"

    if not gate_file.exists():
        print("gate 文件不存在")
        return

    payload = json.loads(gate_file.read_text(encoding="utf-8"))
    approved_at_str = payload.get("approved_at", "")
    approved_at = datetime.fromisoformat(approved_at_str)
    age_minutes = (datetime.now() - approved_at).total_seconds() / 60

    print(f"task: {payload.get('task', '?')}")
    print(f"approved_at: {approved_at_str}")
    print(f"age: {age_minutes:.1f} min")
    print(f"status: {'VALID' if age_minutes <= 30 else 'EXPIRED'}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--check":
        check_gate()
        return

    task = sys.argv[1]
    executor = sys.argv[2] if len(sys.argv) > 2 else "claude-code"
    mode = sys.argv[3] if len(sys.argv) > 3 else "codex-review"

    gate_file = write_gate(task, executor, mode)
    print(f"gate written: {gate_file}")
    print(f"approved_at: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}")


if __name__ == "__main__":
    main()
