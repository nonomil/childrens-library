#!/usr/bin/env python3
"""刷新 docs/修订记录/目录索引.md 中的索引表。"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REVISION_DIR = Path("docs") / "修订记录"
INDEX_FILE_NAME = "目录索引.md"
TEMPLATE_DIR_NAME = "模板"
RECORD_FILE_PATTERN = re.compile(r"^(?P<record_id>\d{4})-(?P<date>\d{4}-\d{2}-\d{2})-.+\.md$")
HEADER_FIELD_PATTERN = re.compile(r"^#\s*(?P<field>[^：]+)：(?P<value>.*)$")
SECTION_FIELD_PATTERN = re.compile(r"^##\s*(?P<title>.+?)\s*$")
INDEX_HEADING = "## 索引"
QUICK_REFERENCE_HEADING = "## 禁止重试方案速查（高频错误汇总）"
QUICK_REFERENCE_SECTION_TITLE = "速查结论（可选）"
TABLE_HEADER_LINES = [
    "| 编号 | 日期 | 模块/问题范围 | 核心结论 | 文件 |",
    "|------|------|--------------|---------|------|",
]


@dataclass
class RecordEntry:
    """索引表中的一条记录。"""

    record_id: str
    record_date: str
    issue_scope: str
    conclusion: str
    relative_path: str
    quick_reference_items: list[str]


def configure_streams() -> None:
    """将标准流调整为 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="刷新修订记录目录索引表")
    parser.add_argument("--project-dir", default=".", help="项目根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不落盘")
    return parser.parse_args(argv)


def collect_record_paths(revision_dir: Path) -> list[Path]:
    """收集各任务目录中的真实记录文件。"""
    record_paths: list[Path] = []
    if not revision_dir.exists():
        return record_paths

    for child_path in sorted(revision_dir.iterdir(), key=lambda item: item.name):
        if not child_path.is_dir():
            continue
        if child_path.name == TEMPLATE_DIR_NAME:
            continue
        for record_path in sorted(child_path.iterdir(), key=lambda item: item.name):
            if not record_path.is_file():
                continue
            if record_path.suffix.lower() != ".md":
                continue
            if not RECORD_FILE_PATTERN.match(record_path.name):
                continue
            record_paths.append(record_path)
    return record_paths


def parse_record(record_path: Path, revision_dir: Path) -> tuple[RecordEntry | None, str | None]:
    """解析单条记录。"""
    text = record_path.read_text(encoding="utf-8")
    header_fields: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for raw_line in text.splitlines():
        header_match = HEADER_FIELD_PATTERN.match(raw_line.strip())
        if header_match and current_section is None:
            header_fields[header_match.group("field").strip()] = header_match.group("value").strip()
            continue

        section_match = SECTION_FIELD_PATTERN.match(raw_line.strip())
        if section_match:
            current_section = section_match.group("title").strip()
            sections[current_section] = []
            continue

        if current_section is not None:
            sections[current_section].append(raw_line.rstrip())

    required_map = {
        "记录编号": "record_id",
        "日期": "record_date",
        "模式": "mode",
        "问题范围": "issue_scope",
    }
    missing_fields = [field_name for field_name in required_map if not header_fields.get(field_name)]
    conclusion_text = extract_section_text(sections.get("结论", []))
    if not conclusion_text:
        missing_fields.append("结论")
    if missing_fields:
        return None, f"缺少必填字段: {', '.join(missing_fields)}"

    relative_path = record_path.relative_to(revision_dir).as_posix()
    entry = RecordEntry(
        record_id=header_fields["记录编号"],
        record_date=header_fields["日期"],
        issue_scope=header_fields["问题范围"],
        conclusion=conclusion_text,
        relative_path=relative_path,
        quick_reference_items=extract_list_items(sections.get(QUICK_REFERENCE_SECTION_TITLE, [])),
    )
    return entry, None


