#!/usr/bin/env python3
"""平台探测与事件兼容适配。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from runtime.contracts import HookEvent, HookPlatform


@dataclass(frozen=True, slots=True)
class PlatformProfile:
    """平台能力画像。"""

    platform: HookPlatform
    supported_events: tuple[HookEvent, ...]
    supports_prompt_hook: bool
    supports_agent_hook: bool
    notes: tuple[str, ...]


PLATFORM_PROFILES: dict[HookPlatform, PlatformProfile] = {
    HookPlatform.CLAUDE: PlatformProfile(
        platform=HookPlatform.CLAUDE,
        supported_events=(
            HookEvent.PRE_TOOL_USE,
            HookEvent.POST_TOOL_USE,
            HookEvent.STOP,
            HookEvent.SESSION_START,
            HookEvent.USER_PROMPT_SUBMIT,
            HookEvent.PERMISSION_REQUEST,
            HookEvent.CWD_CHANGED,
            HookEvent.NOTIFICATION,
        ),
        supports_prompt_hook=True,
        supports_agent_hook=True,
        notes=(
            "Claude 原生事件矩阵最完整，可承接 Prompt Hook 与 Agent Hook。",
            "适合先启用 observe，再逐步升级 warn / enforce。",
        ),
    ),
    HookPlatform.CODEX: PlatformProfile(
        platform=HookPlatform.CODEX,
        supported_events=(
            HookEvent.PRE_TOOL_USE,
            HookEvent.POST_TOOL_USE,
            HookEvent.STOP,
        ),
        supports_prompt_hook=False,
        supports_agent_hook=False,
        notes=(
            "Codex 建议优先从 Stop、PostToolUse 和命令式验证落地。",
            "Prompt / Agent validator 默认需要降级为脚本式验证。",
        ),
    ),
    HookPlatform.UNKNOWN: PlatformProfile(
        platform=HookPlatform.UNKNOWN,
        supported_events=tuple(event for event in HookEvent),
        supports_prompt_hook=False,
        supports_agent_hook=False,
        notes=("未知平台，建议只启用 observe 模式。",),
    ),
}


def normalize_event_name(event_name_text: str) -> HookEvent:
    """把输入文本规范为统一事件名。"""
    normalized = event_name_text.strip().lower().replace("-", "").replace("_", "")
    mapping = {
        "pretooluse": HookEvent.PRE_TOOL_USE,
        "posttooluse": HookEvent.POST_TOOL_USE,
        "stop": HookEvent.STOP,
        "sessionstart": HookEvent.SESSION_START,
        "userpromptsubmit": HookEvent.USER_PROMPT_SUBMIT,
        "permissionrequest": HookEvent.PERMISSION_REQUEST,
        "cwdchanged": HookEvent.CWD_CHANGED,
        "notification": HookEvent.NOTIFICATION,
    }
    if normalized not in mapping:
        raise ValueError(f"未知事件: {event_name_text}")
    return mapping[normalized]


def get_platform_profile(platform: HookPlatform) -> PlatformProfile:
    """读取平台画像。"""
    return PLATFORM_PROFILES.get(platform, PLATFORM_PROFILES[HookPlatform.UNKNOWN])


def event_is_supported(platform: HookPlatform, event_name: HookEvent) -> bool:
    """判断事件是否受平台支持。"""
    return event_name in get_platform_profile(platform).supported_events


def detect_platform(project_dir: Path, env: dict[str, str] | None = None) -> HookPlatform:
    """根据环境变量和目录结构推断当前平台。"""
    env_map = env if env is not None else os.environ
    override = env_map.get("HOOK_RUNTIME_PLATFORM", "").strip().lower()
    if override == HookPlatform.CLAUDE.value:
        return HookPlatform.CLAUDE
    if override == HookPlatform.CODEX.value:
        return HookPlatform.CODEX

    if (project_dir / ".codex" / "hooks").exists() or (project_dir / ".codex" / "hooks.json").exists():
        return HookPlatform.CODEX
    if (project_dir / ".claude" / "settings.json").exists():
        return HookPlatform.CLAUDE
    return HookPlatform.UNKNOWN
