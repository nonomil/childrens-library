#!/usr/bin/env python3
"""resilience pack 规则。"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path

from packs.common import build_mode_result, extract_command, read_last_message, stringify_tool_response
from runtime.contracts import HookEvent, HookRequest, HookResult
from runtime.dispatcher import DispatchRule
from runtime.state_store import HookStateStore


DONE_MARKERS = ("已完成：", "## Result")
RATE_LIMIT_MARKERS = ("429", "rate limit", "capacity", "too many requests", "访问量过大")
RG_COMMAND_PATTERN = re.compile(r"(^|\s)rg(?:\.exe)?(\s|$)")
PYTHON_COMMAND_PATTERN = re.compile(r"(^|\s)(py|python|python3|python\.exe)(\s|$)")
TILDE_CODEX_PATTERN = re.compile(r"~[\\/]\.codex[\\/]")
RECENT_FAILURE_REASON_CODES = {"rg_resource_unavailable", "python_launcher_unavailable"}
RG_FAILURE_MARKERS = (
    "resourceunavailable",
    "program 'rg.exe' failed to run",
    "rg.exe",
    "拒绝访问",
    "access denied",
)
PYTHON_LAUNCHER_FAILURE_MARKERS = (
    "no installed python found",
    "not recognized",
    "python.exe",
    "access is denied",
    "拒绝访问",
)
ENCODING_FAILURE_MARKERS = (
    "unicodedecodeerror",
    "'gbk' codec can't decode",
    "gbk codec can't decode",
    "default encoding",
)


def _is_windows_request(request: HookRequest) -> bool:
    for field_name in ("shell", "host_os", "os"):
        value = request.payload.get(field_name, "")
        if not isinstance(value, str):
            continue
        normalized = value.strip().lower()
        if "powershell" in normalized or "windows" in normalized or normalized == "pwsh":
            return True
    cwd_text = str(request.payload.get("cwd", "")).strip()
    if re.match(r"^[a-zA-Z]:[\\/]", cwd_text):
        return True
    return os.name == "nt"


def _load_recent_shell_failure(store: HookStateStore, session_id: str) -> dict[str, str] | None:
    record = None
    if session_id:
        record = store.get_value(["sessions", session_id, "resilience", "last_shell_failure"])
    if not isinstance(record, dict):
        record = store.get_value(["runtime", "last_shell_failure"])
    return record if isinstance(record, dict) else None


def _record_shell_failure(request: HookRequest, command_family: str, reason_code: str, summary: str) -> None:
    store = HookStateStore(request.project_dir or Path.cwd())
    record = {
        "command_family": command_family,
        "reason_code": reason_code,
        "command": extract_command(request),
        "summary": summary,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }
    store.set_value(["runtime", "last_shell_failure"], record)
    store.set_value(["runtime", "shell_failures", command_family], record)
    if request.session_id:
        store.set_value(["sessions", request.session_id, "resilience", "last_shell_failure"], record)


def _build_rg_fallback_message() -> str:
    return (
        "检测到 `rg.exe` 在当前 Windows 环境中启动失败。"
        "\n建议改用 PowerShell 原生命令："
        "\n`Get-ChildItem -LiteralPath 'docs' -Recurse -File`"
        "\n或"
        "\n`Get-ChildItem -LiteralPath 'docs' -Recurse -File | Select-String -Pattern 'keyword'`"
    )


def _build_python_fallback_message() -> str:
    return (
        "检测到当前 Windows 环境的 Python 启动链路不可用。"
        "\n请停止继续尝试 `python / py / python3`，优先改用："
        "\n`node -e \"const fs=require('fs'); console.log(fs.readFileSync('C:/path/file.md','utf8'))\"`"
        "\n或 PowerShell `Get-Content -Encoding UTF8`。"
    )


def _build_encoding_fallback_message() -> str:
    return (
        "检测到默认编码问题（GBK）。"
        "\n请改用显式 UTF-8 读取："
        "\n`node -e \"const fs=require('fs'); console.log(fs.readFileSync('C:/path/file.md','utf8'))\"`"
        "\n或 `Get-Content -LiteralPath 'C:\\path\\file.md' -Encoding UTF8`。"
    )


def _repeat_shell_failure_guard(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.PRE_TOOL_USE or request.tool_name != "Bash":
        return HookResult.noop()
    if not _is_windows_request(request):
        return HookResult.noop()

    command_text = extract_command(request)
    normalized_command = command_text.lower()
    if not normalized_command:
        return HookResult.noop()

    if TILDE_CODEX_PATTERN.search(command_text.replace("\\", "/")):
        return build_mode_result(
            mode_text,
            "Windows PowerShell 不会直接展开 `~/.codex/...`。"
            "\n请先运行 `node -e \"console.log(require('os').homedir())\"` 获取 home，"
            "\n再执行 `node <home>/.codex/...`。",
            enforce_action="deny",
            metadata={"pack": "resilience", "rule": "repeat_shell_failure_guard"},
        )

    store = HookStateStore(request.project_dir or Path.cwd())
    recent_failure = _load_recent_shell_failure(store, request.session_id)
    if not isinstance(recent_failure, dict):
        return HookResult.noop()

    reason_code = str(recent_failure.get("reason_code", "")).strip()
    command_family = str(recent_failure.get("command_family", "")).strip()
    if reason_code not in RECENT_FAILURE_REASON_CODES:
        return HookResult.noop()

    if command_family == "rg" and RG_COMMAND_PATTERN.search(normalized_command):
        return build_mode_result(
            mode_text,
            "当前会话已记录 `rg.exe` 启动失败，继续重试大概率仍会失败。"
            f"\n{_build_rg_fallback_message()}",
            enforce_action="deny",
            metadata={"pack": "resilience", "rule": "repeat_shell_failure_guard"},
        )

    if command_family == "python-launcher" and PYTHON_COMMAND_PATTERN.search(normalized_command):
        return build_mode_result(
            mode_text,
            "当前会话已记录 Python 启动器不可用，继续重试同类命令意义不大。"
            f"\n{_build_python_fallback_message()}",
            enforce_action="deny",
            metadata={"pack": "resilience", "rule": "repeat_shell_failure_guard"},
        )
    return HookResult.noop()


def _unfinished_stop_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()
    if request.stop_hook_active:
        return HookResult.noop("stop_hook_active=true，本轮跳过续跑。", pack="resilience", rule="unfinished_stop_rule")
    last_message = read_last_message(request)
    if any(marker in last_message for marker in DONE_MARKERS):
        return HookResult.noop("检测到完成标记。", pack="resilience", rule="unfinished_stop_rule")
    return build_mode_result(
        mode_text,
        "任务尚未显式完成。请继续执行未完成部分；全部完成后输出“已完成：[摘要]”或保留 `## Result` 收尾结构。",
        enforce_action="block",
        metadata={"pack": "resilience", "rule": "unfinished_stop_rule"},
    )


def _rate_limit_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.POST_TOOL_USE or request.tool_name != "Bash":
        return HookResult.noop()
    response_text = stringify_tool_response(request).lower()
    store = HookStateStore(request.project_dir or Path.cwd())
    retry_key = ["runtime", "retries", "rate_limit"]
    session_retry_key = ["sessions", request.session_id, "retries", "rate_limit"] if request.session_id else None

    if any(marker in response_text for marker in RATE_LIMIT_MARKERS):
        retry_count = store.increment_value(retry_key)
        if session_retry_key is not None:
            store.increment_value(session_retry_key)
        wait_seconds = min(60, 5 * (2 ** max(retry_count - 1, 0)))
        store.set_value(
            ["runtime", "last_rate_limit"],
            {
                "command": extract_command(request),
                "retry_count": retry_count,
                "suggest_wait_seconds": wait_seconds,
                "recorded_at": datetime.now().isoformat(timespec="seconds"),
            },
        )
        return build_mode_result(
            mode_text,
            f"检测到限流或容量不足（第 {retry_count} 次）。建议等待 {wait_seconds} 秒后重试最近一步。",
            enforce_action="block",
            metadata={"pack": "resilience", "rule": "rate_limit_rule"},
        )

    if store.get_value(retry_key, 0):
        store.set_value(retry_key, 0)
    if session_retry_key is not None and store.get_value(session_retry_key, 0):
        store.set_value(session_retry_key, 0)
    return HookResult.noop()


def _shell_failure_fallback_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.POST_TOOL_USE or request.tool_name != "Bash":
        return HookResult.noop()
    if not _is_windows_request(request):
        return HookResult.noop()

    command_text = extract_command(request).lower()
    response_text = stringify_tool_response(request).lower()
    if not command_text or not response_text:
        return HookResult.noop()

    if RG_COMMAND_PATTERN.search(command_text) and any(marker in response_text for marker in RG_FAILURE_MARKERS):
        _record_shell_failure(request, "rg", "rg_resource_unavailable", "rg.exe 启动失败")
        return build_mode_result(
            mode_text,
            _build_rg_fallback_message(),
            metadata={"pack": "resilience", "rule": "shell_failure_fallback_rule"},
        )

    if PYTHON_COMMAND_PATTERN.search(command_text) and any(
        marker in response_text for marker in PYTHON_LAUNCHER_FAILURE_MARKERS
    ):
        _record_shell_failure(request, "python-launcher", "python_launcher_unavailable", "Python 启动链路不可用")
        return build_mode_result(
            mode_text,
            _build_python_fallback_message(),
            metadata={"pack": "resilience", "rule": "shell_failure_fallback_rule"},
        )

    if any(marker in response_text for marker in ENCODING_FAILURE_MARKERS):
        _record_shell_failure(request, "encoding", "encoding_gbk_decode_failed", "默认编码导致 UTF-8 读取失败")
        return build_mode_result(
            mode_text,
            _build_encoding_fallback_message(),
            metadata={"pack": "resilience", "rule": "shell_failure_fallback_rule"},
        )
    return HookResult.noop()


def build_resilience_rules(mode_text: str = "warn") -> list[DispatchRule]:
    """构建 resilience pack 规则。"""
    return [
        DispatchRule(
            priority=68,
            name="resilience_repeat_shell_failure_guard",
            events=(HookEvent.PRE_TOOL_USE,),
            handler=lambda request: _repeat_shell_failure_guard(request, mode_text),
        ),
        DispatchRule(
            priority=70,
            name="resilience_rate_limit_rule",
            events=(HookEvent.POST_TOOL_USE,),
            handler=lambda request: _rate_limit_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=72,
            name="resilience_shell_failure_fallback_rule",
            events=(HookEvent.POST_TOOL_USE,),
            handler=lambda request: _shell_failure_fallback_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=80,
            name="resilience_unfinished_stop_rule",
            events=(HookEvent.STOP,),
            handler=lambda request: _unfinished_stop_rule(request, mode_text),
        ),
    ]
