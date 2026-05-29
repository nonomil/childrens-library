#!/usr/bin/env python3
"""freeze_baseline.py

在 gate approval 时冻结任务契约哈希到 .meta.yaml。
CC 在写入 .gate-approved 后调用此脚本。

用法：
  python .claude/scripts/freeze_baseline.py [--task-id T042] [--plan docs/plan/PLAN.md]
"""

from __future__ import annotations

import hashlib
import sys
from datetime import datetime
from pathlib import Path


def get_project_dir() -> Path:
    """获取项目目录。"""
    import os
    text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    return Path(text).resolve() if text else Path.cwd().resolve()


def sha256_short(text: str, length: int = 8) -> str:
    """计算文本的 SHA256 前 N 位。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def extract_task_line(plan_path: Path, task_id: str) -> str:
    """从 PLAN.md 提取指定 task_id 的任务行。"""
    if not plan_path.exists():
        return ""
    for line in plan_path.read_text(encoding="utf-8").splitlines():
        if task_id in line and "|" in line:
            return line.strip()
    return ""


def main() -> int:
    import argparse

    # Windows UTF-8
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

    parser = argparse.ArgumentParser(description="冻结任务契约基线哈希")
    parser.add_argument("--task-id", required=True, help="任务 ID（如 T042）")
    parser.add_argument(
        "--plan",
        default="docs/plan/PLAN.md",
        help="PLAN.md 路径（默认 docs/plan/PLAN.md）",
    )
    parser.add_argument(
        "--allowed-paths",
        nargs="*",
        default=None,
        help="允许修改的文件/目录列表",
    )
    args = parser.parse_args()

    project_dir = get_project_dir()
    plan_path = project_dir / args.plan

    # 定位任务目录
    task_dirs = sorted(project_dir.glob(f"docs/plan/tasks/{args.task_id}*"))
    if not task_dirs:
        # 任务目录不存在，只冻结 PLAN 行哈希
        task_line = extract_task_line(plan_path, args.task_id)
        if not task_line:
            print(f"[freeze_baseline] 未找到任务 {args.task_id} 的 PLAN 行", file=sys.stderr)
            return 1
        plan_hash = sha256_short(task_line)
        print(f"plan_hash={plan_hash} (无任务目录，仅冻结 PLAN 行)")
        return 0

    task_dir = task_dirs[0]

    # 收集哈希
    hashes: dict[str, str] = {}
    task_line = extract_task_line(plan_path, args.task_id)
    if task_line:
        hashes["approved_plan_hash"] = sha256_short(task_line)

    acceptance_path = task_dir / "acceptance.md"
    if acceptance_path.exists():
        hashes["approved_acceptance_hash"] = sha256_short(
            acceptance_path.read_text(encoding="utf-8")
        )

    steps_path = task_dir / "steps.md"
    if steps_path.exists():
        hashes["approved_steps_hash"] = sha256_short(
            steps_path.read_text(encoding="utf-8")
        )

    if args.allowed_paths:
        paths_str = "\n".join(sorted(args.allowed_paths))
        hashes["allowed_paths_hash"] = sha256_short(paths_str)

    # 至少需要一个实际哈希（不只是时间戳）
    real_hashes = {k: v for k, v in hashes.items() if k != "frozen_at"}
    if not real_hashes:
        print(
            "[freeze_baseline] 无法冻结：PLAN 行、acceptance.md、allowed_paths 均未找到",
            file=sys.stderr,
        )
        return 1

    hashes["frozen_at"] = datetime.now().isoformat(timespec="seconds")

    # 写入 .meta.yaml
    meta_path = task_dir / ".meta.yaml"
    existing_lines: list[str] = []
    if meta_path.exists():
        existing_lines = meta_path.read_text(encoding="utf-8").splitlines()

    # 检查是否已有 baseline 段
    baseline_block = ["baseline:"]
    for key, value in hashes.items():
        baseline_block.append(f"  {key}: \"{value}\"")

    # 替换或追加 baseline 段
    new_lines: list[str] = []
    in_baseline = False
    baseline_written = False
    for line in existing_lines:
        if line.strip().startswith("baseline:"):
            in_baseline = True
            if not baseline_written:
                new_lines.extend(baseline_block)
                baseline_written = True
            continue
        if in_baseline and line.startswith("  ") and ":" in line:
            continue
        if in_baseline and not line.startswith("  "):
            in_baseline = False
        if not in_baseline:
            new_lines.append(line)

    if not baseline_written:
        new_lines.append("")
        new_lines.extend(baseline_block)

    meta_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    frozen_items = ", ".join(f"{k}={v}" for k, v in hashes.items())
    print(f"[freeze_baseline] 已冻结: {frozen_items} → {meta_path.relative_to(project_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
