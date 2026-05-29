#!/usr/bin/env python3
"""PreToolUse hook: 为长文档编辑提供轻量防踩踏与新鲜度检查。"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


DOC_SUFFIXES = {".md", ".mdx", ".html", ".htm", ".rst", ".txt"}
SPECIAL_DOC_NAMES = {"readme.md", "claude.md", "agents.md"}
ACTIVE_STATUSES = {"doing", "in_review", "approved", "queued"}
DOC_FRESHNESS_BEGIN = "# BEGIN DOC_FRESHNESS_STATE"
DOC_FRESHNESS_END = "# END DOC_FRESHNESS_STATE"
ANCHOR_BLOCK_PATTERN = re.compile(
    r"<!--\s*BEGIN(?P<generated>\s+GENERATED)?:(?P<name>[^>]+?)\s*-->"
    r"(?P<body>.*?)"
    r"<!--\s*END(?:\s+GENERATED)?:(?P=name)\s*-->",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class FreshnessEntry:
    path: str = ""
    content_hash: str = ""
    task_id: str = ""


@dataclass
class FileLease:
    path: str = ""
    section_anchor: str = ""
    lease_owner: str = ""
    lease_state: str = "active"


@dataclass
class TaskMeta:
    task_id: str = ""
    status: str = ""
    doc_targets: list[str] = field(default_factory=list)
    doc_target_anchors: dict[str, str] = field(default_factory=dict)
    section_anchor: str = ""
    file_leases: list[FileLease] = field(default_factory=list)


@dataclass
class AnchorRange:
    name: str
    start: int
    end: int
    generated: bool


def configure_stderr() -> None:
    """将 stderr 调整为 UTF-8，避免 Windows 控制台乱码。"""
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


def block(message_text: str) -> int:
    """统一输出阻断信息。"""
    print(message_text, file=sys.stderr)
    return 2


def get_project_dir() -> Path:
    """获取项目根目录。"""
    project_dir_text = os.getenv("CLAUDE_PROJECT_DIR", "").strip()
    if project_dir_text:
        return Path(project_dir_text).resolve()
    return Path.cwd().resolve()


def parse_scalar(raw_text: str) -> str:
    """解析简单 YAML 标量。"""
    value_text = raw_text.strip()
    if value_text.startswith("- "):
        value_text = value_text[2:].strip()
    if not value_text or value_text.lower() in {"null", "none", "~"}:
        return ""
    if len(value_text) >= 2 and value_text[0] == value_text[-1] and value_text[0] in {'"', "'"}:
        return value_text[1:-1]
    return value_text


def normalize_path(path_text: str, project_dir: Path) -> str:
    """将路径规范化为相对项目根目录的 posix 路径。"""
    cleaned_text = str(path_text).strip()
    if not cleaned_text:
        return ""
    candidate_path = Path(cleaned_text)
    if not candidate_path.is_absolute():
        candidate_path = (project_dir / candidate_path).resolve()
    else:
        candidate_path = candidate_path.resolve()
    try:
        return candidate_path.relative_to(project_dir).as_posix()
    except ValueError:
        return candidate_path.as_posix()


def is_document_path(target_path: Path) -> bool:
    """判断是否属于需要保护的文档。"""
    suffix_text = target_path.suffix.lower()
    if suffix_text in DOC_SUFFIXES:
        return True
    return target_path.name.lower() in SPECIAL_DOC_NAMES


def load_payload() -> dict:
    """读取 Hook 输入。"""
    raw_text = ""
    try:
        raw_text = sys.stdin.read().strip()
    except OSError:
        raw_text = ""
    if not raw_text:
        raw_text = os.getenv("CLAUDE_TOOL_INPUT", "").strip()
    if not raw_text:
        return {}
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def extract_tool_name(payload: dict) -> str:
    """提取工具名。"""
    tool_name = payload.get("tool_name") or payload.get("hook_event_name") or ""
    return str(tool_name).strip()


def extract_tool_input(payload: dict) -> dict:
    """提取工具输入。"""
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        return tool_input
    return payload


def extract_file_path(tool_input: dict) -> str:
    """提取目标文件路径。"""
    for key_name in ("file_path", "path", "filepath"):
        path_text = tool_input.get(key_name)
        if isinstance(path_text, str) and path_text.strip():
            return path_text.strip()
    return ""


def extract_old_strings(tool_input: dict) -> list[str]:
    """提取 edit/multiedit 的旧文本片段。"""
    collected: list[str] = []
    for key_name in ("old_string", "oldText"):
        value_text = tool_input.get(key_name)
        if isinstance(value_text, str) and value_text:
            collected.append(value_text)

    edits_value = tool_input.get("edits")
    if isinstance(edits_value, list):
        for edit_item in edits_value:
            if not isinstance(edit_item, dict):
                continue
            for key_name in ("old_string", "oldText"):
                value_text = edit_item.get(key_name)
                if isinstance(value_text, str) and value_text:
                    collected.append(value_text)

    unique_strings: list[str] = []
    seen_strings: set[str] = set()
    for item_text in collected:
        if item_text in seen_strings:
            continue
        seen_strings.add(item_text)
        unique_strings.append(item_text)
    return unique_strings


def compute_content_hash(file_path: Path) -> str:
    """计算文件内容哈希。"""
    content_bytes = file_path.read_bytes()
    digest_text = hashlib.sha256(content_bytes).hexdigest()
    return f"sha256:{digest_text}"


def load_manifest_text(project_dir: Path) -> str:
    """读取 MANIFEST 原文。"""
    manifest_path = project_dir / ".claude" / "state" / "MANIFEST.yaml"
    if not manifest_path.exists():
        return ""
    return manifest_path.read_text(encoding="utf-8")


def get_session_focus_path(project_dir: Path) -> Path:
    """返回当前会话的 focus.json 路径（含 deterministic fallback）。"""
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
        / "focus.json"
    )


def load_session_focus_task_id(project_dir: Path) -> str:
    """读取当前会话焦点任务编号（只读 session focus.json）。"""
    focus_path = get_session_focus_path(project_dir)
    if not focus_path.exists():
        return ""
    try:
        payload = json.loads(focus_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("task_id") or "").strip()


def parse_manifest_state(manifest_text: str) -> tuple[str, list[str], list[FreshnessEntry]]:
    """解析主焦点任务、次焦点任务与文档新鲜度状态。"""
    current_task_id = ""
    secondary_task_ids: list[str] = []
    entries: list[FreshnessEntry] = []
    current_entry: dict[str, str] | None = None
    in_current_focus = False
    in_secondary_focuses = False
    in_doc_freshness = False
    in_entries = False

    for raw_line in manifest_text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        indent_size = len(raw_line) - len(raw_line.lstrip(" "))

        if indent_size == 0:
            if current_entry:
                entries.append(
                    FreshnessEntry(
                        path=current_entry.get("path", ""),
                        content_hash=current_entry.get("content_hash", ""),
                        task_id=current_entry.get("task_id", ""),
                    )
                )
                current_entry = None
            in_entries = False
            in_current_focus = stripped_line == "current_focus:"
            in_secondary_focuses = stripped_line == "secondary_focuses:"
            in_doc_freshness = stripped_line == "doc_freshness:"
            continue

        if in_current_focus and indent_size >= 2 and stripped_line.startswith("task_id:"):
            current_task_id = parse_scalar(stripped_line.split(":", 1)[1])
            continue

        if in_secondary_focuses:
            if indent_size == 2 and stripped_line.startswith("- "):
                remainder_text = stripped_line[2:].strip()
                if remainder_text.startswith("task_id:"):
                    task_id = parse_scalar(remainder_text.split(":", 1)[1])
                    if task_id:
                        secondary_task_ids.append(task_id)
                continue
            if indent_size >= 4 and stripped_line.startswith("task_id:"):
                task_id = parse_scalar(stripped_line.split(":", 1)[1])
                if task_id:
                    secondary_task_ids.append(task_id)
                continue

        if not in_doc_freshness:
            continue

        if indent_size == 2 and stripped_line == "entries:":
            in_entries = True
            continue

        if not in_entries:
            continue

        if indent_size == 4 and stripped_line.startswith("- "):
            if current_entry:
                entries.append(
                    FreshnessEntry(
                        path=current_entry.get("path", ""),
                        content_hash=current_entry.get("content_hash", ""),
                        task_id=current_entry.get("task_id", ""),
                    )
                )
            current_entry = {}
            remainder_text = stripped_line[2:].strip()
            if remainder_text.startswith("path:"):
                current_entry["path"] = parse_scalar(remainder_text.split(":", 1)[1])
            continue

        if indent_size >= 6 and ":" in stripped_line and current_entry is not None:
            key_text, value_text = stripped_line.split(":", 1)
            current_entry[key_text.strip()] = parse_scalar(value_text)

    if current_entry:
        entries.append(
            FreshnessEntry(
                path=current_entry.get("path", ""),
                content_hash=current_entry.get("content_hash", ""),
                task_id=current_entry.get("task_id", ""),
            )
        )

    unique_secondary_task_ids: list[str] = []
    seen_task_ids: set[str] = {current_task_id} if current_task_id else set()
    for task_id in secondary_task_ids:
        if not task_id or task_id in seen_task_ids:
            continue
        seen_task_ids.add(task_id)
        unique_secondary_task_ids.append(task_id)

    return current_task_id, unique_secondary_task_ids, entries


def render_doc_freshness_block(entries: list[FreshnessEntry]) -> str:
    """渲染文档新鲜度块。"""
    lines = [DOC_FRESHNESS_BEGIN, "doc_freshness:"]
    if entries:
        lines.append("  entries:")
        for entry in sorted(entries, key=lambda item: (item.path, item.task_id)):
            lines.extend(
                [
                    f'    - path: "{entry.path}"',
                    f'      content_hash: "{entry.content_hash}"',
                    f'      task_id: "{entry.task_id}"',
                ]
            )
    else:
        lines.append("  entries: []")
    lines.append(DOC_FRESHNESS_END)
    return "\n".join(lines)


def write_manifest_freshness(
    project_dir: Path,
    manifest_text: str,
    entries: list[FreshnessEntry],
) -> None:
    """将文档新鲜度状态写回 MANIFEST。"""
    manifest_path = project_dir / ".claude" / "state" / "MANIFEST.yaml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    freshness_block = render_doc_freshness_block(entries)

    if DOC_FRESHNESS_BEGIN in manifest_text:
        base_manifest_text = manifest_text.split(DOC_FRESHNESS_BEGIN, 1)[0].rstrip()
        if base_manifest_text:
            new_manifest_text = base_manifest_text + "\n" + freshness_block + "\n"
        else:
            new_manifest_text = freshness_block + "\n"
    elif manifest_text.strip():
        new_manifest_text = manifest_text.rstrip() + "\n\n" + freshness_block + "\n"
    else:
        new_manifest_text = freshness_block + "\n"

    manifest_path.write_text(new_manifest_text, encoding="utf-8")


def update_freshness_snapshot(project_dir: Path, rel_path: str, current_task_id: str) -> str:
    """刷新当前任务的文档新鲜度快照。"""
    target_path = (project_dir / rel_path).resolve()
    content_hash = compute_content_hash(target_path)
    manifest_text = load_manifest_text(project_dir)
    _, _, entries = parse_manifest_state(manifest_text)

    replaced = False
    new_entries: list[FreshnessEntry] = []
    for entry in entries:
        entry_path = normalize_path(entry.path, project_dir)
        if entry_path == rel_path and entry.task_id == current_task_id:
            new_entries.append(
                FreshnessEntry(path=rel_path, content_hash=content_hash, task_id=current_task_id)
            )
            replaced = True
        else:
            new_entries.append(
                FreshnessEntry(
                    path=entry_path,
                    content_hash=entry.content_hash,
                    task_id=entry.task_id,
                )
            )

    if not replaced:
        new_entries.append(
            FreshnessEntry(path=rel_path, content_hash=content_hash, task_id=current_task_id)
        )

    write_manifest_freshness(project_dir, manifest_text, new_entries)
    return content_hash


def find_freshness_entry(
    entries: list[FreshnessEntry],
    project_dir: Path,
    rel_path: str,
    current_task_id: str,
) -> FreshnessEntry | None:
    """查找当前任务对应的文档新鲜度记录。"""
    for entry in entries:
        entry_path = normalize_path(entry.path, project_dir)
        if entry_path == rel_path and entry.task_id == current_task_id:
            return FreshnessEntry(
                path=entry_path,
                content_hash=entry.content_hash,
                task_id=entry.task_id,
            )
    return None


def parse_task_meta(meta_path: Path, project_dir: Path) -> TaskMeta:
    """解析任务元数据中的文档协作字段。"""
    meta = TaskMeta()
    current_doc_target: dict[str, str] | None = None
    current_lease: dict[str, str] | None = None
    active_block = ""

    def flush_current_doc_target() -> None:
        nonlocal current_doc_target
        if current_doc_target is None:
            return
        target_path = normalize_path(current_doc_target.get("path", ""), project_dir)
        if target_path:
            meta.doc_targets.append(target_path)
            section_anchor = current_doc_target.get("section_anchor", "")
            if section_anchor:
                meta.doc_target_anchors[target_path] = section_anchor
        current_doc_target = None

    for raw_line in meta_path.read_text(encoding="utf-8").splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        indent_size = len(raw_line) - len(raw_line.lstrip(" "))

        if indent_size == 0:
            flush_current_doc_target()
            if current_lease is not None:
                meta.file_leases.append(
                    FileLease(
                        path=normalize_path(current_lease.get("path", ""), project_dir),
                        section_anchor=current_lease.get("section_anchor", ""),
                        lease_owner=current_lease.get("lease_owner", ""),
                        lease_state=current_lease.get("lease_state", "active") or "active",
                    )
                )
                current_lease = None

            active_block = ""
            if stripped_line.startswith("task_id:"):
                meta.task_id = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("status:"):
                meta.status = parse_scalar(stripped_line.split(":", 1)[1]).lower()
            elif stripped_line.startswith("section_anchor:"):
                meta.section_anchor = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line == "doc_targets:":
                active_block = "doc_targets"
            elif stripped_line == "file_leases:":
                active_block = "file_leases"
            continue

        if active_block == "doc_targets" and indent_size >= 2 and stripped_line.startswith("- "):
            flush_current_doc_target()
            item_text = stripped_line[2:].strip()
            if item_text.startswith("path:"):
                current_doc_target = {"path": parse_scalar(item_text.split(":", 1)[1])}
            else:
                parsed_path = parse_scalar(item_text)
                if parsed_path:
                    meta.doc_targets.append(normalize_path(parsed_path, project_dir))
            continue

        if active_block == "doc_targets" and indent_size >= 4 and ":" in stripped_line and current_doc_target is not None:
            key_text, value_text = stripped_line.split(":", 1)
            current_doc_target[key_text.strip()] = parse_scalar(value_text)
            continue

        if active_block == "file_leases":
            if indent_size >= 2 and stripped_line.startswith("- "):
                if current_lease is not None:
                    meta.file_leases.append(
                        FileLease(
                            path=normalize_path(current_lease.get("path", ""), project_dir),
                            section_anchor=current_lease.get("section_anchor", ""),
                            lease_owner=current_lease.get("lease_owner", ""),
                            lease_state=current_lease.get("lease_state", "active") or "active",
                        )
                    )
                current_lease = {}
                remainder_text = stripped_line[2:].strip()
                if remainder_text.startswith("path:"):
                    current_lease["path"] = parse_scalar(remainder_text.split(":", 1)[1])
                continue

            if indent_size >= 4 and ":" in stripped_line and current_lease is not None:
                key_text, value_text = stripped_line.split(":", 1)
                current_lease[key_text.strip()] = parse_scalar(value_text)

    flush_current_doc_target()
    if current_lease is not None:
        meta.file_leases.append(
            FileLease(
                path=normalize_path(current_lease.get("path", ""), project_dir),
                section_anchor=current_lease.get("section_anchor", ""),
                lease_owner=current_lease.get("lease_owner", ""),
                lease_state=current_lease.get("lease_state", "active") or "active",
            )
        )

    return meta


def load_active_task_metas(project_dir: Path) -> list[TaskMeta]:
    """加载所有活跃任务的文档协作元数据。"""
    tasks_dir = project_dir / "docs" / "plan" / "tasks"
    if not tasks_dir.exists():
        return []

    tasks: list[TaskMeta] = []
    for meta_path in sorted(tasks_dir.glob("*/.meta.yaml")):
        try:
            meta = parse_task_meta(meta_path, project_dir)
        except OSError:
            continue
        if meta.status in ACTIVE_STATUSES and meta.task_id:
            tasks.append(meta)
    return tasks


def resolve_effective_task_id(
    project_dir: Path,
    rel_path: str,
    current_task_id: str,
    secondary_task_ids: list[str],
) -> str:
    """根据目标文档路径，从主/次焦点中解析当前应生效的任务。"""
    focus_task_ids = [task_id for task_id in [current_task_id, *secondary_task_ids] if task_id]
    if not focus_task_ids:
        return current_task_id

    active_tasks = load_active_task_metas(project_dir)
    task_by_id = {task.task_id: task for task in active_tasks if task.task_id}
    for task_id in focus_task_ids:
        task_meta = task_by_id.get(task_id)
        if task_meta and task_targets_path(task_meta, rel_path):
            return task_id
    return current_task_id


def collect_anchor_ranges(content_text: str) -> list[AnchorRange]:
    """提取 BEGIN/END 锚点区块。"""
    ranges: list[AnchorRange] = []
    for match in ANCHOR_BLOCK_PATTERN.finditer(content_text):
        ranges.append(
            AnchorRange(
                name=match.group("name").strip(),
                start=match.start(),
                end=match.end(),
                generated=bool(match.group("generated")),
            )
        )
    return ranges


def find_touched_anchors(content_text: str, old_strings: list[str]) -> set[str]:
    """根据 old_string 判断当前编辑触及了哪些锚点。"""
    touched_anchors: set[str] = set()
    if not old_strings:
        return touched_anchors

    for old_text in old_strings:
        if not old_text:
            continue
        search_from = 0
        while True:
            hit_index = content_text.find(old_text, search_from)
            if hit_index < 0:
                break
            hit_end = hit_index + len(old_text)
            for anchor in collect_anchor_ranges(content_text):
                if hit_index >= anchor.start and hit_end <= anchor.end:
                    touched_anchors.add(anchor.name)
            search_from = hit_index + max(1, len(old_text))
    return touched_anchors


def find_generated_block_hit(content_text: str, old_strings: list[str]) -> str:
    """检查编辑是否触及 generated block。"""
    if not old_strings:
        return ""

    generated_ranges = [item for item in collect_anchor_ranges(content_text) if item.generated]
    if not generated_ranges:
        return ""

    for old_text in old_strings:
        if not old_text:
            continue
        search_from = 0
        while True:
            hit_index = content_text.find(old_text, search_from)
            if hit_index < 0:
                break
            hit_end = hit_index + len(old_text)
            for anchor in generated_ranges:
                if hit_index >= anchor.start and hit_end <= anchor.end:
                    return anchor.name
            search_from = hit_index + max(1, len(old_text))
    return ""


def task_targets_path(task: TaskMeta, rel_path: str) -> bool:
    """判断任务是否声明了当前文档。"""
    if rel_path in task.doc_targets:
        return True
    return any(lease.path == rel_path for lease in task.file_leases)


def task_anchor_for_path(task: TaskMeta, rel_path: str) -> str:
    """获取任务在当前文档上的锚点。"""
    for lease in task.file_leases:
        if lease.path == rel_path and lease.section_anchor:
            return lease.section_anchor
    if rel_path in task.doc_target_anchors:
        return task.doc_target_anchors[rel_path]
    return task.section_anchor


def is_active_lease(lease: FileLease) -> bool:
    """判断租约是否仍处于生效状态。"""
    return lease.lease_state.lower() not in {"released", "done", "closed", "expired"}


def check_task_conflicts(
    project_dir: Path,
    rel_path: str,
    content_text: str,
    current_task_id: str,
    old_strings: list[str],
) -> int:
    """执行任务级文档冲突检查。"""
    tasks = [task for task in load_active_task_metas(project_dir) if task_targets_path(task, rel_path)]
    if not tasks:
        return 0

    touched_anchors = find_touched_anchors(content_text, old_strings)
    leases: list[FileLease] = []
    for task in tasks:
        for lease in task.file_leases:
            if lease.path == rel_path and is_active_lease(lease):
                leases.append(lease)

    for lease in leases:
        lease_owner = lease.lease_owner or ""
        if not lease_owner:
            continue
        if lease.section_anchor:
            if lease.section_anchor in touched_anchors and lease_owner != current_task_id:
                return block(
                    "[doc_conflict_guard] section lease 冲突："
                    f"{rel_path}#{lease.section_anchor} 当前由 {lease_owner} 持有。"
                )
            continue
        if lease_owner != current_task_id:
            return block(
                f"[doc_conflict_guard] file lease 冲突：{rel_path} 当前由 {lease_owner} 持有。"
            )

    task_ids = {task.task_id for task in tasks if task.task_id}
    if len(task_ids) <= 1:
        return 0

    if not current_task_id:
        return block(
            "[doc_conflict_guard] 文档冲突：多个活跃任务同时声明了 "
            f"{rel_path}，但 MANIFEST.current_focus.task_id 为空。"
        )

    if current_task_id not in task_ids:
        joined_ids = ", ".join(sorted(task_ids))
        return block(
            "[doc_conflict_guard] 文档冲突：当前任务 "
            f"{current_task_id} 未持有 {rel_path} 的写入权限，活跃任务为 {joined_ids}。"
        )

    lease_task_ids = {
        task.task_id
        for task in tasks
        if task.task_id and any(lease.path == rel_path and is_active_lease(lease) for lease in task.file_leases)
    }
    if lease_task_ids != task_ids:
        return block(
            "[doc_conflict_guard] 文档冲突：多个活跃任务同时声明了 "
            f"{rel_path}，advanced 模式下每个任务都必须声明 file_leases。"
        )

    current_owned_leases = [
        lease for lease in leases if (lease.lease_owner or current_task_id) == current_task_id
    ]
    if current_owned_leases:
        owned_anchors = {lease.section_anchor for lease in current_owned_leases if lease.section_anchor}
        if touched_anchors and owned_anchors and not touched_anchors.issubset(owned_anchors):
            return block(
                "[doc_conflict_guard] section lease 越界："
                f"{rel_path} 当前任务仅持有 {', '.join(sorted(owned_anchors))}，"
                f"但补丁命中了 {', '.join(sorted(touched_anchors))}。"
            )
        overlapping_leases = []
        for lease in leases:
            if (lease.lease_owner or "") == current_task_id:
                continue
            if not lease.section_anchor:
                overlapping_leases.append(lease)
                continue
            if not owned_anchors or lease.section_anchor in owned_anchors:
                overlapping_leases.append(lease)
        if not overlapping_leases:
            return 0

    return block(
        "[doc_conflict_guard] 文档冲突：多个活跃任务同时声明了 "
        f"{rel_path}，请补充 section_anchor / file_leases 或改为串行。"
    )


def handle_read(
    project_dir: Path,
    target_path: Path,
    rel_path: str,
    current_task_id: str,
) -> int:
    """在读取文档时刷新新鲜度快照。"""
    if not current_task_id or not target_path.exists():
        return 0

    content_hash = update_freshness_snapshot(project_dir, rel_path, current_task_id)
    print(
        f"[doc_conflict_guard] freshness snapshot updated: {rel_path} ({content_hash})",
        file=sys.stderr,
    )
    return 0


def handle_write_like(
    project_dir: Path,
    target_path: Path,
    rel_path: str,
    current_task_id: str,
    old_strings: list[str],
) -> int:
    """在编辑前执行新鲜度与冲突检查。"""
    if not target_path.exists():
        return 0

    content_text = target_path.read_text(encoding="utf-8")
    manifest_text = load_manifest_text(project_dir)
    _, _, entries = parse_manifest_state(manifest_text)

    if current_task_id:
        freshness_entry = find_freshness_entry(entries, project_dir, rel_path, current_task_id)
        if freshness_entry is not None:
            current_hash = compute_content_hash(target_path)
            if freshness_entry.content_hash != current_hash:
                return block(
                    "[doc_conflict_guard] freshness 冲突："
                    f"{rel_path} 已发生变化，请先重新读取最新文件后再修改。"
                )

    generated_name = find_generated_block_hit(content_text, old_strings)
    if generated_name:
        return block(
            "[doc_conflict_guard] generated block 冲突："
            f"{rel_path}#{generated_name} 属于生成区块，请改生成源或更换锚点。"
        )

    active_tasks = load_active_task_metas(project_dir)
    current_task = next(
        (task for task in active_tasks if task.task_id == current_task_id),
        None,
    )
    if len(content_text.splitlines()) > 200:
        declared_anchor = task_anchor_for_path(current_task, rel_path) if current_task else ""
        touched_anchors = find_touched_anchors(content_text, old_strings)
        if not old_strings:
            return block(
                "[doc_conflict_guard] 大文档编辑必须是 section 级 patch，"
                f"{rel_path} 不允许整页重写。"
            )
        if not declared_anchor:
            return block(
                "[doc_conflict_guard] 大文档编辑需要先声明 section_anchor，"
                f"{rel_path} 当前任务未声明可编辑 section。"
            )
        if not touched_anchors:
            return block(
                "[doc_conflict_guard] 大文档编辑必须命中稳定锚点，"
                f"{rel_path} 当前补丁未命中任何 section。"
            )
        if len(touched_anchors) > 1:
            return block(
                "[doc_conflict_guard] 一个任务一次只允许改一个 section，"
                f"{rel_path} 当前命中了多个锚点：{', '.join(sorted(touched_anchors))}。"
            )
        if touched_anchors != {declared_anchor}:
            return block(
                "[doc_conflict_guard] section_anchor 不匹配："
                f"任务声明 `{declared_anchor}`，但补丁实际命中了 "
                f"`{', '.join(sorted(touched_anchors))}`。"
            )

    return check_task_conflicts(project_dir, rel_path, content_text, current_task_id, old_strings)


def main() -> int:
    """脚本入口。"""
    configure_stderr()
    payload = load_payload()
    tool_name = extract_tool_name(payload)
    tool_input = extract_tool_input(payload)

    if tool_name not in {"Read", "Edit", "Write", "MultiEdit"}:
        return 0

    file_path_text = extract_file_path(tool_input)
    if not file_path_text:
        return 0

    project_dir = get_project_dir()
    target_path = Path(file_path_text)
    if not target_path.is_absolute():
        target_path = (project_dir / target_path).resolve()
    else:
        target_path = target_path.resolve()

    if not is_document_path(target_path):
        return 0

    rel_path = normalize_path(str(target_path), project_dir)
    session_task_id = load_session_focus_task_id(project_dir)
    if not session_task_id:
        # 无 session focus 时放行（MANIFEST 不再作为运行时真相源）
        return 0
    effective_task_id = resolve_effective_task_id(
        project_dir,
        rel_path,
        session_task_id,
        [],
    )

    if tool_name == "Read":
        return handle_read(project_dir, target_path, rel_path, effective_task_id)

    old_strings = extract_old_strings(tool_input)
    return handle_write_like(project_dir, target_path, rel_path, effective_task_id, old_strings)


if __name__ == "__main__":
    raise SystemExit(main())
