#!/usr/bin/env python3
"""PreToolUse hook: 拦截 Codex 调用，强制要求门禁确认。"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

GATE_MAX_AGE_MINUTES = int(os.getenv("GATE_MAX_AGE_MINUTES", "120"))
INVALID_TASK_VALUES = {"", "test", "unknown", "未知任务", "TODO"}
INVALID_EXECUTOR_VALUES = {"", "unknown", "未指定", "TODO"}


def get_project_dir() -> Path:
    """获取项目目录。"""
    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if project_dir_text:
        return Path(project_dir_text).resolve()
    return Path.cwd().resolve()


def configure_stderr() -> None:
    """将 stderr 调整为 UTF-8，避免 Windows 控制台输出异常。"""
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


def block(message_text: str) -> int:
    """统一输出阻断信息并返回官方阻断码。"""
    print(message_text, file=sys.stderr)
    return 2


def load_gate_payload(gate_file: Path) -> dict:
    """读取 gate 文件内容。"""
    content_text = gate_file.read_text(encoding="utf-8")
    payload = json.loads(content_text)
    if not isinstance(payload, dict):
        raise ValueError("gate-approved 必须是 JSON 对象")
    return payload


def validate_gate_payload(payload: dict) -> None:
    """校验 gate 内容是否完整。"""
    task_desc = str(payload.get("task", "")).strip()
    executor = str(payload.get("executor", "")).strip()
    approved_at = str(payload.get("approved_at", "")).strip()

    if task_desc in INVALID_TASK_VALUES:
        raise ValueError(f"门禁任务描述无效: {task_desc or '<empty>'}")
    if executor in INVALID_EXECUTOR_VALUES:
        raise ValueError(f"门禁执行者无效: {executor or '<empty>'}")
    if not approved_at:
        raise ValueError("门禁缺少 approved_at 时间")

    # 仅验证 approved_at 格式合法，不做超时校验
    approved_at.replace("Z", "+00:00")
    datetime.fromisoformat(approved_at)


def get_session_gate_file(project_dir: Path) -> Path:
    """返回当前会话的门禁文件路径（含 deterministic fallback）。"""
    session_id = os.getenv("CLAUDE_SESSION_ID", "").strip()
    if not session_id:
        import platform as _platform
        host_name = _platform.node().strip() or "unknown-host"
        session_id = f"fallback-{host_name}-{os.getpid()}"
    return (
        project_dir
        / ".claude"
        / "state"
        / "runtime"
        / "sessions"
        / session_id
        / ".gate-approved"
    )


def get_gate_files(project_dir: Path) -> list[Path]:
    """返回按优先级排列的门禁文件列表。"""
    return [
        get_session_gate_file(project_dir),
        project_dir / ".claude" / "state" / ".gate-approved",
    ]


def main() -> int:
    """脚本入口。"""
    configure_stderr()

    try:
        sys.stdin.read()
    except Exception:
        pass

    project_dir = get_project_dir()
    for gate_file in get_gate_files(project_dir):
        if not gate_file.exists():
            continue
        try:
            payload = load_gate_payload(gate_file)
            validate_gate_payload(payload)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            return block(f"[gate_guard] 门禁文件无效，请修复 {gate_file}: {exc}")

        task_desc = str(payload.get("task", "")).strip()
        executor = str(payload.get("executor", "")).strip()
        print(f"[gate_guard] 门禁已通过: {executor} — {task_desc}", file=sys.stderr)
        return 0

    denied_log = project_dir / ".claude" / "state" / ".gate-denied-log"
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Codex 调用被拦截（无 gate-approved）\n"
        with denied_log.open("a", encoding="utf-8") as handle:
            handle.write(log_entry)
    except OSError:
        pass

    return block(
        "[gate_guard] 拦截 Codex 调用：未通过门禁确认。\n"
        "请先完成需求确认，并写入有效的 .claude/state/.gate-approved 后再重试。"
    )


if __name__ == "__main__":
    raise SystemExit(main())
