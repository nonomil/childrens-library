#!/usr/bin/env python3
"""notify pack 规则。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from packs.common import read_last_message
from runtime.contracts import HookEvent, HookRequest, HookResult
from runtime.dispatcher import DispatchRule
from runtime.state_store import HookStateStore


NOTIFICATION_LABELS = {
    "permissionprompt": "需要授权操作",
    "idleprompt": "等待用户输入",
    "authsuccess": "认证成功",
    "elicitationdialog": "需要用户决策",
}


def _notification_event_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.NOTIFICATION:
        return HookResult.noop()
    notification_type = str(request.payload.get("notification_type", "")).strip().lower()
    if not notification_type:
        return HookResult.noop()

    label = NOTIFICATION_LABELS.get(notification_type, "有新的通知事件")
    cwd_text = str(request.payload.get("cwd", "")).strip()
    message = f"Notification 事件：{label}" + (f" / {cwd_text}" if cwd_text else "")
    if mode_text == "observe":
        return HookResult.noop(message, pack="notify", rule="notification_event_rule")
    return HookResult.context(message, pack="notify", rule="notification_event_rule")


def _session_timer_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.SESSION_START:
        return HookResult.noop()
    session_id = request.session_id
    if not session_id:
        return HookResult.noop()

    store = HookStateStore(request.project_dir or Path.cwd())
    store.set_value(
        ["sessions", session_id, "notify", "started_at"],
        datetime.now().isoformat(timespec="seconds"),
    )
    if mode_text == "observe":
        return HookResult.noop("已记录会话开始时间。", pack="notify", rule="session_timer_rule")
    return HookResult.context("已记录本次会话开始时间。", pack="notify", rule="session_timer_rule")


def _stop_notify_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()

    last_message = read_last_message(request)
    if "已完成：" not in last_message and "## Result" not in last_message:
        return HookResult.noop()

    store = HookStateStore(request.project_dir or Path.cwd())
    started_at = None
    if request.session_id:
        started_at = store.get_value(["sessions", request.session_id, "notify", "started_at"])
    elapsed_text = ""
    if isinstance(started_at, str) and started_at.strip():
        try:
            start_time = datetime.fromisoformat(started_at)
            delta = datetime.now() - start_time
            total_seconds = int(delta.total_seconds())
            elapsed_text = f"{total_seconds // 60}分{total_seconds % 60}秒"
        except ValueError:
            elapsed_text = ""

    summary_line = last_message.strip().splitlines()[0][:120]
    notification_record = {
        "summary": summary_line,
        "elapsed": elapsed_text,
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }
    store.set_value(["runtime", "notify", "last_completion"], notification_record)
    if request.session_id:
        store.set_value(["sessions", request.session_id, "notify", "last_completion"], notification_record)

    message = f"通知摘要：任务已完成。{summary_line}"
    if elapsed_text:
        message += f" 用时 {elapsed_text}。"
    if mode_text == "observe":
        return HookResult.noop(message, pack="notify", rule="stop_notify_rule")
    return HookResult.context(message, pack="notify", rule="stop_notify_rule")


def build_notify_rules(mode_text: str = "warn") -> list[DispatchRule]:
    """构建 notify pack 规则。"""
    return [
        DispatchRule(
            priority=61,
            name="notify_session_timer_rule",
            events=(HookEvent.SESSION_START,),
            handler=lambda request: _session_timer_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=62,
            name="notify_notification_event_rule",
            events=(HookEvent.NOTIFICATION,),
            handler=lambda request: _notification_event_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=86,
            name="notify_stop_notify_rule",
            events=(HookEvent.STOP,),
            handler=lambda request: _stop_notify_rule(request, mode_text),
            stop_on_action=False,
        ),
    ]
