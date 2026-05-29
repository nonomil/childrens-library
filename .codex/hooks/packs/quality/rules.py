#!/usr/bin/env python3
"""quality pack 规则。"""

from __future__ import annotations

import py_compile
from datetime import datetime
from pathlib import Path

from packs.common import EDIT_TOOL_NAMES, build_mode_result, detect_exit_code, extract_command, extract_target_path
from runtime.contracts import HookEvent, HookRequest, HookResult
from runtime.dispatcher import DispatchRule
from runtime.state_store import HookStateStore


VERIFICATION_COMMAND_MARKERS = (
    "pytest",
    "python -m pytest",
    "python -m unittest",
    "python .codex/hooks/tests",
)


def _looks_like_verification_command(command_text: str) -> bool:
    normalized = command_text.strip().lower()
    return any(marker in normalized for marker in VERIFICATION_COMMAND_MARKERS)


def _record_verification_result(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.POST_TOOL_USE or request.tool_name != "Bash":
        return HookResult.noop()
    command_text = extract_command(request)
    if not _looks_like_verification_command(command_text):
        return HookResult.noop()

    exit_code = detect_exit_code(request)
    status = "unknown"
    if exit_code == 0:
        status = "passed"
    elif exit_code is not None:
        status = "failed"

    record = {
        "command": command_text,
        "status": status,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }
    store = HookStateStore(request.project_dir or Path.cwd())
    store.set_value(["runtime", "last_verification"], record)
    if request.session_id:
        store.set_value(["sessions", request.session_id, "last_verification"], record)

    if status == "failed":
        return build_mode_result(
            mode_text,
            f"最近一次验证命令失败：`{command_text}`。建议修复后再尝试提交。",
            enforce_action="block",
            metadata={"pack": "quality", "rule": "record_verification_result"},
        )
    return HookResult.noop(
        f"已记录验证结果：{status}",
        pack="quality",
        rule="record_verification_result",
    )


def _commit_gate(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.PRE_TOOL_USE or request.tool_name != "Bash":
        return HookResult.noop()
    command_text = extract_command(request).lower()
    if "git commit" not in command_text:
        return HookResult.noop()

    store = HookStateStore(request.project_dir or Path.cwd())
    verification = None
    if request.session_id:
        verification = store.get_value(["sessions", request.session_id, "last_verification"])
    if not isinstance(verification, dict):
        verification = store.get_value(["runtime", "last_verification"])

    if not isinstance(verification, dict):
        return build_mode_result(
            mode_text,
            "检测到 `git commit`，但当前没有最近一次验证通过记录。建议先运行测试或至少执行一次语法检查。",
            enforce_action="block",
            metadata={"pack": "quality", "rule": "commit_gate"},
        )

    if verification.get("status") != "passed":
        command_preview = str(verification.get("command", "")).strip() or "最近一次验证"
        return build_mode_result(
            mode_text,
            f"检测到 `git commit`，但 {command_preview} 的状态不是 passed。请修复失败项后再提交。",
            enforce_action="block",
            metadata={"pack": "quality", "rule": "commit_gate"},
        )

    return HookResult.noop(
        "最近一次验证已通过，允许继续提交。",
        pack="quality",
        rule="commit_gate",
    )


def _python_syntax_check(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.POST_TOOL_USE or request.tool_name not in EDIT_TOOL_NAMES:
        return HookResult.noop()
    target_path = extract_target_path(request)
    if target_path is None or target_path.suffix.lower() != ".py" or not target_path.exists():
        return HookResult.noop()

    try:
        py_compile.compile(str(target_path), doraise=True)
    except py_compile.PyCompileError as exc:
        return build_mode_result(
            mode_text,
            f"Python 语法检查失败：`{target_path.name}`\n{exc.msg}",
            enforce_action="block",
            metadata={"pack": "quality", "rule": "python_syntax_check"},
        )

    return HookResult.noop(
        f"Python 语法检查通过：{target_path.name}",
        pack="quality",
        rule="python_syntax_check",
    )


def build_quality_rules(mode_text: str = "warn") -> list[DispatchRule]:
    """构建 quality pack 规则。"""
    return [
        DispatchRule(
            priority=40,
            name="quality_commit_gate",
            events=(HookEvent.PRE_TOOL_USE,),
            handler=lambda request: _commit_gate(request, mode_text),
        ),
        DispatchRule(
            priority=50,
            name="quality_record_verification_result",
            events=(HookEvent.POST_TOOL_USE,),
            handler=lambda request: _record_verification_result(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=60,
            name="quality_python_syntax_check",
            events=(HookEvent.POST_TOOL_USE,),
            handler=lambda request: _python_syntax_check(request, mode_text),
            stop_on_action=False,
        ),
    ]
