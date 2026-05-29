#!/usr/bin/env python3
"""hooks 审计日志写入器。"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AuditEntry:
    """单条审计记录。"""

    timestamp_utc: str
    platform: str
    event_name: str
    rule_name: str
    action: str
    elapsed_ms: int
    dry_run: bool
    session_id: str = ""
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def build(
        cls,
        *,
        platform: str,
        event_name: str,
        rule_name: str,
        action: str,
        elapsed_ms: int,
        dry_run: bool,
        session_id: str = "",
        message: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> "AuditEntry":
        return cls(
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            platform=platform,
            event_name=event_name,
            rule_name=rule_name,
            action=action,
            elapsed_ms=elapsed_ms,
            dry_run=dry_run,
            session_id=session_id,
            message=message,
            metadata=metadata or {},
        )


class AuditLogger:
    """管理 `.codex/hooks/state/audit.log.jsonl`。"""

    def __init__(self, project_dir: Path, log_path: Path | None = None) -> None:
        self.project_dir = project_dir.resolve()
        default_log_path = self.project_dir / ".codex" / "hooks" / "state" / "audit.log.jsonl"
        self.log_path = log_path.resolve() if log_path else default_log_path

    def append_entry(self, entry: AuditEntry) -> None:
        """追加 JSONL 审计记录。"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(asdict(entry), ensure_ascii=False, sort_keys=True)
        with self.log_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line)
            handle.write("\n")

    def read_recent(self, limit: int = 20) -> list[dict[str, Any]]:
        """读取最近若干条审计记录。"""
        if not self.log_path.exists():
            return []
        lines = self.log_path.read_text(encoding="utf-8").splitlines()
        result: list[dict[str, Any]] = []
        for line in lines[-limit:]:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                result.append(item)
        return result
