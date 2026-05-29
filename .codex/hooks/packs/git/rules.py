#!/usr/bin/env python3
"""git pack 规则。"""

from __future__ import annotations

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from packs.common import EDIT_TOOL_NAMES, extract_command, extract_target_path, read_last_message
from packs.validate.rules import collect_stop_validation_issues, is_completion_message
from runtime.contracts import HookEvent, HookRequest, HookResult
from runtime.dispatcher import DispatchRule
from runtime.state_store import HookStateStore


PROTECTED_BRANCHES = {"main", "master", "production", "prod"}
SESSION_BRANCH_PREFIX = "codex/"
TRUTHY_VALUES = {"1", "true", "yes", "on", "enabled"}
DANGEROUS_GIT_MARKERS = (
    "git push --force",
    "git push -f",
    "git reset --hard",
    "git push origin main",
    "git push origin master",
)
AUTO_BRANCH_PAYLOAD_KEY = "git_auto_branch"
AUTO_COMMIT_PAYLOAD_KEY = "git_auto_commit"
AUTO_BRANCH_ENV_KEY = "HOOK_GIT_AUTO_BRANCH"
AUTO_COMMIT_ENV_KEY = "HOOK_GIT_AUTO_COMMIT"
INTERNAL_STATE_PREFIXES = (".codex/hooks/state/",)


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


def _current_branch(project_dir: Path) -> str:
    return _run_git(project_dir, ["branch", "--show-current"])[1].strip()


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


def _git_status_lines(project_dir: Path) -> list[str]:
    kept_lines: list[str] = []
    for raw_line in _run_git_status_lines(project_dir):
        path_text = raw_line[3:].strip() if len(raw_line) > 3 else raw_line.strip()
        if any(path_text.startswith(prefix) for prefix in INTERNAL_STATE_PREFIXES):
            continue
        kept_lines.append(raw_line)
    return kept_lines


def _is_protected_branch(branch_name: str) -> bool:
    return branch_name.strip().lower() in PROTECTED_BRANCHES


def _is_enabled(request: HookRequest, payload_key: str, env_key: str) -> bool:
    value = request.payload.get(payload_key, None)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in TRUTHY_VALUES
    env_value = os.environ.get(env_key, "")
    return env_value.strip().lower() in TRUTHY_VALUES


def _sanitize_branch_token(raw_text: str) -> str:
    normalized = re.sub(r"[^a-z0-9._-]+", "-", raw_text.strip().lower())
    return normalized.strip("-._")[:24]


def _build_session_branch_name(request: HookRequest) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    session_token = _sanitize_branch_token(request.session_id) or "session"
    return f"{SESSION_BRANCH_PREFIX}{timestamp}-{session_token}"


def _extract_completion_summary(last_message: str) -> str:
    if "已完成：" in last_message:
        return last_message.split("已完成：", maxsplit=1)[1].strip().splitlines()[0][:60]

    lines = [line.strip() for line in last_message.splitlines() if line.strip()]
    if not lines:
        return "update hooks flow"

    for index, line in enumerate(lines):
        if line == "## Result" and index + 1 < len(lines):
            return lines[index + 1][:60]
    return lines[0][:60]


def _build_auto_commit_message(last_message: str) -> str:
    summary = _extract_completion_summary(last_message).replace("`", "").strip() or "update hooks flow"
    return f"codex: stop checkpoint - {summary[:60]}"


def _record_git_state(
    project_dir: Path,
    request: HookRequest,
    state_key: str,
    payload: dict[str, object],
) -> None:
    store = HookStateStore(project_dir)
    store.set_value(["runtime", "git", state_key], payload)
    if request.session_id:
        store.set_value(["sessions", request.session_id, "git", state_key], payload)


def _session_branch_hint_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.SESSION_START:
        return HookResult.noop()
    project_dir = request.project_dir or Path.cwd()
    if not _is_git_repo(project_dir):
        return HookResult.noop()

    branch_name = _current_branch(project_dir)
    dirty_files = _run_git(project_dir, ["diff", "--name-only"])[1].strip()
    lines = [f"当前分支：{branch_name or 'unknown'}"]
    if dirty_files:
        preview = "\n".join(dirty_files.splitlines()[:8])
        lines.append("未提交修改：\n" + preview)
    if mode_text == "observe":
        return HookResult.noop("Git 会话提示已准备。", pack="git", rule="session_branch_hint_rule")
    return HookResult.context("\n\n".join(lines), pack="git", rule="session_branch_hint_rule")


