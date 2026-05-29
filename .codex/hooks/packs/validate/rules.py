#!/usr/bin/env python3
"""validate pack 规则。"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from packs.common import build_mode_result, read_last_message
from runtime.contracts import HookEvent, HookRequest, HookResult
from runtime.dispatcher import DispatchRule
from runtime.state_store import HookStateStore


SOURCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp"}
DONE_MARKERS = ("已完成：", "## Result")
IGNORED_PATH_PREFIXES = (".codex/hooks/state/",)
LEFTOVER_PATTERNS = (
    (re.compile(r"\bTODO\b", re.IGNORECASE), "TODO"),
    (re.compile(r"\bFIXME\b", re.IGNORECASE), "FIXME"),
    (re.compile(r"console\.log\s*\("), "console.log"),
)


def _run_git(project_dir: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    return result.returncode, output


def _is_git_repo(project_dir: Path) -> bool:
    return _run_git(project_dir, ["rev-parse", "--is-inside-work-tree"])[0] == 0


def _run_git_status_lines(project_dir: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def _collect_changed_files(project_dir: Path) -> list[Path]:
    if not _is_git_repo(project_dir):
        return []
    paths: list[Path] = []
    seen_paths: set[Path] = set()
    for raw_line in _run_git_status_lines(project_dir):
        if len(raw_line) < 4:
            continue
        path_text = raw_line[3:].strip()
        if " -> " in path_text:
            path_text = path_text.split(" -> ", maxsplit=1)[1].strip()
        if not path_text or any(path_text.startswith(prefix) for prefix in IGNORED_PATH_PREFIXES):
            continue
        path = (project_dir / path_text).resolve()
        if path.exists() and path not in seen_paths:
            seen_paths.add(path)
            paths.append(path)
    return paths


def is_completion_message(last_message: str) -> bool:
    """判断 Stop 消息是否包含完成标记。"""
    return any(marker in last_message for marker in DONE_MARKERS)


def _load_last_verification(project_dir: Path, session_id: str) -> dict[str, str] | None:
    store = HookStateStore(project_dir)
    verification = None
    if session_id:
        verification = store.get_value(["sessions", session_id, "last_verification"])
    if not isinstance(verification, dict):
        verification = store.get_value(["runtime", "last_verification"])
    return verification if isinstance(verification, dict) else None


def collect_stop_validation_issues(project_dir: Path, session_id: str = "") -> list[str]:
    """收集 Stop 阶段会阻止验收的验证问题。"""
    issues: list[str] = []
    verification = _load_last_verification(project_dir, session_id)

    if isinstance(verification, dict):
        if verification.get("status") != "passed":
            issues.append(
                "最近一次验证结果不是 passed："
                f"{verification.get('status', 'unknown')} / {verification.get('command', '')}"
            )
    else:
        issues.append("没有最近一次验证结果记录。")

    for file_path in _collect_changed_files(project_dir):
        if file_path.suffix.lower() not in SOURCE_SUFFIXES:
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except OSError:
            continue
        for pattern, label in LEFTOVER_PATTERNS:
            if pattern.search(text):
                issues.append(f"{file_path.name} 中存在遗留标记：{label}")
                break
    return issues


def _validate_stop_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()
    last_message = read_last_message(request)
    if not is_completion_message(last_message):
        return HookResult.noop()

    project_dir = request.project_dir or Path.cwd()
    issues = collect_stop_validation_issues(project_dir, request.session_id)

    if not issues:
        return HookResult.context(
            "验证摘要：最近验证已通过，且未发现常见遗留标记。",
            pack="validate",
            rule="validate_stop_rule",
        )

    return build_mode_result(
        mode_text,
        "验证未通过：\n- " + "\n- ".join(issues),
        enforce_action="block",
        metadata={"pack": "validate", "rule": "validate_stop_rule"},
    )


def build_validate_rules(mode_text: str = "warn") -> list[DispatchRule]:
    """构建 validate pack 规则。"""
    return [
        DispatchRule(
            priority=87,
            name="validate_stop_rule",
            events=(HookEvent.STOP,),
            handler=lambda request: _validate_stop_rule(request, mode_text),
            stop_on_action=False,
        ),
    ]
