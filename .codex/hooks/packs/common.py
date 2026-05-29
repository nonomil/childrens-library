#!/usr/bin/env python3
"""packs 共享工具。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.contracts import HookRequest, HookResult


EDIT_TOOL_NAMES = {"Edit", "Write", "MultiEdit"}
MODE_VALUES = {"observe", "warn", "enforce"}


def normalize_mode(mode_text: str) -> str:
    """规范化档位。"""
    mode = mode_text.strip().lower()
    return mode if mode in MODE_VALUES else "warn"


def build_mode_result(
    mode_text: str,
    message: str,
    *,
    enforce_action: str = "block",
    metadata: dict[str, Any] | None = None,
) -> HookResult:
    """按 observe / warn / enforce 生成结果。"""
    mode = normalize_mode(mode_text)
    details = metadata or {}
    if mode == "observe":
        return HookResult.noop(message, **details)
    if mode == "warn":
        return HookResult.context(message, **details)
    if enforce_action == "deny":
        return HookResult.deny(message, **details)
    return HookResult.block(message, **details)


def extract_command(request: HookRequest) -> str:
    """提取 Bash 命令文本。"""
    value = request.tool_input.get("command", "")
    return value.strip() if isinstance(value, str) else ""


def stringify_tool_response(request: HookRequest) -> str:
    """把 tool_response 规范化成文本。"""
    value = request.payload.get("tool_response", "")
    if isinstance(value, str):
        return value
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _extract_nested_path(value: object) -> str:
    if isinstance(value, dict):
        for key_name in ("file_path", "path", "target_file"):
            candidate = value.get(key_name)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        for child in value.values():
            candidate = _extract_nested_path(child)
            if candidate:
                return candidate
    if isinstance(value, list):
        for item in value:
            candidate = _extract_nested_path(item)
            if candidate:
                return candidate
    return ""


def extract_target_path(request: HookRequest) -> Path | None:
    """从 tool_input 中提取目标文件。"""
    target_text = _extract_nested_path(request.tool_input)
    if not target_text:
        return None
    target_path = Path(target_text)
    if target_path.is_absolute():
        return target_path.resolve()
    project_dir = request.project_dir or Path.cwd()
    return (project_dir / target_path).resolve()


def detect_exit_code(request: HookRequest) -> int | None:
    """尽量从 payload 中推断 exit code。"""
    for key_group in (
        ("exit_code",),
        ("tool_result", "exit_code"),
        ("tool_response", "exit_code"),
        ("metadata", "exit_code"),
    ):
        value = request.get_path(*key_group, default=None)
        if isinstance(value, int):
            return value

    response_text = stringify_tool_response(request).lower()
    if not response_text.strip():
        return None
    fail_markers = ("failed", "traceback", "error:", "syntaxerror", "exception")
    pass_markers = (" passed", "ok", "success", "通过")
    if any(marker in response_text for marker in fail_markers):
        return 1
    if any(marker in response_text for marker in pass_markers):
        return 0
    return None


def read_last_message(request: HookRequest) -> str:
    """读取 Stop 阶段消息。"""
    value = request.payload.get("last_assistant_message", "")
    return value if isinstance(value, str) else ""
