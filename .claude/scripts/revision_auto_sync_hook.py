#!/usr/bin/env python3
"""PostToolUse hook：修订记录变更后自动同步索引与 AI 轨。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path


WRITE_TOOL_NAMES = {"Edit", "Write", "MultiEdit"}
REVISION_ROOT = Path("docs") / "修订记录"


def load_module(script_name: str, module_name: str):
    """按相邻脚本路径加载模块。"""
    if module_name in sys.modules:
        return sys.modules[module_name]

    script_path = Path(__file__).resolve().with_name(script_name)
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块: {script_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


revision_index = load_module("revision_index_sync.py", "revision_index_sync")
revision_context = load_module("revision_context_sync.py", "revision_context_sync")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="修订记录自动同步 Hook")
    parser.add_argument("--project-dir", default="", help="项目根目录，可选")
    parser.add_argument("--force-path", default="", help="手动指定触发路径，调试时可用")
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
    """将目标路径解析为绝对路径。"""
    cleaned_text = path_text.strip()
    if not cleaned_text:
        return None
    target_path = Path(cleaned_text)
    if not target_path.is_absolute():
        target_path = (project_dir / target_path).resolve()
    else:
        target_path = target_path.resolve()
    return target_path


def is_revision_record_path(target_path: Path, project_dir: Path) -> bool:
    """判断目标路径是否位于修订记录目录下。"""
    try:
        relative_path = target_path.relative_to(project_dir)
    except ValueError:
        return False
    return relative_path.suffix.lower() == ".md" and relative_path.parts[:2] == REVISION_ROOT.parts


def detect_trigger_path(payload: dict, project_dir: Path, force_path_text: str) -> tuple[Path | None, str]:
    """识别是否应触发修订记录自动同步。"""
    if force_path_text.strip():
        target_path = resolve_target_path(force_path_text, project_dir)
        if target_path is None:
            return None, "未提供有效的 force-path"
        if is_revision_record_path(target_path, project_dir):
            return target_path, ""
        return None, "force-path 不在 docs/修订记录/ 下"

    if not payload:
        return None, "未收到 Hook payload"

    tool_name = extract_tool_name(payload)
    if tool_name and tool_name not in WRITE_TOOL_NAMES:
        return None, f"工具 {tool_name} 不属于写入类工具"

    target_path = resolve_target_path(extract_file_path(extract_tool_input(payload)), project_dir)
    if target_path is None:
        return None, "未识别到目标文件路径"
    if not is_revision_record_path(target_path, project_dir):
        return None, "目标文件不在 docs/修订记录/ 下"
    return target_path, ""


def run_sync(project_dir: Path) -> int:
    """执行修订记录索引与 AI 轨同步。"""
    index_exit_code = revision_index.main(["--project-dir", str(project_dir)])
    if index_exit_code != 0:
        return index_exit_code
    return revision_context.main(["--project-dir", str(project_dir)])


def main(argv: list[str] | None = None) -> int:
    """脚本入口。"""
    revision_index.configure_streams()
    args = parse_args(argv)
    project_dir = get_project_dir(args.project_dir)
    target_path, skip_reason = detect_trigger_path(load_payload(), project_dir, args.force_path)

    if target_path is None:
        print(f"[revision_auto_sync_hook] 跳过：{skip_reason}")
        return 0

    exit_code = run_sync(project_dir)
    if exit_code != 0:
        return exit_code

    print(f"[revision_auto_sync_hook] 已同步修订记录索引与 AI 轨：{target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
