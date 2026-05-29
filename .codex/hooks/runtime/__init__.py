"""Codex hooks 运行时公共导出。"""

from runtime.audit_log import AuditEntry, AuditLogger
from runtime.contracts import ActionMode, HookEvent, HookPlatform, HookRequest, HookResult
from runtime.dispatcher import DispatchOutcome, DispatchRule, HookRuntimeDispatcher
from runtime.platform_adapter import PlatformProfile, detect_platform, event_is_supported, normalize_event_name
from runtime.state_store import HookStateStore

__all__ = [
    "ActionMode",
    "AuditEntry",
    "AuditLogger",
    "DispatchOutcome",
    "DispatchRule",
    "HookEvent",
    "HookPlatform",
    "HookRequest",
    "HookResult",
    "HookRuntimeDispatcher",
    "HookStateStore",
    "PlatformProfile",
    "detect_platform",
    "event_is_supported",
    "normalize_event_name",
]
