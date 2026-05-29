#!/usr/bin/env python3
"""PostToolUse hook：记录 AI 是否读取过修订记录相关上下文。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


REVISION_DIR = Path("docs") / "修订记录"
INDEX_PATH = REVISION_DIR / "目录索引.md"
AI_CONTEXT_DIR = Path(".claude") / "memory" / "context" / "revision"
AUDIT_LOG_PATH = Path(".claude") / "state" / "revision_read_audit.jsonl"


def configure_streams() -> None:
    """将标准流调整为 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="修订记录读取审计 Hook")
    parser.add_argument("--project-dir", default="", help="项目根目录，可选")
    parser.add_argument("--force-path", default="", help="手动指定读取目标路径，调试时可用")
    return parser.parse_args(argv)


def get_project_dir(project_dir_text: str) -> Path:
    """获取项目根目录。"""
    if project_dir_text.strip():
        return Path(project_dir_text).resolve()
    env_project_dir = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if env_project_dir:
        return Path(env_project_dir).resolve()
    return Path.cwd().resolve()


def load_payload() -> dict:
    """读取 Hook 输入。"""
    raw_text = ""
    try:
        raw_text = sys.stdin.read().strip()
    except OSError:
        raw_text = ""
    if not raw_text:
        raw_text = os.getenv("CLAUDE_TOOL_INPUT", "").strip()
    if not raw_text:
        return {}
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def extract_tool_name(payload: dict) -> str:
    """提取工具名。"""
    tool_name = payload.get("tool_name") or payload.get("hook_event_name") or ""
    return str(tool_name).strip()


def extract_tool_input(payload: dict) -> dict:
    """提取工具输入。"""
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        return tool_input
    return payload


def extract_file_path(tool_input: dict) -> str:
    """提取目标文件路径。"""
    for key_name in ("file_path", "path", "filepath"):
        path_text = tool_input.get(key_name)
        if isinstance(path_text, str) and path_text.strip():
            return path_text.strip()
    return ""


def resolve_target_path(path_text: str, project_dir: Path) -> Path | None:
    """将路径解析为绝对路径。"""
    cleaned_text = path_text.strip()
    if not cleaned_text:
        return None
    target_path = Path(cleaned_text)
    if not target_path.is_absolute():
        target_path = (project_dir / target_path).resolve()
    else:
        target_path = target_path.resolve()
    return target_path


def classify_target_path(target_path: Path, project_dir: Path) -> tuple[str, str] | tuple[None, None]:
    """识别读取目标属于哪类修订记录上下文。"""
    try:
        relative_path = target_path.relative_to(project_dir).as_posix()
    except ValueError:
        return None, None

    if relative_path == INDEX_PATH.as_posix():
        return "index", relative_path
    if relative_path.startswith(f"{AI_CONTEXT_DIR.as_posix()}/") and relative_path.endswith(".md"):
        return "ai_context", relative_path
    if relative_path.startswith(f"{REVISION_DIR.as_posix()}/") and relative_path.endswith(".md"):
        if relative_path == INDEX_PATH.as_posix():
            return "index", relative_path
        return "record", relative_path
    return None, None


def detect_target(payload: dict, project_dir: Path, force_path_text: str) -> tuple[str | None, str | None, str]:
    """识别当前是否需要记账。"""
    if force_path_text.strip():
        target_path = resolve_target_path(force_path_text, project_dir)
        if target_path is None:
            return None, None, "未提供有效的 force-path"
        category, relative_path = classify_target_path(target_path, project_dir)
        if category is None or relative_path is None:
            return None, None, "force-path 不属于修订记录上下文"
        return category, relative_path, ""

    if not payload:
        return None, None, "未收到 Hook payload"
    if extract_tool_name(payload) != "Read":
        return None, None, "当前事件不是 Read"

    target_path = resolve_target_path(extract_file_path(extract_tool_input(payload)), project_dir)
    if target_path is None:
        return None, None, "未识别到读取文件路径"

    category, relative_path = classify_target_path(target_path, project_dir)
    if category is None or relative_path is None:
        return None, None, "目标文件不属于修订记录上下文"
    return category, relative_path, ""


def append_audit_log(project_dir: Path, category: str, relative_path: str) -> None:
    """追加读取审计日志。"""
    log_path = project_dir / AUDIT_LOG_PATH
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": category,
        "relative_path": relative_path,
    }
    with log_path.open("a", encoding="utf-8") as file_obj:
        file_obj.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    """脚本入口。"""
    configure_streams()
    args = parse_args(argv)
    project_dir = get_project_dir(args.project_dir)
    category, relative_path, skip_reason = detect_target(load_payload(), project_dir, args.force_path)

    if category is None or relative_path is None:
        print(f"[revision_read_audit] 跳过：{skip_reason}")
        return 0

    append_audit_log(project_dir, category, relative_path)
    print(f"[revision_read_audit] 已记录读取：{category} -> {relative_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