def extract_section_text(section_lines: list[str]) -> str:
    """提取小节正文的首段文本。"""
    paragraph_lines: list[str] = []
    for raw_line in section_lines:
        line = raw_line.strip()
        if not line:
            if paragraph_lines:
                break
            continue
        paragraph_lines.append(line)
    return " ".join(paragraph_lines).strip()


def extract_list_items(section_lines: list[str]) -> list[str]:
    """提取小节中的显式列表项。"""
    items: list[str] = []
    for raw_line in section_lines:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def build_index_table(entries: list[RecordEntry]) -> list[str]:
    """构建索引表文本。"""
    lines = list(TABLE_HEADER_LINES)
    for entry in entries:
        lines.append(
            f"| {entry.record_id} | {entry.record_date} | {entry.issue_scope} | {entry.conclusion} | [记录]({entry.relative_path}) |"
        )
    return lines


def build_quick_reference_lines(entries: list[RecordEntry]) -> list[str]:
    """构建速查区文本。"""
    lines: list[str] = []
    for entry in entries:
        for item in entry.quick_reference_items:
            lines.append(f"- {item}（见 `{entry.record_id}`）")
    if not lines:
        lines.append("- 暂无显式速查结论")
    return lines


def replace_named_section(index_text: str, section_heading: str, body_lines: list[str]) -> str:
    """只替换目录索引中的指定区块。"""
    lines = index_text.splitlines()
    start_index: int | None = None
    end_index: int | None = None

    for index, line in enumerate(lines):
        if line.strip() == section_heading:
            start_index = index
            continue
        if start_index is not None and index > start_index and line.startswith("## "):
            end_index = index
            break

    if start_index is None:
        raise ValueError(f"目录索引缺少“{section_heading}”区块")
    if end_index is None:
        end_index = len(lines)

    new_lines = lines[: start_index + 1]
    new_lines.append("")
    new_lines.extend(body_lines)
    new_lines.append("")
    new_lines.extend(lines[end_index:])
    return "\n".join(new_lines) + "\n"


def replace_index_section(index_text: str, table_lines: list[str]) -> str:
    """只替换目录索引中的索引表区块。"""
    return replace_named_section(index_text, INDEX_HEADING, table_lines)


def main(argv: list[str] | None = None) -> int:
    """脚本入口。"""
    configure_streams()
    args = parse_args(argv)
    project_dir = Path(args.project_dir).resolve()
    revision_dir = project_dir / REVISION_DIR
    index_path = revision_dir / INDEX_FILE_NAME

    if not index_path.exists():
        print(f"[revision_index_sync] 未找到索引文件: {index_path}", file=sys.stderr)
        return 2

    entries: list[RecordEntry] = []
    for record_path in collect_record_paths(revision_dir):
        entry, warning_text = parse_record(record_path, revision_dir)
        if warning_text:
            print(f"[revision_index_sync] 跳过 {record_path.name}：{warning_text}", file=sys.stderr)
            continue
        if entry is not None:
            entries.append(entry)

    entries.sort(key=lambda item: (item.record_id, item.record_date, item.relative_path))
    table_lines = build_index_table(entries)
    quick_reference_lines = build_quick_reference_lines(entries)
    original_text = index_path.read_text(encoding="utf-8")
    updated_text = replace_index_section(original_text, table_lines)
    updated_text = replace_named_section(updated_text, QUICK_REFERENCE_HEADING, quick_reference_lines)

    if args.dry_run:
        if updated_text == original_text:
            print("[revision_index_sync] dry-run: 索引表无需更新")
        else:
            print(f"[revision_index_sync] dry-run: 将刷新 {index_path}")
        return 0

    if updated_text == original_text:
        print(f"[revision_index_sync] 索引表无需更新: {index_path}")
        return 0

    index_path.write_text(updated_text, encoding="utf-8")
    print(f"[revision_index_sync] 已刷新索引表: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
