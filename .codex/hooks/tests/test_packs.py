from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
import subprocess
from unittest.mock import patch


HOOK_ROOT = Path(__file__).resolve().parents[1]
if str(HOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(HOOK_ROOT))

from packs.context.rules import build_context_rules
from packs.git.rules import build_git_rules
from packs.notify.rules import build_notify_rules
from packs.quality.rules import build_quality_rules
from packs.resilience.rules import build_resilience_rules
from packs.security.rules import build_security_rules
from packs.validate.rules import build_validate_rules
from runtime.contracts import HookEvent, HookPlatform, HookRequest
from runtime.dispatcher import HookRuntimeDispatcher, build_runtime_dispatcher
from runtime.state_store import HookStateStore


FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"


def load_fixture(name: str) -> dict:
    """读取 fixture。"""
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class PackRulesTest(unittest.TestCase):
    def test_security_pack_denies_dangerous_command(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_security_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PRE_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload=load_fixture("pretool-dangerous-bash.json"),
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertIn("危险命令模式", payload["hookSpecificOutput"]["permissionDecisionReason"])

    def test_resilience_pack_blocks_incomplete_stop(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload=load_fixture("stop-incomplete.json"),
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["decision"], "block")
            self.assertIn("任务尚未显式完成", payload["reason"])

    def test_resilience_pack_records_rate_limit_retry_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("warn"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.POST_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload=load_fixture("posttool-rate-limit.json"),
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertIn("限流或容量不足", payload["hookSpecificOutput"]["additionalContext"])
            store = HookStateStore(project_dir)
            self.assertEqual(store.get_value(["runtime", "retries", "rate_limit"]), 1)
            self.assertEqual(
                store.get_value(["sessions", "fixture-session", "retries", "rate_limit"]),
                1,
            )

    def test_resilience_pack_records_rg_fallback_and_suggests_powershell(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("warn"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.POST_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={
                        "session_id": "shell-session",
                        "shell": "powershell",
                        "tool_name": "Bash",
                        "tool_input": {"command": 'rg --files "docs"'},
                        "tool_response": (
                            "ResourceUnavailable:\n"
                            "Program 'rg.exe' failed to run: access denied.\n"
                            "拒绝访问。"
                        ),
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertIn("Get-ChildItem", payload["hookSpecificOutput"]["additionalContext"])
            store = HookStateStore(project_dir)
            self.assertEqual(
                store.get_value(["sessions", "shell-session", "resilience", "last_shell_failure", "command_family"]),
                "rg",
            )

    def test_resilience_pack_denies_repeat_rg_when_failure_was_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            store = HookStateStore(project_dir)
            store.set_value(
                ["runtime", "last_shell_failure"],
                {"command_family": "rg", "reason_code": "rg_resource_unavailable"},
            )

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PRE_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={
                        "shell": "powershell",
                        "tool_name": "Bash",
                        "tool_input": {"command": 'rg --files "docs"'},
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertIn("Get-ChildItem", payload["hookSpecificOutput"]["permissionDecisionReason"])

    def test_resilience_pack_blocks_tilde_codex_path_on_windows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PRE_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={
                        "shell": "powershell",
                        "tool_name": "Bash",
                        "tool_input": {
                            "command": "~/.codex/superpowers/.codex/superpowers-codex bootstrap"
                        },
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertIn("node -e", payload["hookSpecificOutput"]["permissionDecisionReason"])

    def test_resilience_pack_suggests_node_when_python_launcher_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("warn"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.POST_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={
                        "shell": "powershell",
                        "tool_name": "Bash",
                        "tool_input": {"command": "py -3 script.py"},
                        "tool_response": "No installed Python found",
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertIn("node -e", payload["hookSpecificOutput"]["additionalContext"])

    def test_resilience_pack_suggests_utf8_when_gbk_decode_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_resilience_rules("warn"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.POST_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={
                        "shell": "powershell",
                        "tool_name": "Bash",
                        "tool_input": {"command": "python scan.py"},
                        "tool_response": "UnicodeDecodeError: 'gbk' codec can't decode byte 0xff",
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertIn("UTF-8", payload["hookSpecificOutput"]["additionalContext"])

    def test_quality_pack_blocks_commit_without_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = HookRuntimeDispatcher(project_dir)
            for rule in build_quality_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PRE_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={
                        "tool_name": "Bash",
                        "tool_input": {"command": "git commit -m \"demo\""},
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["decision"], "block")
            self.assertIn("没有最近一次验证通过记录", payload["reason"])

    def test_quality_pack_warns_on_python_syntax_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            bad_file = project_dir / "broken.py"
            bad_file.write_text("def broken(:\n    pass\n", encoding="utf-8")

            dispatcher = HookRuntimeDispatcher(project_dir)
            for rule in build_quality_rules("warn"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.POST_TOOL_USE,
                    platform=HookPlatform.CLAUDE,
                    payload={
                        "tool_name": "Write",
                        "tool_input": {"file_path": str(bad_file)},
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "PostToolUse")
            self.assertIn("Python 语法检查失败", payload["hookSpecificOutput"]["additionalContext"])

    def test_context_pack_restores_progress_and_prompt_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_context_rules("warn"):
                dispatcher.register_rule(rule)

            dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CLAUDE,
                    payload={"last_assistant_message": "处理中：修复 hooks 边界问题", "session_id": "context-session"},
                    project_dir=project_dir,
                )
            )

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.SESSION_START,
                    platform=HookPlatform.CLAUDE,
                    payload=load_fixture("session-start-compact.json"),
                    project_dir=project_dir,
                )
            )
            payload = outcome.to_payload()
            self.assertIn("上次进度", payload["hookSpecificOutput"]["additionalContext"])

            store = HookStateStore(project_dir)
            store.set_value(
                ["runtime", "last_verification"],
                {"status": "failed", "command": "pytest tests/test_demo.py"},
            )
            prompt_outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.USER_PROMPT_SUBMIT,
                    platform=HookPlatform.CLAUDE,
                    payload=load_fixture("user-prompt-fix-tests.json"),
                    project_dir=project_dir,
                )
            )
            prompt_payload = prompt_outcome.to_payload()
            self.assertIn("最近验证状态", prompt_payload["hookSpecificOutput"]["additionalContext"])

    def test_git_pack_protects_main_and_writes_pr_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            (project_dir / "README.md").write_text("# demo\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "README.md"])
            self._run_git(project_dir, ["commit", "-m", "init"])
            (project_dir / "README.md").write_text("# demo\n\nchange\n", encoding="utf-8")

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("warn"):
                dispatcher.register_rule(rule)
            for rule in build_git_rules("enforce"):
                if rule.name == "git_protect_main_rule":
                    dispatcher.register_rule(rule)

            protect_outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PRE_TOOL_USE,
                    platform=HookPlatform.CODEX,
                    payload={"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}},
                    project_dir=project_dir,
                )
            )
            protect_payload = protect_outcome.to_payload()
            self.assertEqual(protect_payload["hookSpecificOutput"]["permissionDecision"], "deny")

            draft_outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={"last_assistant_message": "已完成：整理 hooks 文档", "session_id": "git-session"},
                    project_dir=project_dir,
                )
            )
            draft_payload = draft_outcome.to_payload()
            self.assertIn("已生成 PR 草稿", draft_payload["hookSpecificOutput"]["additionalContext"])
            draft_path = project_dir / ".codex" / "hooks" / "state" / "pr-draft.md"
            self.assertTrue(draft_path.exists())
            self.assertIn("整理 hooks 文档", draft_path.read_text(encoding="utf-8"))

    def test_git_pack_suggests_and_creates_session_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            (project_dir / "README.md").write_text("# demo\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "README.md"])
            self._run_git(project_dir, ["commit", "-m", "init"])

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("warn"):
                dispatcher.register_rule(rule)

            suggest_outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.SESSION_START,
                    platform=HookPlatform.CODEX,
                    payload={"session_id": "session-branch"},
                    project_dir=project_dir,
                )
            )
            suggest_payload = suggest_outcome.to_payload()
            self.assertIn("建议为本次会话切出独立分支", suggest_payload["hookSpecificOutput"]["additionalContext"])
            self.assertEqual(self._read_git(project_dir, ["branch", "--show-current"]), "main")

            create_dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("enforce"):
                create_dispatcher.register_rule(rule)

            create_outcome = create_dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.SESSION_START,
                    platform=HookPlatform.CODEX,
                    payload={"session_id": "session-branch", "git_auto_branch": True},
                    project_dir=project_dir,
                )
            )
            create_payload = create_outcome.to_payload()
            branch_name = self._read_git(project_dir, ["branch", "--show-current"])
            self.assertTrue(branch_name.startswith("codex/"))
            self.assertIn("已创建会话工作分支", create_payload["hookSpecificOutput"]["additionalContext"])

    def test_git_pack_auto_commit_creates_checkpoint_after_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            (project_dir / "README.md").write_text("# demo\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "README.md"])
            self._run_git(project_dir, ["commit", "-m", "init"])
            self._run_git(project_dir, ["checkout", "-b", "codex/demo"])
            (project_dir / "README.md").write_text("# demo\n\ncheckpoint\n", encoding="utf-8")

            store = HookStateStore(project_dir)
            store.set_value(
                ["runtime", "last_verification"],
                {"status": "passed", "command": "python -m unittest"},
            )

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={
                        "last_assistant_message": "已完成：补齐 git 自动提交",
                        "session_id": "git-auto-commit",
                        "git_auto_commit": True,
                    },
                    project_dir=project_dir,
                )
            )
            payload = outcome.to_payload()
            self.assertIn("已自动提交检查点", payload["hookSpecificOutput"]["additionalContext"])
            self.assertIn("补齐 git 自动提交", self._read_git(project_dir, ["log", "-1", "--pretty=%s"]))

    def test_git_pack_auto_commit_skips_on_protected_branch_or_validation_issue(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            (project_dir / "README.md").write_text("# demo\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "README.md"])
            self._run_git(project_dir, ["commit", "-m", "init"])
            (project_dir / "demo.py").write_text("# TODO: keep\nprint('demo')\n", encoding="utf-8")

            store = HookStateStore(project_dir)
            store.set_value(
                ["runtime", "last_verification"],
                {"status": "passed", "command": "python -m unittest"},
            )

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={
                        "last_assistant_message": "已完成：尝试自动提交",
                        "session_id": "git-auto-commit-skip",
                        "git_auto_commit": True,
                    },
                    project_dir=project_dir,
                )
            )
            payload = outcome.to_payload()
            self.assertIn("当前分支受保护", payload["hookSpecificOutput"]["additionalContext"])
            self.assertEqual(self._read_git(project_dir, ["log", "-1", "--pretty=%s"]), "init")

    def test_git_pack_auto_commit_skips_when_untracked_source_has_todo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            (project_dir / "README.md").write_text("# demo\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "README.md"])
            self._run_git(project_dir, ["commit", "-m", "init"])
            self._run_git(project_dir, ["checkout", "-b", "codex/demo"])
            (project_dir / "new_feature.py").write_text("# TODO: cleanup\nprint('demo')\n", encoding="utf-8")

            store = HookStateStore(project_dir)
            store.set_value(
                ["runtime", "last_verification"],
                {"status": "passed", "command": "python -m unittest"},
            )

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("enforce"):
                dispatcher.register_rule(rule)

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={
                        "last_assistant_message": "已完成：尝试提交未跟踪文件",
                        "session_id": "git-auto-commit-untracked",
                        "git_auto_commit": True,
                    },
                    project_dir=project_dir,
                )
            )
            payload = outcome.to_payload()
            self.assertIn("验证未通过", payload["hookSpecificOutput"]["additionalContext"])
            self.assertEqual(self._read_git(project_dir, ["log", "-1", "--pretty=%s"]), "init")

    def test_git_pack_session_branch_supports_env_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            (project_dir / "README.md").write_text("# demo\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "README.md"])
            self._run_git(project_dir, ["commit", "-m", "init"])

            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_git_rules("enforce"):
                dispatcher.register_rule(rule)

            with patch.dict("os.environ", {"HOOK_GIT_AUTO_BRANCH": "1"}, clear=False):
                outcome = dispatcher.dispatch(
                    HookRequest(
                        event_name=HookEvent.SESSION_START,
                        platform=HookPlatform.CODEX,
                        payload={"session_id": "env-branch"},
                        project_dir=project_dir,
                    )
                )

            payload = outcome.to_payload()
            self.assertIn("已创建会话工作分支", payload["hookSpecificOutput"]["additionalContext"])
            self.assertTrue(self._read_git(project_dir, ["branch", "--show-current"]).startswith("codex/"))

    def test_notify_pack_records_timer_and_completion_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_notify_rules("warn"):
                dispatcher.register_rule(rule)

            dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.SESSION_START,
                    platform=HookPlatform.CLAUDE,
                    payload={"session_id": "notify-session"},
                    project_dir=project_dir,
                )
            )

            notification_outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.NOTIFICATION,
                    platform=HookPlatform.CLAUDE,
                    payload=load_fixture("notification-authsuccess.json"),
                    project_dir=project_dir,
                )
            )
            notification_payload = notification_outcome.to_payload()
            self.assertIn("认证成功", notification_payload["hookSpecificOutput"]["additionalContext"])

            stop_outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CLAUDE,
                    payload=load_fixture("stop-complete.json"),
                    project_dir=project_dir,
                )
            )
            stop_payload = stop_outcome.to_payload()
            self.assertIn("通知摘要：任务已完成", stop_payload["hookSpecificOutput"]["additionalContext"])
            store = HookStateStore(project_dir)
            completion_record = store.get_value(["sessions", "notify-session", "notify", "last_completion"])
            self.assertIsInstance(completion_record, dict)

    def test_validate_pack_blocks_when_todo_left_in_changed_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            self._init_git_repo(project_dir)
            file_path = project_dir / "demo.py"
            file_path.write_text("print('ok')\n", encoding="utf-8")
            self._run_git(project_dir, ["add", "demo.py"])
            self._run_git(project_dir, ["commit", "-m", "init validate"])

            file_path.write_text("# TODO: cleanup\nprint('ok')\n", encoding="utf-8")
            dispatcher = build_runtime_dispatcher(project_dir)
            for rule in build_validate_rules("enforce"):
                dispatcher.register_rule(rule)

            store = HookStateStore(project_dir)
            store.set_value(
                ["runtime", "last_verification"],
                {"status": "passed", "command": "pytest"},
            )

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={"last_assistant_message": "已完成：验证 pack 基线", "session_id": "validate-session"},
                    project_dir=project_dir,
                )
            )
            payload = outcome.to_payload()
            self.assertEqual(payload["decision"], "block")
            self.assertIn("TODO", payload["reason"])

    def _init_git_repo(self, project_dir: Path) -> None:
        self._run_git(project_dir, ["init"])
        self._run_git(project_dir, ["config", "user.email", "test@example.com"])
        self._run_git(project_dir, ["config", "user.name", "Test User"])
        self._run_git(project_dir, ["checkout", "-b", "main"])

    def _run_git(self, project_dir: Path, args: list[str]) -> None:
        result = subprocess.run(
            ["git", *args],
            cwd=project_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stdout}\n{result.stderr}")

    def _read_git(self, project_dir: Path, args: list[str]) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=project_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stdout}\n{result.stderr}")
        return result.stdout.strip()


if __name__ == "__main__":
    unittest.main()
