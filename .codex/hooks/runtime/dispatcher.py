#!/usr/bin/env python3
"""hooks 运行时调度器与 dry-run 模拟入口。"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


HOOK_ROOT = Path(__file__).resolve().parents[1]
if str(HOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(HOOK_ROOT))

from runtime.audit_log import AuditEntry, AuditLogger
from runtime.contracts import ActionMode, DispatchOutcome, HookEvent, HookPlatform, HookRequest, HookResult, TERMINAL_ACTIONS
from runtime.platform_adapter import detect_platform, event_is_supported, normalize_event_name
from runtime.state_store import HookStateStore


HookHandler = Callable[[HookRequest], HookResult]


@dataclass(order=True, slots=True)
class DispatchRule:
    """一条调度规则。"""

    priority: int = 100
    name: str = field(default="unnamed", compare=False)
    events: tuple[HookEvent, ...] = field(default_factory=tuple, compare=False)
    handler: HookHandler = field(default=lambda _: HookResult.noop(), compare=False)
    platforms: tuple[HookPlatform, ...] = field(default_factory=tuple, compare=False)
    stop_on_action: bool = field(default=True, compare=False)

    def matches(self, request: HookRequest) -> bool:
        if self.events and request.event_name not in self.events:
            return False
        if self.platforms and request.platform not in self.platforms:
            return False
        return True


class HookRuntimeDispatcher:
    """统一调度 hooks 规则。"""

    def __init__(
        self,
        project_dir: Path,
        *,
        state_store: HookStateStore | None = None,
        audit_logger: AuditLogger | None = None,
    ) -> None:
        self.project_dir = project_dir.resolve()
        self.state_store = state_store or HookStateStore(self.project_dir)
        self.audit_logger = audit_logger or AuditLogger(self.project_dir)
        self.rules: list[DispatchRule] = []

    def register_rule(self, rule: DispatchRule) -> None:
        """注册规则。"""
        self.rules.append(rule)
        self.rules.sort()

    def dispatch(self, request: HookRequest) -> DispatchOutcome:
        """执行一次调度。"""
        outcome = DispatchOutcome(request=request)
        self._record_dispatch_start(request)

        for rule in self.rules:
            if not rule.matches(request):
                continue
            start_time = time.perf_counter()
            try:
                result = rule.handler(request)
            except Exception as exc:  # pragma: no cover - 保护性分支
                result = HookResult.context(
                    f"规则 `{rule.name}` 执行异常：{exc}",
                    exception_type=exc.__class__.__name__,
                )
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            outcome.add_record(rule.name, result, elapsed_ms)
            self._record_audit_entry(request, rule.name, result, elapsed_ms)

            if request.dry_run:
                continue
            if result.action in TERMINAL_ACTIONS and rule.stop_on_action:
                break

        self._record_dispatch_finish(request, outcome)
        return outcome

    def _record_dispatch_start(self, request: HookRequest) -> None:
        dispatch_total = self.state_store.increment_value(["runtime", "dispatch_total"])
        self.state_store.set_value(
            ["runtime", "last_event"],
            {
                "dispatch_total": dispatch_total,
                "event_name": request.event_name.value,
                "platform": request.platform.value,
                "session_id": request.session_id,
                "dry_run": request.dry_run,
            },
        )

    def _record_dispatch_finish(self, request: HookRequest, outcome: DispatchOutcome) -> None:
        self.state_store.set_value(["runtime", "last_output"], outcome.to_payload())
        if request.session_id:
            self.state_store.set_value(
                ["sessions", request.session_id, "last_event"],
                {
                    "event_name": request.event_name.value,
                    "platform": request.platform.value,
                    "record_count": len(outcome.records),
                },
            )
        self.state_store.append_recent_event(
            {
                "event_name": request.event_name.value,
                "platform": request.platform.value,
                "record_count": len(outcome.records),
                "dry_run": request.dry_run,
            }
        )

    def _record_audit_entry(
        self,
        request: HookRequest,
        rule_name: str,
        result: HookResult,
        elapsed_ms: int,
    ) -> None:
        summary = result.message.strip() or result.additional_context.strip()
        entry = AuditEntry.build(
            platform=request.platform.value,
            event_name=request.event_name.value,
            rule_name=rule_name,
            action=result.action.value,
            elapsed_ms=elapsed_ms,
            dry_run=request.dry_run,
            session_id=request.session_id,
            message=summary,
            metadata=result.metadata,
        )
        self.audit_logger.append_entry(entry)


def runtime_platform_guard(request: HookRequest) -> HookResult:
    """事件不受平台支持时给出上下文提醒。"""
    if event_is_supported(request.platform, request.event_name):
        return HookResult.noop("事件受支持")
    return HookResult.context(
        f"平台 `{request.platform.value}` 当前未声明原生支持 `{request.event_name.value}`，"
        "建议先以 observe 模式验证，再决定是否启用 enforce。"
    )


def runtime_stop_guard(request: HookRequest) -> HookResult:
    """Stop 事件的防循环保护。"""
    if request.event_name != HookEvent.STOP:
        return HookResult.noop()
    if request.stop_hook_active:
        return HookResult.context("检测到 stop_hook_active=true，本轮跳过强制续跑判定。")
    return HookResult.noop()


def build_runtime_dispatcher(project_dir: Path) -> HookRuntimeDispatcher:
    """创建带基础守卫的调度器。"""
    dispatcher = HookRuntimeDispatcher(project_dir=project_dir)
    dispatcher.register_rule(
        DispatchRule(
            priority=10,
            name="runtime_platform_guard",
            events=tuple(event for event in HookEvent),
            handler=runtime_platform_guard,
            stop_on_action=False,
        )
    )
    dispatcher.register_rule(
        DispatchRule(
            priority=20,
            name="runtime_stop_guard",
            events=(HookEvent.STOP,),
            handler=runtime_stop_guard,
            stop_on_action=False,
        )
    )
    return dispatcher


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="模拟 hooks 运行时调度")
    parser.add_argument("--event", required=True, help="事件名，例如 Stop / PostToolUse")
    parser.add_argument("--platform", default="", help="平台名，claude / codex")
    parser.add_argument("--project-dir", default=".", help="项目根目录")
    parser.add_argument("--payload-file", default="", help="JSON 输入文件，可选")
    parser.add_argument("--dry-run", action="store_true", help="只模拟，不输出强阻断动作")
    return parser.parse_args(argv)


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    """从文件或标准输入读取 JSON 负载。"""
    if args.payload_file:
        text = Path(args.payload_file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        return {}
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("hook payload 必须是 JSON 对象")
    return data


def resolve_platform(project_dir: Path, platform_text: str) -> HookPlatform:
    """解析平台参数。"""
    normalized = platform_text.strip().lower()
    if normalized == HookPlatform.CLAUDE.value:
        return HookPlatform.CLAUDE
    if normalized == HookPlatform.CODEX.value:
        return HookPlatform.CODEX
    return detect_platform(project_dir)


def main(argv: list[str] | None = None) -> int:
    """命令行入口。"""
    args = parse_args(argv)
    project_dir = Path(args.project_dir).resolve()
    payload = load_payload(args)
    event_name = normalize_event_name(args.event)
    platform = resolve_platform(project_dir, args.platform)

    dispatcher = build_runtime_dispatcher(project_dir)
    outcome = dispatcher.dispatch(
        HookRequest(
            event_name=event_name,
            platform=platform,
            payload=payload,
            project_dir=project_dir,
            dry_run=args.dry_run,
        )
    )
    print(json.dumps(outcome.to_payload(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
