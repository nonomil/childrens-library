#!/usr/bin/env python3
"""hooks 运行时的统一数据契约。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class HookEvent(str, Enum):
    """统一事件名。"""

    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    STOP = "Stop"
    SESSION_START = "SessionStart"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    PERMISSION_REQUEST = "PermissionRequest"
    CWD_CHANGED = "CwdChanged"
    NOTIFICATION = "Notification"


class HookPlatform(str, Enum):
    """支持的平台枚举。"""

    CLAUDE = "claude"
    CODEX = "codex"
    UNKNOWN = "unknown"


class ActionMode(str, Enum):
    """统一动作语义。"""

    NOOP = "noop"
    CONTEXT = "context"
    BLOCK = "block"
    DENY = "deny"
    ALLOW = "allow"


TERMINAL_ACTIONS = {ActionMode.BLOCK, ActionMode.DENY, ActionMode.ALLOW}


@dataclass(slots=True)
class HookRequest:
    """统一输入请求。"""

    event_name: HookEvent
    platform: HookPlatform
    payload: dict[str, Any] = field(default_factory=dict)
    project_dir: Path | None = None
    dry_run: bool = False

    @property
    def session_id(self) -> str:
        value = self.payload.get("session_id", "")
        return value.strip() if isinstance(value, str) else ""

    @property
    def stop_hook_active(self) -> bool:
        return bool(self.payload.get("stop_hook_active", False))

    @property
    def tool_name(self) -> str:
        value = self.payload.get("tool_name", "")
        return value.strip() if isinstance(value, str) else ""

    @property
    def tool_input(self) -> dict[str, Any]:
        value = self.payload.get("tool_input", {})
        return value if isinstance(value, dict) else {}

    def get_path(self, *keys: str, default: Any = None) -> Any:
        """按路径读取嵌套字段。"""
        current: Any = self.payload
        for key_name in keys:
            if not isinstance(current, dict) or key_name not in current:
                return default
            current = current[key_name]
        return current


@dataclass(slots=True)
class HookResult:
    """统一输出结果。"""

    action: ActionMode = ActionMode.NOOP
    message: str = ""
    additional_context: str = ""
    updated_input: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def noop(cls, message: str = "", **metadata: Any) -> "HookResult":
        return cls(action=ActionMode.NOOP, message=message, metadata=dict(metadata))

    @classmethod
    def context(cls, text: str, **metadata: Any) -> "HookResult":
        return cls(action=ActionMode.CONTEXT, additional_context=text, metadata=dict(metadata))

    @classmethod
    def block(cls, reason: str, **metadata: Any) -> "HookResult":
        return cls(action=ActionMode.BLOCK, message=reason, metadata=dict(metadata))

    @classmethod
    def deny(cls, reason: str, **metadata: Any) -> "HookResult":
        return cls(action=ActionMode.DENY, message=reason, metadata=dict(metadata))

    @classmethod
    def allow(
        cls,
        updated_input: dict[str, Any] | None = None,
        message: str = "",
        **metadata: Any,
    ) -> "HookResult":
        return cls(
            action=ActionMode.ALLOW,
            message=message,
            updated_input=updated_input,
            metadata=dict(metadata),
        )


@dataclass(slots=True)
class DispatchRecord:
    """单条规则执行记录。"""

    rule_name: str
    result: HookResult
    elapsed_ms: int


@dataclass(slots=True)
class DispatchOutcome:
    """一次调度的聚合结果。"""

    request: HookRequest
    records: list[DispatchRecord] = field(default_factory=list)

    def add_record(self, rule_name: str, result: HookResult, elapsed_ms: int) -> None:
        self.records.append(DispatchRecord(rule_name=rule_name, result=result, elapsed_ms=elapsed_ms))

    def _action_rank(self, action: ActionMode) -> int:
        return {
            ActionMode.NOOP: 0,
            ActionMode.CONTEXT: 1,
            ActionMode.ALLOW: 2,
            ActionMode.BLOCK: 3,
            ActionMode.DENY: 4,
        }[action]

    def get_primary_record(self) -> DispatchRecord | None:
        if not self.records:
            return None
        return max(self.records, key=lambda item: self._action_rank(item.result.action))

    def collect_context_messages(self) -> list[str]:
        messages: list[str] = []
        for record in self.records:
            text = record.result.additional_context.strip()
            if text:
                messages.append(text)
        return messages

    def collect_action_messages(self, action: ActionMode) -> list[str]:
        messages: list[str] = []
        for record in self.records:
            if record.result.action != action:
                continue
            text = record.result.message.strip()
            if text:
                messages.append(text)
        return messages

    def to_payload(self) -> dict[str, Any]:
        """把聚合结果转成 hook 可消费的 JSON 结构。"""
        if not self.records:
            return {}

        if self.request.dry_run:
            dry_run_lines: list[str] = []
            for record in self.records:
                result = record.result
                if result.action == ActionMode.NOOP:
                    continue
                summary = result.message.strip() or result.additional_context.strip() or "无摘要"
                dry_run_lines.append(
                    f"[dry-run][{record.rule_name}] {result.action.value}: {summary}"
                )
            if not dry_run_lines:
                return {}
            return {
                "hookSpecificOutput": {
                    "hookEventName": self.request.event_name.value,
                    "additionalContext": "\n".join(dry_run_lines),
                }
            }

        primary_record = self.get_primary_record()
        if primary_record is None:
            return {}

        primary_result = primary_record.result
        context_text = "\n\n".join(self.collect_context_messages()).strip()

        if primary_result.action == ActionMode.BLOCK:
            reasons = self.collect_action_messages(ActionMode.BLOCK)
            if context_text:
                reasons.append(context_text)
            return {
                "decision": "block",
                "reason": "\n\n".join(part for part in reasons if part),
            }

        hook_specific_output: dict[str, Any] = {
            "hookEventName": self.request.event_name.value,
        }

        if primary_result.action == ActionMode.DENY:
            reasons = self.collect_action_messages(ActionMode.DENY)
            hook_specific_output["permissionDecision"] = "deny"
            hook_specific_output["permissionDecisionReason"] = "\n\n".join(
                part for part in reasons if part
            )
        elif primary_result.action == ActionMode.ALLOW:
            hook_specific_output["decision"] = {
                "behavior": "allow",
                "updatedInput": primary_result.updated_input or self.request.tool_input,
            }
            if primary_result.message.strip():
                context_text = (
                    f"{context_text}\n\n{primary_result.message.strip()}".strip()
                    if context_text
                    else primary_result.message.strip()
                )
        elif primary_result.action == ActionMode.CONTEXT:
            context_text = (
                f"{context_text}\n\n{primary_result.additional_context.strip()}".strip()
                if context_text and primary_result.additional_context.strip() not in context_text
                else context_text or primary_result.additional_context.strip()
            )

        if context_text:
            hook_specific_output["additionalContext"] = context_text

        return {"hookSpecificOutput": hook_specific_output}
