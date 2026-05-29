#!/usr/bin/env python3
"""PreToolUse 合并队列门禁：只允许 merge queue 队首任务进入 git merge。"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path


def configure_stderr() -> None:
    """将 stderr 调整为 UTF-8。"""
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


def parse_json_text(raw_text: str) -> dict:
    """解析 JSON 文本。"""
    if not raw_text:
        return {}
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return {"raw": raw_text}
    return payload if isinstance(payload, dict) else {"raw": raw_text}


def read_input_payload() -> dict:
    """读取 hook 输入。"""
    env_text = os.getenv("CLAUDE_TOOL_INPUT", "").strip()
    if env_text:
        return parse_json_text(env_text)

    try:
        stdin_text = sys.stdin.read().strip()
    except OSError:
        stdin_text = ""
    if stdin_text:
        return parse_json_text(stdin_text)
    return {}


def deep_find_command(payload: object) -> str:
    """递归提取命令文本。"""
    if isinstance(payload, dict):
        for key_name in ("command", "cmd", "raw", "input", "tool_input"):
            command_text = deep_find_command(payload.get(key_name))
            if command_text:
                return command_text
        for value in payload.values():
            command_text = deep_find_command(value)
            if command_text:
                return command_text
    elif isinstance(payload, list):
        for item in payload:
            command_text = deep_find_command(item)
            if command_text:
                return command_text
    elif isinstance(payload, str) and payload.strip():
        return payload
    return ""


def split_command_tokens(command_text: str) -> list[str]:
    """拆分命令 token。"""
    try:
        return shlex.split(command_text, posix=False)
    except ValueError:
        return command_text.strip().split()


def is_merge_command(command_text: str) -> bool:
    """判断是否 git merge。"""
    return bool(re.search(r"\bgit\s+merge\b", command_text, flags=re.IGNORECASE))


def extract_merge_source_branch(command_text: str) -> str:
    """提取 git merge 来源分支。"""
    tokens = split_command_tokens(command_text)
    merge_index = -1
    for index_value in range(len(tokens) - 1):
        if tokens[index_value].lower() == "git" and tokens[index_value + 1].lower() == "merge":
            merge_index = index_value + 2
            break
    if merge_index < 0:
        return ""

    options_with_value = {
        "-m",
        "--message",
        "-s",
        "--strategy",
        "-X",
        "--strategy-option",
        "--log",
        "--file",
    }
    index_value = merge_index
    while index_value < len(tokens):
        token_text = tokens[index_value]
        token_lower = token_text.lower()
        if token_text.startswith("-"):
            if token_lower in options_with_value and index_value + 1 < len(tokens):
                index_value += 2
            else:
                index_value += 1
            continue
        if token_text == "--":
            index_value += 1
            continue
        return token_text.strip().strip("\"'")
    return ""


def parse_scalar(raw_text: str) -> str:
    """解析简单 YAML 标量。"""
    value_text = raw_text.strip()
    if value_text.startswith("- "):
        value_text = value_text[2:].strip()
    if not value_text or value_text.lower() in {"null", "none", "~"}:
        return ""
    if len(value_text) >= 2 and value_text[0] == value_text[-1] and value_text[0] in {'"', "'"}:
        return value_text[1:-1]
    return value_text


def load_queue(queue_path: Path) -> list[dict[str, str]]:
    """读取 merge queue。"""
    if not queue_path.exists():
        return []
    queue_items: list[dict[str, str]] = []
    current_item: dict[str, str] | None = None
    in_items = False
    for raw_line in queue_path.read_text(encoding="utf-8").splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        indent_size = len(raw_line) - len(raw_line.lstrip(" "))
        if indent_size == 0:
            in_items = stripped_line == "items:"
            continue
        if not in_items:
            continue
        if indent_size == 2 and stripped_line == "[]":
            return []
        if indent_size == 2 and stripped_line.startswith("- "):
            if current_item:
                queue_items.append(current_item)
            current_item = {}
            remainder_text = stripped_line[2:].strip()
            if ":" in remainder_text:
                key_text, value_text = remainder_text.split(":", 1)
                current_item[key_text.strip()] = parse_scalar(value_text)
            continue
        if current_item is not None and indent_size >= 4 and ":" in stripped_line:
            key_text, value_text = stripped_line.split(":", 1)
            current_item[key_text.strip()] = parse_scalar(value_text)
    if current_item:
        queue_items.append(current_item)
    return queue_items


def load_branch_map(project_dir: Path) -> dict[str, str]:
    """读取任务 branch_or_workspace 映射。"""
    branch_map: dict[str, str] = {}
    for meta_path in sorted((project_dir / "docs" / "plan" / "tasks").glob("*/.meta.yaml")):
        task_id = meta_path.parent.name.split("-", 1)[0]
        branch_or_workspace = ""
        status = ""
        for raw_line in meta_path.read_text(encoding="utf-8").splitlines():
            stripped_line = raw_line.strip()
            if stripped_line.startswith("task_id:"):
                task_id = parse_scalar(stripped_line.split(":", 1)[1]) or task_id
            elif stripped_line.startswith("branch_or_workspace:"):
                branch_or_workspace = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("branch:") and not branch_or_workspace:
                branch_or_workspace = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("status:"):
                status = parse_scalar(stripped_line.split(":", 1)[1]).lower()
        if branch_or_workspace:
            branch_map[branch_or_workspace] = task_id
        if status == "queued" and branch_or_workspace:
            branch_map[branch_or_workspace] = task_id
    return branch_map


def emit_error(message_text: str) -> int:
    """统一阻断输出。"""
    print(f"[queue_guard] {message_text}", file=sys.stderr)
    return 2


def main() -> int:
    """脚本入口。"""
    configure_stderr()
    payload = read_input_payload()
    command_text = deep_find_command(payload) or json.dumps(payload, ensure_ascii=False)
    if not is_merge_command(command_text):
        return 0

    source_branch = extract_merge_source_branch(command_text)
    if not source_branch:
        return emit_error("无法解析 git merge 来源分支，请使用 'git merge <branch>' 形式")

    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    project_dir = Path(project_dir_text).resolve() if project_dir_text else Path.cwd().resolve()
    queue_path = project_dir / "docs" / "plan" / "MERGE_QUEUE.yaml"
    queue_items = load_queue(queue_path)
    if not queue_items:
        return 0

    head_item = queue_items[0]
    head_ref = head_item.get("merge_ref", "")
    head_task_id = head_item.get("task_id", "")

    if source_branch == head_ref:
        print(
            f"[queue_guard] merge queue 通过：队首任务 {head_task_id} -> {head_ref}",
            file=sys.stderr,
        )
        return 0

    branch_map = load_branch_map(project_dir)
    source_task_id = branch_map.get(source_branch, "")
    if source_task_id:
        return emit_error(
            f"当前 merge queue 队首是 {head_task_id} ({head_ref})，不能先合并 {source_task_id} ({source_branch})"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
