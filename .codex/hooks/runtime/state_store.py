#!/usr/bin/env python3
"""基于 JSON 文件的 hooks 共享状态存储。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class HookStateStore:
    """管理 `.codex/hooks/state/runtime_state.json`。"""

    def __init__(self, project_dir: Path, state_path: Path | None = None) -> None:
        self.project_dir = project_dir.resolve()
        default_state_path = self.project_dir / ".codex" / "hooks" / "state" / "runtime_state.json"
        self.state_path = state_path.resolve() if state_path else default_state_path

    def load(self) -> dict[str, Any]:
        """读取状态文件。"""
        if not self.state_path.exists():
            return {}
        try:
            text = self.state_path.read_text(encoding="utf-8")
        except OSError:
            return {}
        if not text.strip():
            return {}
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return {}
        return data if isinstance(data, dict) else {}

    def save(self, data: dict[str, Any]) -> None:
        """原子写回状态文件。"""
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        self.state_path.write_text(payload, encoding="utf-8")

    def get_value(self, path_keys: list[str], default: Any = None) -> Any:
        """读取路径值。"""
        current: Any = self.load()
        for key_name in path_keys:
            if not isinstance(current, dict) or key_name not in current:
                return default
            current = current[key_name]
        return current

    def set_value(self, path_keys: list[str], value: Any) -> dict[str, Any]:
        """写入路径值。"""
        data = self.load()
        current = data
        for key_name in path_keys[:-1]:
            child_value = current.get(key_name)
            if not isinstance(child_value, dict):
                child_value = {}
                current[key_name] = child_value
            current = child_value
        current[path_keys[-1]] = value
        self.save(data)
        return data

    def increment_value(self, path_keys: list[str], step: int = 1) -> int:
        """递增整数值。"""
        current_value = self.get_value(path_keys, 0)
        if not isinstance(current_value, int):
            current_value = 0
        next_value = current_value + step
        self.set_value(path_keys, next_value)
        return next_value

    def append_recent_event(self, entry: dict[str, Any], limit: int = 20) -> list[dict[str, Any]]:
        """追加最近事件列表。"""
        recent_events = self.get_value(["runtime", "recent_events"], [])
        if not isinstance(recent_events, list):
            recent_events = []
        recent_events.append(entry)
        recent_events = recent_events[-limit:]
        self.set_value(["runtime", "recent_events"], recent_events)
        return recent_events
