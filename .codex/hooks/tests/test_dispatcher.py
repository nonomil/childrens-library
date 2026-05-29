from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


HOOK_ROOT = Path(__file__).resolve().parents[1]
if str(HOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(HOOK_ROOT))

from runtime.audit_log import AuditLogger
from runtime.contracts import HookEvent, HookPlatform, HookRequest, HookResult
from runtime.dispatcher import DispatchRule, HookRuntimeDispatcher, build_runtime_dispatcher
from runtime.state_store import HookStateStore


DISPATCHER_PATH = HOOK_ROOT / "runtime" / "dispatcher.py"


def load_dispatcher_module():
    """按文件路径加载 dispatcher 模块。"""
    spec = importlib.util.spec_from_file_location("codex_hooks_dispatcher", DISPATCHER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块: {DISPATCHER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DispatcherRuntimeTest(unittest.TestCase):
    def test_dispatch_stops_after_block_when_not_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_store = HookStateStore(project_dir)
            audit_logger = AuditLogger(project_dir)
            dispatcher = HookRuntimeDispatcher(
                project_dir=project_dir,
                state_store=state_store,
                audit_logger=audit_logger,
            )

            def first_rule(_request: HookRequest) -> HookResult:
                return HookResult.context("先记录上下文")

            def second_rule(_request: HookRequest) -> HookResult:
                return HookResult.block("测试失败，需要修复")

            def third_rule(_request: HookRequest) -> HookResult:
                return HookResult.context("这条不应执行")

            dispatcher.register_rule(
                DispatchRule(
                    priority=10,
                    name="first_rule",
                    events=(HookEvent.STOP,),
                    handler=first_rule,
                    stop_on_action=False,
                )
            )
            dispatcher.register_rule(
                DispatchRule(
                    priority=20,
                    name="second_rule",
                    events=(HookEvent.STOP,),
                    handler=second_rule,
                )
            )
            dispatcher.register_rule(
                DispatchRule(
                    priority=30,
                    name="third_rule",
                    events=(HookEvent.STOP,),
                    handler=third_rule,
                    stop_on_action=False,
                )
            )

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={"last_assistant_message": "未完成"},
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["decision"], "block")
            self.assertIn("测试失败，需要修复", payload["reason"])
            self.assertIn("先记录上下文", payload["reason"])
            self.assertEqual(len(outcome.records), 2)
            self.assertEqual(state_store.get_value(["runtime", "dispatch_total"]), 1)
            self.assertEqual(len(audit_logger.read_recent()), 2)

    def test_dry_run_turns_terminal_actions_into_context_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = HookRuntimeDispatcher(project_dir=project_dir)

            dispatcher.register_rule(
                DispatchRule(
                    priority=10,
                    name="deny_rule",
                    events=(HookEvent.PRE_TOOL_USE,),
                    handler=lambda _request: HookResult.deny("检测到危险命令"),
                )
            )
            dispatcher.register_rule(
                DispatchRule(
                    priority=20,
                    name="context_rule",
                    events=(HookEvent.PRE_TOOL_USE,),
                    handler=lambda _request: HookResult.context("这是补充提示"),
                    stop_on_action=False,
                )
            )

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PRE_TOOL_USE,
                    platform=HookPlatform.CLAUDE,
                    payload={"tool_name": "Bash"},
                    project_dir=project_dir,
                    dry_run=True,
                )
            )

            payload = outcome.to_payload()
            additional_context = payload["hookSpecificOutput"]["additionalContext"]
            self.assertIn("[dry-run][deny_rule] deny: 检测到危险命令", additional_context)
            self.assertIn("[dry-run][context_rule] context: 这是补充提示", additional_context)
            self.assertEqual(len(outcome.records), 2)

    def test_allow_result_matches_permission_request_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = HookRuntimeDispatcher(project_dir=project_dir)
            dispatcher.register_rule(
                DispatchRule(
                    priority=10,
                    name="allow_rule",
                    events=(HookEvent.PERMISSION_REQUEST,),
                    handler=lambda request: HookResult.allow(
                        updated_input={"command": request.tool_input.get("command", "")},
                        message="自动放行低风险命令",
                    ),
                )
            )

            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.PERMISSION_REQUEST,
                    platform=HookPlatform.CLAUDE,
                    payload={
                        "tool_name": "Bash",
                        "tool_input": {"command": "git status"},
                    },
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["hookSpecificOutput"]["decision"]["behavior"], "allow")
            self.assertEqual(
                payload["hookSpecificOutput"]["decision"]["updatedInput"]["command"],
                "git status",
            )
            self.assertIn("自动放行低风险命令", payload["hookSpecificOutput"]["additionalContext"])

    def test_runtime_dispatcher_records_stop_guard_and_cli_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            dispatcher = build_runtime_dispatcher(project_dir)
            outcome = dispatcher.dispatch(
                HookRequest(
                    event_name=HookEvent.STOP,
                    platform=HookPlatform.CODEX,
                    payload={"stop_hook_active": True, "session_id": "demo-session"},
                    project_dir=project_dir,
                )
            )

            payload = outcome.to_payload()
            self.assertEqual(payload["hookSpecificOutput"]["hookEventName"], "Stop")
            self.assertIn("stop_hook_active=true", payload["hookSpecificOutput"]["additionalContext"])

            dispatcher_module = load_dispatcher_module()
            payload_file = project_dir / "payload.json"
            payload_file.write_text(
                json.dumps({"stop_hook_active": True, "session_id": "cli-session"}, ensure_ascii=False),
                encoding="utf-8",
            )
            exit_code = dispatcher_module.main(
                [
                    "--event",
                    "Stop",
                    "--platform",
                    "codex",
                    "--project-dir",
                    str(project_dir),
                    "--payload-file",
                    str(payload_file),
                    "--dry-run",
                ]
            )
            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
