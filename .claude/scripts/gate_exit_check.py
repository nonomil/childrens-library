#!/usr/bin/env python3
"""Stop hook：任务结束时执行硬检查，但不阻塞退出。"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


LOG_PREFIX = "[gate_exit_check]"
GIT_TIMEOUT_SECONDS = 5
MAX_LISTED_FILES = 10


def configure_stderr() -> None:
    """将 stderr 调整为 UTF-8，避免 Windows 控制台输出告警符号失败。"""
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


def emit_message(message: str) -> None:
    """统一写入 stderr。

    Args:
        message: 待输出消息。
    """
    print(message, file=sys.stderr)


def get_project_dir() -> Path:
    """获取项目目录。

    Returns:
        当前项目根目录绝对路径。
    """
    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if project_dir_text:
        return Path(project_dir_text).resolve()
    return Path.cwd().resolve()


def run_git_command(
    project_dir: Path, *args: str
) -> subprocess.CompletedProcess[str] | None:
    """执行 git 命令。

    Args:
        project_dir: Git 仓库目录。
        *args: Git 参数列表。

    Returns:
        Git 命令结果；执行异常时返回 None。
    """
    try:
        return subprocess.run(
            ["git", "-c", "core.quotepath=false", *args],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (FileNotFoundError, OSError, subprocess.SubprocessError, ValueError) as exc:
        emit_message(
            f"{LOG_PREFIX} ⚠ Git 命令执行失败 ({' '.join(args)}): {exc}"
        )
        return None


def extract_status_paths(status_output: str) -> list[str]:
    """解析 `git status --short` 输出中的文件列表。

    Args:
        status_output: Git 状态原始输出。

    Returns:
        解析后的文件路径列表。
    """
    paths: list[str] = []
    for raw_line in status_output.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        path_text = line[3:].strip() if len(line) >= 3 else line.strip()
        if path_text:
            paths.append(path_text)
    return paths


def has_today_denied_entry(log_text: str, target_date: date) -> bool:
    """检查日志中是否存在当天门禁拦截记录。

    Args:
        log_text: 日志文本。
        target_date: 目标日期。

    Returns:
        若命中当天日期则返回 True。
    """
    date_tokens = {
        target_date.strftime("%Y-%m-%d"),
        target_date.strftime("%Y/%m/%d"),
        target_date.strftime("%Y.%m.%d"),
        target_date.strftime("%Y%m%d"),
    }
    return any(token in log_text for token in date_tokens)


def get_gate_files(project_dir: Path) -> list[Path]:
    """返回当前需要检查的 gate 文件列表。"""
    session_id = os.getenv("CLAUDE_SESSION_ID", "").strip()
    if not session_id:
        import platform as _platform
        host_name = _platform.node().strip() or "unknown-host"
        session_id = f"fallback-{host_name}-{os.getpid()}"
    gate_files: list[Path] = [
        project_dir
        / ".claude"
        / "state"
        / "runtime"
        / "sessions"
        / session_id
        / ".gate-approved",
        project_dir / ".claude" / "state" / ".gate-approved",
    ]
    return gate_files


def check_gate_approved_file(project_dir: Path) -> None:
    """检查 gate-approved 是否残留。

    Args:
        project_dir: 项目根目录。
    """
    try:
        remaining_files = [gate_file for gate_file in get_gate_files(project_dir) if gate_file.exists()]
        if remaining_files:
            joined_paths = ", ".join(str(path) for path in remaining_files)
            emit_message(
                f"{LOG_PREFIX} ⚠ gate-approved 仍存在，任务可能未完成清理流程: {joined_paths}"
            )
            return
        emit_message(f"{LOG_PREFIX} gate-approved 已清理")
    except Exception as exc:
        emit_message(f"{LOG_PREFIX} ⚠ gate-approved 检查失败: {exc}")


def check_uncommitted_changes(project_dir: Path) -> None:
    """检查未提交改动并输出摘要。

    Args:
        project_dir: 项目根目录。
    """
    try:
        status_result = run_git_command(project_dir, "status", "--short")
        diff_result = run_git_command(project_dir, "diff", "--stat")

        if status_result is None:
            emit_message(f"{LOG_PREFIX} ⚠ 未提交改动检查失败，请手动确认 Git 状态")
        elif status_result.returncode != 0:
            details = status_result.stderr.strip() or status_result.stdout.strip()
            emit_message(f"{LOG_PREFIX} ⚠ 未提交改动检查失败: {details or '未知错误'}")
        else:
            changed_paths = extract_status_paths(status_result.stdout)
            if changed_paths:
                emit_message(
                    f"{LOG_PREFIX} ⚠ 有 {len(changed_paths)} 个未提交文件，请确认是否需要提交"
                )
                for path_text in changed_paths[:MAX_LISTED_FILES]:
                    emit_message(f"{LOG_PREFIX} - {path_text}")
                if len(changed_paths) > MAX_LISTED_FILES:
                    emit_message(
                        f"{LOG_PREFIX} - 其余 {len(changed_paths) - MAX_LISTED_FILES} 个文件已省略"
                    )
            else:
                emit_message(f"{LOG_PREFIX} 工作区无未提交改动")

        if diff_result is None:
            emit_message(f"{LOG_PREFIX} ⚠ git diff --stat 获取失败，请手动确认差异摘要")
        elif diff_result.returncode != 0:
            details = diff_result.stderr.strip() or diff_result.stdout.strip()
            emit_message(
                f"{LOG_PREFIX} ⚠ git diff --stat 获取失败: {details or '未知错误'}"
            )
        else:
            diff_summary = diff_result.stdout.strip()
            if diff_summary:
                summary_line = diff_summary.splitlines()[-1].strip()
                emit_message(f"{LOG_PREFIX} git diff --stat: {summary_line}")
            else:
                emit_message(
                    f"{LOG_PREFIX} git diff --stat: 无已跟踪文件差异（可能仅有未跟踪文件）"
                )
    except Exception as exc:
        emit_message(f"{LOG_PREFIX} ⚠ 未提交改动检查执行异常: {exc}")


def check_denied_log(project_dir: Path) -> None:
    """检查当天是否存在门禁拦截日志。

    Args:
        project_dir: 项目根目录。
    """
    try:
        denied_log_file = project_dir / ".claude" / "state" / ".gate-denied-log"
        if not denied_log_file.exists():
            emit_message(f"{LOG_PREFIX} 本次会话未发现门禁拦截记录")
            return

        log_text = denied_log_file.read_text(encoding="utf-8", errors="replace")
        if has_today_denied_entry(log_text, datetime.now().date()):
            emit_message(
                f"{LOG_PREFIX} ⚠ 本次会话曾被门禁拦截，请确认教训已更新"
            )
            return
        emit_message(f"{LOG_PREFIX} 本次会话未发现门禁拦截记录")
    except Exception as exc:
        emit_message(f"{LOG_PREFIX} ⚠ 门禁拦截日志检查失败: {exc}")


def check_untracked_files(project_dir: Path) -> None:
    """检查未跟踪文件，提醒用户提交以避免丢失。

    Args:
        project_dir: 项目根目录。
    """
    try:
        result = run_git_command(
            project_dir, "ls-files", "--others", "--exclude-standard"
        )
        if result is None:
            emit_message(f"{LOG_PREFIX} ⚠ 未跟踪文件检查失败，请手动确认")
            return
        untracked = [line for line in result.stdout.strip().splitlines() if line.strip()]
        if not untracked:
            return
        emit_message(
            f"{LOG_PREFIX} ⚠ 发现 {len(untracked)} 个未跟踪文件，"
            "未 git add 将无法恢复："
        )
        for path_text in untracked[:MAX_LISTED_FILES]:
            emit_message(f"{LOG_PREFIX}   - {path_text}")
        if len(untracked) > MAX_LISTED_FILES:
            emit_message(
                f"{LOG_PREFIX}   - 其余 {len(untracked) - MAX_LISTED_FILES} 个文件已省略"
            )
    except Exception as exc:
        emit_message(f"{LOG_PREFIX} ⚠ 未跟踪文件检查异常: {exc}")


def main() -> int:
    """程序入口。

    Returns:
        始终返回 0，避免阻塞退出流程。
    """
    configure_stderr()

    try:
        project_dir = get_project_dir()
    except Exception as exc:
        emit_message(f"{LOG_PREFIX} ⚠ 项目目录解析失败: {exc}")
        project_dir = Path.cwd().resolve()

    checks = (
        ("gate-approved", check_gate_approved_file),
        ("git-status", check_uncommitted_changes),
        ("untracked-files", check_untracked_files),
        ("gate-denied-log", check_denied_log),
    )
    for check_name, check_func in checks:
        try:
            check_func(project_dir)
        except Exception as exc:
            emit_message(f"{LOG_PREFIX} ⚠ {check_name} 检查异常: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
