#!/usr/bin/env python3
"""按 pack 执行 hooks 规则的统一入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


HOOK_ROOT = Path(__file__).resolve().parents[1]
if str(HOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(HOOK_ROOT))

from packs import PACK_BUILDERS
from packs.common import normalize_mode
from runtime.contracts import HookRequest
from runtime.dispatcher import build_runtime_dispatcher
from runtime.platform_adapter import HookPlatform, detect_platform, normalize_event_name


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="执行指定 hooks pack")
    parser.add_argument("--pack", required=True, choices=sorted(PACK_BUILDERS.keys()), help="pack 名称")
    parser.add_argument("--event", required=True, help="事件名，例如 Stop / PostToolUse")
    parser.add_argument("--platform", default="", help="平台名，claude / codex")
    parser.add_argument("--mode", default="warn", help="档位：observe / warn / enforce")
    parser.add_argument("--project-dir", default=".", help="项目根目录")
    parser.add_argument("--payload-file", default="", help="JSON 输入文件，可选")
    parser.add_argument("--dry-run", action="store_true", help="只模拟，不输出强阻断动作")
    return parser.parse_args(argv)


def load_payload(payload_file: str) -> dict:
    """从文件或标准输入读取 JSON 负载。"""
    if payload_file:
        text = Path(payload_file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    if not text.strip():
        return {}
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("hook payload 必须是 JSON 对象")
    return payload


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
    payload = load_payload(args.payload_file)
    platform = resolve_platform(project_dir, args.platform)
    event_name = normalize_event_name(args.event)
    mode_text = normalize_mode(args.mode)

    dispatcher = build_runtime_dispatcher(project_dir)
    builder = PACK_BUILDERS[args.pack]
    for rule in builder(mode_text):
        dispatcher.register_rule(rule)

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
