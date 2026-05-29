#!/usr/bin/env python3
"""context pack 规则。"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from packs.common import build_mode_result, read_last_message
from runtime.contracts import HookEvent, HookRequest, HookResult
from runtime.dispatcher import DispatchRule
from runtime.state_store import HookStateStore


PROMPT_CONTEXT_MARKERS = (
    "测试",
    "修复",
    "报错",
    "错误",
    "debug",
    "fix",
    "test",
    "continue",
    "继续",
)


def _progress_snapshot_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()

    last_message = read_last_message(request)
    if not last_message.strip():
        return HookResult.noop()

    summary_line = last_message.strip().splitlines()[0][:200]
    status = "done" if ("已完成：" in last_message or "## Result" in last_message) else "in_progress"
    snapshot = {
        "status": status,
        "summary": summary_line,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    store = HookStateStore(request.project_dir or Path.cwd())
    store.set_value(["runtime", "last_progress"], snapshot)
    if request.session_id:
        store.set_value(["sessions", request.session_id, "progress"], snapshot)

    if mode_text == "observe":
        return HookResult.noop("已记录进度快照。", pack="context", rule="progress_snapshot_rule")
    return HookResult.context(
        f"已记录当前任务进度：{status} / {summary_line}",
        pack="context",
        rule="progress_snapshot_rule",
    )


def _session_restore_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.SESSION_START:
        return HookResult.noop()

    store = HookStateStore(request.project_dir or Path.cwd())
    lines: list[str] = []
    cwd_text = request.payload.get("cwd", "")
    if isinstance(cwd_text, str) and cwd_text.strip():
        lines.append(f"当前工作目录：{cwd_text}")

    session_progress = None
    if request.session_id:
        session_progress = store.get_value(["sessions", request.session_id, "progress"])
    if not isinstance(session_progress, dict):
        session_progress = store.get_value(["runtime", "last_progress"])
    if isinstance(session_progress, dict):
        lines.append(
            "上次进度："
            f"{session_progress.get('status', 'unknown')} / {session_progress.get('summary', '')}"
        )

    verification = store.get_value(["runtime", "last_verification"])
    if isinstance(verification, dict):
        lines.append(
            "最近验证："
            f"{verification.get('status', 'unknown')} / {verification.get('command', '')}"
        )

    critical_file = (request.project_dir or Path.cwd()) / ".codex" / "hooks" / "context" / "critical-context.md"
    if critical_file.exists():
        lines.append("关键上下文：\n" + critical_file.read_text(encoding="utf-8")[:600].strip())

    if not lines:
        return HookResult.noop()
    if mode_text == "observe":
        return HookResult.noop("可恢复上下文已就绪。", pack="context", rule="session_restore_rule")
    prefix = "[Context 已压缩，恢复关键上下文]\n" if request.payload.get("matcher") == "compact" else ""
    return HookResult.context(prefix + "\n\n".join(lines), pack="context", rule="session_restore_rule")


def _prompt_context_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.USER_PROMPT_SUBMIT:
        return HookResult.noop()
    prompt_text = request.payload.get("prompt", "")
    if not isinstance(prompt_text, str) or not any(marker in prompt_text.lower() for marker in [m.lower() for m in PROMPT_CONTEXT_MARKERS]):
        return HookResult.noop()

    store = HookStateStore(request.project_dir or Path.cwd())
    lines: list[str] = []
    verification = store.get_value(["runtime", "last_verification"])
    if isinstance(verification, dict):
        lines.append(
            "最近验证状态："
            f"{verification.get('status', 'unknown')} / {verification.get('command', '')}"
        )
    last_rate_limit = store.get_value(["runtime", "last_rate_limit"])
    if isinstance(last_rate_limit, dict):
        lines.append(
            "最近限流记录："
            f"第 {last_rate_limit.get('retry_count', 0)} 次 / 建议等待 {last_rate_limit.get('suggest_wait_seconds', 0)} 秒"
        )
    last_progress = store.get_value(["runtime", "last_progress"])
    if isinstance(last_progress, dict):
        lines.append(
            "最近任务进度："
            f"{last_progress.get('status', 'unknown')} / {last_progress.get('summary', '')}"
        )

    if not lines:
        return HookResult.noop()
    if mode_text == "observe":
        return HookResult.noop("存在可注入上下文。", pack="context", rule="prompt_context_rule")
    return HookResult.context("\n".join(lines), pack="context", rule="prompt_context_rule")


def _cwd_changed_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.CWD_CHANGED:
        return HookResult.noop()
    cwd_text = request.payload.get("cwd", "")
    if not isinstance(cwd_text, str) or not cwd_text.strip():
        return HookResult.noop()

    cwd_path = Path(cwd_text)
    if not cwd_path.exists():
        return HookResult.noop()

    lines = [f"工作目录已切换至：{cwd_path}"]
    package_json = cwd_path / "package.json"
    if package_json.exists():
        try:
            package_data = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            package_data = {}
        name_text = package_data.get("name", "")
        if isinstance(name_text, str) and name_text.strip():
            lines.append(f"当前包：{name_text}")
        scripts = package_data.get("scripts", {})
        if isinstance(scripts, dict) and scripts:
            script_names = ", ".join(list(scripts.keys())[:5])
            lines.append(f"可用脚本：{script_names}")
    if (cwd_path / "pyproject.toml").exists():
        lines.append("检测到 Python 项目（存在 pyproject.toml）")
    if (cwd_path / ".env").exists():
        lines.append("检测到本目录存在 .env，请注意环境变量边界")

    if mode_text == "observe":
        return HookResult.noop("目录切换信息已记录。", pack="context", rule="cwd_changed_rule")
    return HookResult.context("\n".join(lines), pack="context", rule="cwd_changed_rule")


def build_context_rules(mode_text: str = "warn") -> list[DispatchRule]:
    """构建 context pack 规则。"""
    return [
        DispatchRule(
            priority=65,
            name="context_progress_snapshot_rule",
            events=(HookEvent.STOP,),
            handler=lambda request: _progress_snapshot_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=66,
            name="context_session_restore_rule",
            events=(HookEvent.SESSION_START,),
            handler=lambda request: _session_restore_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=67,
            name="context_prompt_context_rule",
            events=(HookEvent.USER_PROMPT_SUBMIT,),
            handler=lambda request: _prompt_context_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=68,
            name="context_cwd_changed_rule",
            events=(HookEvent.CWD_CHANGED,),
            handler=lambda request: _cwd_changed_rule(request, mode_text),
            stop_on_action=False,
        ),
    ]