def _session_branch_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.SESSION_START:
        return HookResult.noop()
    project_dir = request.project_dir or Path.cwd()
    if not _is_git_repo(project_dir):
        return HookResult.noop()

    base_branch = _current_branch(project_dir)
    if not _is_protected_branch(base_branch):
        return HookResult.noop()

    suggested_branch = _build_session_branch_name(request)
    status_lines = _git_status_lines(project_dir)
    branch_record = {
        "base_branch": base_branch,
        "suggested_branch": suggested_branch,
        "has_worktree_changes": bool(status_lines),
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }
    _record_git_state(project_dir, request, "last_session_branch_plan", branch_record)

    if mode_text == "observe":
        return HookResult.noop("Git 会话分支建议已记录。", pack="git", rule="session_branch_rule")

    if status_lines:
        preview = "\n".join(status_lines[:8])
        return HookResult.context(
            "当前在受保护分支上，且工作区已有改动，跳过自动切分支。"
            f"\n建议先检查改动，再手动执行：`git checkout -b {suggested_branch}`"
            f"\n当前工作区：\n{preview}",
            pack="git",
            rule="session_branch_rule",
        )

    if mode_text == "enforce" and _is_enabled(request, AUTO_BRANCH_PAYLOAD_KEY, AUTO_BRANCH_ENV_KEY):
        checkout_code, checkout_output = _run_git(project_dir, ["checkout", "-b", suggested_branch])
        if checkout_code == 0:
            branch_record["created_branch"] = suggested_branch
            branch_record["created_at"] = datetime.now().isoformat(timespec="seconds")
            _record_git_state(project_dir, request, "last_session_branch_plan", branch_record)
            return HookResult.context(
                f"已创建会话工作分支：`{suggested_branch}`。后续提交和 PR 草稿将基于该分支。",
                pack="git",
                rule="session_branch_rule",
            )
        return HookResult.context(
            f"尝试创建会话工作分支失败：{checkout_output or suggested_branch}",
            pack="git",
            rule="session_branch_rule",
        )

    return HookResult.context(
        "当前位于受保护分支，建议为本次会话切出独立分支："
        f"`git checkout -b {suggested_branch}`。若要自动创建，请显式开启 `git_auto_branch` 或 `{AUTO_BRANCH_ENV_KEY}=1`。",
        pack="git",
        rule="session_branch_rule",
    )


def _protect_main_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.PRE_TOOL_USE or request.tool_name != "Bash":
        return HookResult.noop()
    project_dir = request.project_dir or Path.cwd()
    if not _is_git_repo(project_dir):
        return HookResult.noop()

    command_text = extract_command(request).lower()
    if not any(marker in command_text for marker in DANGEROUS_GIT_MARKERS):
        return HookResult.noop()

    branch_name = _current_branch(project_dir).lower()
    mentions_protected_target = any(target in command_text for target in (" main", " master", " prod", " production"))
    if branch_name in PROTECTED_BRANCHES or mentions_protected_target:
        if mode_text == "observe":
            return HookResult.noop("检测到受保护分支风险。", pack="git", rule="protect_main_rule")
        return HookResult.deny(
            f"当前处于受保护分支 `{branch_name or 'unknown'}` 或命令直接指向受保护分支，已阻止危险 Git 操作。",
            pack="git",
            rule="protect_main_rule",
        )
    return HookResult.noop()


def _edit_snapshot_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.PRE_TOOL_USE or request.tool_name not in EDIT_TOOL_NAMES:
        return HookResult.noop()
    project_dir = request.project_dir or Path.cwd()
    if not _is_git_repo(project_dir):
        return HookResult.noop()

    target_path = extract_target_path(request)
    if target_path is None or not target_path.exists():
        return HookResult.noop()

    store = HookStateStore(project_dir)
    snapshot = {
        "file_path": str(target_path),
        "branch": _current_branch(project_dir),
        "dirty_files": _run_git(project_dir, ["diff", "--name-only"])[1].splitlines(),
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }
    store.set_value(["runtime", "git", "last_snapshot"], snapshot)
    if request.session_id:
        store.set_value(["sessions", request.session_id, "git", "last_snapshot"], snapshot)

    if mode_text == "observe":
        return HookResult.noop("Git 快照元数据已记录。", pack="git", rule="edit_snapshot_rule")
    return HookResult.context(
        f"已记录 Git 快照元数据：{target_path.name}",
        pack="git",
        rule="edit_snapshot_rule",
    )


