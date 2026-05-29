#!/usr/bin/env python3
"""PreToolUse hook：任务范围与并发泳道门禁。

目标：
1. normal 模式下，写入必须命中当前任务的 `allowed_paths`
2. advanced 模式下，要求最小字段齐备，并校验 `lane_key` 串行规则
3. 在明显需要升级 advanced 的场景下，阻断并提示补齐控制面字段
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


WRITE_TOOLS = {"Edit", "Write", "MultiEdit"}
ACTIVE_STATUSES = {"doing", "in_review", "approved", "queued"}

# 代码文件扩展名：只有代码文件才需要 scope guard 保护
CODE_EXTENSIONS = {
    ".py", ".pyw",
    ".cpp", ".hpp", ".c", ".h",
    ".js", ".ts", ".jsx", ".tsx",
    ".java", ".kt", ".scala",
    ".rs", ".go", ".rb",
    ".cs", ".fs", ".vb",
    ".swift", ".m", ".mm",
    ".sh", ".bash", ".ps1",
    ".sql", ".cmake",
}


class TaskMeta:
    """任务元数据的轻量容器。"""

    def __init__(self) -> None:
        self.task_id: str = ""
        self.status: str = ""
        self.allowed_paths: list[str] = []
        self.lane_key: str = ""
        self.approval_targets: dict[str, str] = {}
        self.has_file_leases: bool = False
        self.route_key: str = ""

    @property
    def has_approval_target(self) -> bool:
        return any(value.strip() for value in self.approval_targets.values())

    @property
    def is_advanced(self) -> bool:
        return bool(
            self.lane_key
            or self.has_approval_target
            or self.has_file_leases
        )


def configure_stderr() -> None:
    """将 stderr 调整为 UTF-8。"""
    try:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


def block(message_text: str) -> int:
    """统一阻断输出。"""
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
        value_text = tool_input.get(key_name)
        if isinstance(value_text, str) and value_text.strip():
            return value_text.strip()
    return ""


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


def load_manifest_focus_task_ids(project_dir: Path) -> list[str]:
    """读取焦点任务列表（只读 session focus.json，不回退 MANIFEST）。"""
    focus_path = get_session_focus_path(project_dir)
    task_id = ""
    if focus_path.exists():
        try:
            payload = json.loads(focus_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        if isinstance(payload, dict):
            task_id = str(payload.get("task_id") or "").strip()
    return [task_id] if task_id else []


def load_manifest_current_task_id(project_dir: Path) -> str:
    """读取当前会话主 focus 任务。"""
    focus_task_ids = load_manifest_focus_task_ids(project_dir)
    return focus_task_ids[0] if focus_task_ids else ""


def load_collaboration_mode(project_dir: Path) -> str:
    """读取协作模式。"""
    pref_path = project_dir / ".claude" / "preferences.json"
    try:
        payload = json.loads(pref_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "normal"
    mode_text = str(payload.get("collaboration_mode", "normal")).strip().lower()
    return mode_text if mode_text in {"normal", "advanced"} else "normal"


def parse_task_meta(meta_path: Path, project_dir: Path) -> TaskMeta:
    """解析任务元数据的最小字段。"""
    task_meta = TaskMeta()
    active_block = ""

    for raw_line in meta_path.read_text(encoding="utf-8").splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        indent_size = len(raw_line) - len(raw_line.lstrip(" "))

        if indent_size == 0:
            active_block = ""
            if stripped_line.startswith("task_id:"):
                task_meta.task_id = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("status:"):
                task_meta.status = parse_scalar(stripped_line.split(":", 1)[1]).lower()
            elif stripped_line.startswith("lane_key:"):
                task_meta.lane_key = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("route_key:"):
                task_meta.route_key = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line == "allowed_paths:":
                active_block = "allowed_paths"
            elif stripped_line == "approval_target:":
                active_block = "approval_target"
            elif stripped_line.startswith("file_leases:"):
                task_meta.has_file_leases = True
                active_block = "file_leases"
            continue

        if active_block == "allowed_paths" and indent_size >= 2 and stripped_line.startswith("- "):
            path_text = parse_scalar(stripped_line[2:])
            if path_text:
                task_meta.allowed_paths.append(normalize_path(path_text, project_dir))
            continue

        if active_block == "approval_target" and indent_size >= 2 and ":" in stripped_line:
            key_text, value_text = stripped_line.split(":", 1)
            parsed_value = parse_scalar(value_text)
            if parsed_value:
                task_meta.approval_targets[key_text.strip()] = parsed_value

    if not task_meta.task_id:
        task_meta.task_id = meta_path.parent.name.split("-", 1)[0]
    return task_meta


def load_active_tasks(project_dir: Path) -> list[TaskMeta]:
    """加载所有活跃任务。"""
    tasks_dir = project_dir / "docs" / "plan" / "tasks"
    if not tasks_dir.exists():
        return []

    active_tasks: list[TaskMeta] = []
    for meta_path in sorted(tasks_dir.glob("*/.meta.yaml")):
        try:
            task_meta = parse_task_meta(meta_path, project_dir)
        except OSError:
            continue
        if task_meta.task_id and task_meta.status in ACTIVE_STATUSES:
            active_tasks.append(task_meta)
    return active_tasks


def path_matches_scope(rel_path: str, scope_path: str) -> bool:
    """判断目标路径是否命中某个 allowed_path。"""
    normalized_scope = scope_path.strip().strip("/")
    if not normalized_scope:
        return False
    if rel_path == normalized_scope:
        return True
    return rel_path.startswith(f"{normalized_scope}/")


def task_allows_path(task_meta: TaskMeta, rel_path: str) -> bool:
    """判断任务是否允许写入该路径。"""
    return any(path_matches_scope(rel_path, scope_path) for scope_path in task_meta.allowed_paths)


def find_matching_tasks(tasks: list[TaskMeta], rel_path: str) -> list[TaskMeta]:
    """找到所有允许写入当前路径的活跃任务。"""
    return [task_meta for task_meta in tasks if task_allows_path(task_meta, rel_path)]


def validate_lane_serialization(current_task: TaskMeta, active_tasks: list[TaskMeta]) -> int:
    """校验 advanced 模式的 lane 串行规则。"""
    if not current_task.lane_key:
        return block(
            f"[task_scope_guard] 任务 {current_task.task_id} 已进入 advanced，但缺少 lane_key。"
        )
    if not current_task.has_file_leases:
        return block(
            f"[task_scope_guard] 任务 {current_task.task_id} 已进入 advanced，但缺少 file_leases。"
        )
    if not current_task.has_approval_target:
        return block(
            f"[task_scope_guard] 任务 {current_task.task_id} 已进入 advanced，但缺少 approval_target。"
        )

    conflicting_tasks = [
        task_meta.task_id
        for task_meta in active_tasks
        if task_meta.task_id != current_task.task_id
        and task_meta.status == "doing"
        and task_meta.lane_key
        and task_meta.lane_key == current_task.lane_key
    ]
    if conflicting_tasks:
        joined_ids = ", ".join(conflicting_tasks)
        return block(
            "[task_scope_guard] lane_key 串行门禁："
            f"{current_task.lane_key} 当前已有 doing 任务 {joined_ids}，"
            f"请先串行推进，再让 {current_task.task_id} 写入。"
        )
    return 0


# 管理性路径白名单：这些路径始终允许写入，不受 allowed_paths 限制
ADMIN_PATH_PREFIXES = (
    ".claude/state/",          # MANIFEST、.gate-approved 等
    "docs/plan/tasks/",        # 任务元数据（.meta.yaml、steps.md 等）
    ".claude/memory/lessons/", # 教训文件
)


def is_code_file(rel_path: str) -> bool:
    """判断是否为代码文件（需要 scope guard 保护）。文档/配置文件免检。"""
    import os
    _, ext = os.path.splitext(rel_path)
    return ext.lower() in CODE_EXTENSIONS


def main() -> int:
    """脚本入口。"""
    configure_stderr()
    payload = load_payload()
    tool_name = extract_tool_name(payload)
    if tool_name not in WRITE_TOOLS:
        return 0

    tool_input = extract_tool_input(payload)
    file_path_text = extract_file_path(tool_input)
    if not file_path_text:
        return 0

    project_dir = get_project_dir()
    target_path = Path(file_path_text)
    if not target_path.is_absolute():
        target_path = (project_dir / target_path).resolve()
    else:
        target_path = target_path.resolve()
    rel_path = normalize_path(str(target_path), project_dir)

    # 非代码文件免检（文档、配置、计划等）
    if not is_code_file(rel_path):
        return 0

    active_tasks = load_active_tasks(project_dir)
    if not active_tasks:
        return 0

    focus_task_ids = load_manifest_focus_task_ids(project_dir)
    current_task_id = focus_task_ids[0] if focus_task_ids else ""
    if not current_task_id:
        # 无 session focus 时放行（MANIFEST 不再作为运行时真相源）
        return 0

    focus_tasks = [task_meta for task_meta in active_tasks if task_meta.task_id in set(focus_task_ids)]
    current_task = next((task_meta for task_meta in focus_tasks if task_meta.task_id == current_task_id), None)
    if current_task is None:
        return block(
            f"[task_scope_guard] 当前任务 {current_task_id} 不在活跃任务列表中，请先修正 .meta.yaml 或 MANIFEST。"
        )

    if any(not task_meta.allowed_paths for task_meta in focus_tasks):
        missing_ids = ", ".join(task_meta.task_id for task_meta in focus_tasks if not task_meta.allowed_paths)
        return block(
            f"[task_scope_guard] 任务 {missing_ids} 缺少 allowed_paths，normal/advanced 都不能放行写入。"
        )

    if not any(task_allows_path(task_meta, rel_path) for task_meta in focus_tasks):
        joined_scopes = "; ".join(
            f"{task_meta.task_id}: {', '.join(task_meta.allowed_paths)}" for task_meta in focus_tasks
        )
        return block(
            "[task_scope_guard] allowed_paths 越界："
            f"{rel_path} 不在当前焦点任务集合的允许范围内（{joined_scopes}）。"
        )

    matching_tasks = find_matching_tasks(active_tasks, rel_path)
    collaboration_mode = load_collaboration_mode(project_dir)
    requires_advanced = (
        collaboration_mode == "advanced"
        or current_task.is_advanced
        or len(active_tasks) >= 3
        or len(matching_tasks) >= 2
    )

    if len(matching_tasks) >= 2 and not current_task.is_advanced and collaboration_mode != "advanced":
        task_ids = ", ".join(task_meta.task_id for task_meta in matching_tasks)
        return block(
            "[task_scope_guard] 检测到同一路径被多个活跃任务声明："
            f"{rel_path} <- {task_ids}。"
            " 请升级 advanced，并补齐 lane_key / file_leases / approval_target。"
        )

    if len(active_tasks) >= 3 and not current_task.is_advanced and collaboration_mode != "advanced":
        return block(
            "[task_scope_guard] 当前活跃任务数已达到 3 个以上。"
            f" 请将任务 {current_task.task_id} 升级到 advanced，并补齐 lane_key / file_leases / approval_target。"
        )

    if requires_advanced:
        return validate_lane_serialization(current_task, active_tasks)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
