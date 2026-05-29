#!/usr/bin/env python3
"""导出修订记录的 AI 轨摘要到 .claude/memory/context/revision/。"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


def load_revision_index_module():
    """按相邻脚本路径加载 revision_index_sync 模块。"""
    module_name = "revision_index_sync"
    if module_name in sys.modules:
        return sys.modules[module_name]

    script_path = Path(__file__).resolve().with_name("revision_index_sync.py")
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块: {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


revision_index = load_revision_index_module()


AI_CONTEXT_DIR = Path(".claude") / "memory" / "context" / "revision"
AI_SUMMARY_SECTION_TITLE = "AI轨摘要（可选）"
EXPORTABLE_MODES = {"标准", "高级", "standard", "advanced"}


@dataclass
class AiContextEntry:
    """一条修订记录对应的 AI 轨导出数据。"""

    record_id: str
    record_date: str
    mode: str
    issue_scope: str
    conclusion: str
    relative_record_path: str
    export_relative_path: Path
    wrong_approaches: list[str]
    read_before_items: list[str]
    ai_summary_items: list[str]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="导出修订记录 AI 轨摘要")
    parser.add_argument("--project-dir", default=".", help="项目根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不落盘")
    return parser.parse_args(argv)


def parse_record_for_ai(record_path: Path, project_dir: Path, revision_dir: Path) -> tuple[AiContextEntry | None, str | None]:
    """解析单条记录，决定是否导出 AI 轨。"""
    text = record_path.read_text(encoding="utf-8")
    header_fields: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for raw_line in text.splitlines():
        header_match = revision_index.HEADER_FIELD_PATTERN.match(raw_line.strip())
        if header_match and current_section is None:
            header_fields[header_match.group("field").strip()] = header_match.group("value").strip()
            continue

        section_match = revision_index.SECTION_FIELD_PATTERN.match(raw_line.strip())
        if section_match:
            current_section = section_match.group("title").strip()
            sections[current_section] = []
            continue

        if current_section is not None:
            sections[current_section].append(raw_line.rstrip())

    required_fields = ["记录编号", "日期", "模式", "问题范围"]
    missing_fields = [field_name for field_name in required_fields if not header_fields.get(field_name)]
    conclusion_text = revision_index.extract_section_text(sections.get("结论", []))
    if not conclusion_text:
        missing_fields.append("结论")
    if missing_fields:
        return None, f"缺少必填字段: {', '.join(missing_fields)}"

    ai_summary_items = revision_index.extract_list_items(sections.get(AI_SUMMARY_SECTION_TITLE, []))
    mode_text = header_fields["模式"].strip()
    should_export = mode_text in EXPORTABLE_MODES or mode_text.lower() in EXPORTABLE_MODES or bool(ai_summary_items)
    if not should_export:
        return None, None

    relative_record_path = record_path.relative_to(project_dir).as_posix()
    export_relative_path = record_path.relative_to(revision_dir)
    entry = AiContextEntry(
        record_id=header_fields["记录编号"],
        record_date=header_fields["日期"],
        mode=mode_text,
        issue_scope=header_fields["问题范围"],
        conclusion=conclusion_text,
        relative_record_path=relative_record_path,
        export_relative_path=export_relative_path,
        wrong_approaches=revision_index.extract_list_items(sections.get("禁止重复的错误方案", [])),
        read_before_items=revision_index.extract_list_items(sections.get("下次修改前先读", [])),
        ai_summary_items=ai_summary_items,
    )
    return entry, None


def render_ai_context(entry: AiContextEntry) -> str:
    """渲染单条 AI 轨摘要。"""
    lines = [
        "---",
        f'source_record: "{entry.relative_record_path}"',
        f'record_id: "{entry.record_id}"',
        f'date: "{entry.record_date}"',
        f'mode: "{entry.mode}"',
        f'issue_scope: "{entry.issue_scope}"',
        "---",
        "",
        f"# 修订记录 AI 摘要：{entry.record_id}",
        "",
        "## 核心结论",
        "",
        entry.conclusion,
        "",
        "## 禁止重复方案",
        "",
    ]

    if entry.wrong_approaches:
        lines.extend([f"- {item}" for item in entry.wrong_approaches])
    else:
        lines.append("- 暂无显式禁止重复方案")

    lines.extend(["", "## 下次先读", ""])
    if entry.read_before_items:
        lines.extend([f"- {item}" for item in entry.read_before_items])
    else:
        lines.append("- 暂无显式下次先读项")

    if entry.ai_summary_items:
        lines.extend(["", "## AI 摘要（显式）", ""])
        lines.extend([f"- {item}" for item in entry.ai_summary_items])

    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """脚本入口。"""
    revision_index.configure_streams()
    args = parse_args(argv)
    project_dir = Path(args.project_dir).resolve()
    revision_dir = project_dir / revision_index.REVISION_DIR
    export_root = project_dir / AI_CONTEXT_DIR

    entries: list[AiContextEntry] = []
    for record_path in revision_index.collect_record_paths(revision_dir):
        entry, warning_text = parse_record_for_ai(record_path, project_dir, revision_dir)
        if warning_text:
            print(f"[revision_context_sync] 跳过 {record_path.name}：{warning_text}", file=sys.stderr)
            continue
        if entry is not None:
            entries.append(entry)

    entries.sort(key=lambda item: (item.record_id, item.record_date, item.relative_record_path))
    changed_targets: list[tuple[Path, str]] = []
    for entry in entries:
        target_path = export_root / entry.export_relative_path
        rendered_text = render_ai_context(entry)
        if not target_path.exists() or target_path.read_text(encoding="utf-8") != rendered_text:
            changed_targets.append((target_path, rendered_text))

    if args.dry_run:
        if not changed_targets:
            print("[revision_context_sync] dry-run: AI 轨摘要无需更新")
        else:
            print(f"[revision_context_sync] dry-run: 将写入 {len(changed_targets)} 个 AI 轨摘要文件")
        return 0

    if not changed_targets:
        print(f"[revision_context_sync] AI 轨摘要无需更新: {export_root}")
        return 0

    for target_path, rendered_text in changed_targets:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(rendered_text, encoding="utf-8")

    print(f"[revision_context_sync] 已写入 {len(changed_targets)} 个 AI 轨摘要文件到 {export_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