def _auto_commit_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()
    if mode_text == "observe":
        return HookResult.noop("observe 模式跳过自动提交。", pack="git", rule="auto_commit_rule")

    last_message = read_last_message(request)
    if not is_completion_message(last_message):
        return HookResult.noop()

    project_dir = request.project_dir or Path.cwd()
    if not _is_git_repo(project_dir):
        return HookResult.noop()

    status_lines = _git_status_lines(project_dir)
    if not status_lines:
        return HookResult.noop()

    branch_name = _current_branch(project_dir)
    commit_message = _build_auto_commit_message(last_message)
    validation_issues = collect_stop_validation_issues(project_dir, request.session_id)
    skip_reasons: list[str] = []
    if _is_protected_branch(branch_name):
        skip_reasons.append(f"当前分支受保护：`{branch_name}`")
    if validation_issues:
        issue_preview = "\n".join(f"- {item}" for item in validation_issues[:4])
        skip_reasons.append(f"验证未通过：\n{issue_preview}")

    if skip_reasons:
        return HookResult.context(
            "已跳过 git 自动提交：\n" + "\n".join(skip_reasons),
            pack="git",
            rule="auto_commit_rule",
        )

    if mode_text != "enforce" or not _is_enabled(request, AUTO_COMMIT_PAYLOAD_KEY, AUTO_COMMIT_ENV_KEY):
        return HookResult.context(
            "检测到可提交改动，建议在独立分支上生成检查点提交："
            f"`git add -A && git commit -m \\\"{commit_message}\\\"`。"
            f"\n若要由 hook 自动执行，请显式开启 `git_auto_commit` 或 `{AUTO_COMMIT_ENV_KEY}=1`。",
            pack="git",
            rule="auto_commit_rule",
        )

    add_code, add_output = _run_git(
        project_dir,
        ["add", "-A", "--", ".", ":(exclude).codex/hooks/state", ":(exclude).codex/hooks/state/**"],
    )
    if add_code != 0:
        return HookResult.context(
            f"自动提交前暂存失败：{add_output}",
            pack="git",
            rule="auto_commit_rule",
        )

    commit_code, commit_output = _run_git(project_dir, ["commit", "-m", commit_message])
    if commit_code != 0:
        return HookResult.context(
            f"自动提交失败：{commit_output or commit_message}",
            pack="git",
            rule="auto_commit_rule",
        )

    commit_hash = _run_git(project_dir, ["rev-parse", "--short", "HEAD"])[1].strip()
    record = {
        "branch": branch_name,
        "commit_hash": commit_hash,
        "commit_message": commit_message,
        "file_count": len(status_lines),
        "recorded_at": datetime.now().isoformat(timespec="seconds"),
    }
    _record_git_state(project_dir, request, "last_auto_commit", record)
    return HookResult.context(
        f"已自动提交检查点：`{commit_message}` ({commit_hash})",
        pack="git",
        rule="auto_commit_rule",
    )


def _pr_draft_rule(request: HookRequest, mode_text: str) -> HookResult:
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()
    if mode_text == "observe":
        return HookResult.noop("observe 模式跳过 PR 草稿生成。", pack="git", rule="pr_draft_rule")

    last_message = read_last_message(request)
    if not is_completion_message(last_message):
        return HookResult.noop()

    project_dir = request.project_dir or Path.cwd()
    if not _is_git_repo(project_dir):
        return HookResult.noop()

    summary = last_message.strip().splitlines()[0][:120]
    branch_name = _current_branch(project_dir) or "unknown"
    changed_files = _run_git(project_dir, ["diff", "--name-only", "HEAD"])[1].strip()
    diff_stat = _run_git(project_dir, ["diff", "--stat", "HEAD"])[1].strip()

    draft_path = project_dir / ".codex" / "hooks" / "state" / "pr-draft.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text(
        "\n".join(
            [
                "# PR 描述草稿",
                "",
                f"- 分支：`{branch_name}`",
                f"- 摘要：{summary}",
                "",
                "## 涉及文件",
                "",
                changed_files or "_无未提交变更_",
                "",
                "## 变更统计",
                "",
                diff_stat or "_无 diff 统计_",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return HookResult.context(
        f"已生成 PR 草稿：`{draft_path}`",
        pack="git",
        rule="pr_draft_rule",
    )


def build_git_rules(mode_text: str = "warn") -> list[DispatchRule]:
    """构建 git pack 规则。"""
    return [
        DispatchRule(
            priority=32,
            name="git_protect_main_rule",
            events=(HookEvent.PRE_TOOL_USE,),
            handler=lambda request: _protect_main_rule(request, mode_text),
        ),
        DispatchRule(
            priority=33,
            name="git_edit_snapshot_rule",
            events=(HookEvent.PRE_TOOL_USE,),
            handler=lambda request: _edit_snapshot_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=64,
            name="git_session_branch_hint_rule",
            events=(HookEvent.SESSION_START,),
            handler=lambda request: _session_branch_hint_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=65,
            name="git_session_branch_rule",
            events=(HookEvent.SESSION_START,),
            handler=lambda request: _session_branch_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=85,
            name="git_pr_draft_rule",
            events=(HookEvent.STOP,),
            handler=lambda request: _pr_draft_rule(request, mode_text),
            stop_on_action=False,
        ),
        DispatchRule(
            priority=88,
            name="git_auto_commit_rule",
            events=(HookEvent.STOP,),
            handler=lambda request: _auto_commit_rule(request, mode_text),
            stop_on_action=False,
        ),
    ]
