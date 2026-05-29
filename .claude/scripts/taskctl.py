#!/usr/bin/env python3
"""Coordinator 控制脚本：维护任务状态机、MANIFEST 焦点和 merge queue。"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


ACTIVE_STATUSES = {"doing", "in_review", "approved", "queued"}
TRANSITION_RULES = {
    "doing": {"todo", "blocked"},
    "in_review": {"doing"},
    "approved": {"in_review"},
    "queued": {"approved"},
    "merged": {"queued"},
}
STATUS_ORDER = ["merged", "doing", "todo", "in_review", "approved", "queued", "blocked"]
PLAN_STATUS_BEGIN = "<!-- BEGIN:plan-status-summary -->"
PLAN_STATUS_END = "<!-- END:plan-status-summary -->"
PLAN_TABLE_BEGIN = "<!-- BEGIN:plan-task-table -->"
PLAN_TABLE_END = "<!-- END:plan-task-table -->"
PLAN_QUEUE_BEGIN = "<!-- BEGIN:plan-merge-queue -->"
PLAN_QUEUE_END = "<!-- END:plan-merge-queue -->"
DEFAULT_AUTO_APPROVAL_TARGET = {
    "gate": "coordinator",
    "review": "reviewer",
    "merge": "merge-owner",
}
DEFAULT_AUTO_ADVANCED_PARALLEL_LIMIT = 3
SEVERITY_ORDER = {
    "blocker": 0,
    "major": 1,
    "minor": 2,
    "question": 3,
}
VALID_REVIEW_DECISIONS = {"approved", "changes_requested", "blocked"}
REVIEW_TRACK_TEMPLATES: dict[str, list[dict[str, object]]] = {
    "code": [
        {
            "slug": "correctness",
            "title": "功能正确性",
            "summary": "确认实现是否真正满足需求与验收标准。",
            "questions": [
                "核心行为是否与需求、计划和验收标准一致？",
                "是否存在明显的边界条件或错误分支遗漏？",
                "是否引入了与当前任务无关的额外行为？",
            ],
            "checklist": [
                "对照 plan / acceptance 检查主流程",
                "检查空输入、异常路径和回退行为",
                "标出 blocker / major / minor / question",
            ],
        },
        {
            "slug": "regression",
            "title": "测试与回归缺口",
            "summary": "确认验证覆盖是否足够，是否存在高风险回归盲区。",
            "questions": [
                "现有测试是否覆盖本次改动的主路径和长尾路径？",
                "是否存在未被验证的回归风险或兼容性风险？",
                "验证命令、测试数据和断言是否足够说明问题？",
            ],
            "checklist": [
                "检查测试文件和验证命令",
                "检查新增路径是否有对应断言",
                "列出缺失测试或验证证据不足点",
            ],
        },
        {
            "slug": "architecture",
            "title": "架构与边界一致性",
            "summary": "确认改动是否遵守当前代码库的结构约束与职责边界。",
            "questions": [
                "模块职责是否仍然清晰，是否出现跨层泄漏？",
                "命名、模式、依赖方向是否与现有代码一致？",
                "是否引入未来维护成本明显偏高的实现？",
            ],
            "checklist": [
                "检查职责边界和依赖方向",
                "检查命名、风格和公共接口一致性",
                "指出需要回到 plan 级修正的问题",
            ],
        },
    ],
    "algorithm": [
        {
            "slug": "semantics",
            "title": "规格语义",
            "summary": "确认算法含义、阈值语义和触发条件被正确理解。",
            "questions": [
                "规格文本里的术语、阈值和动作条件是否被正确解释？",
                "是否存在同名字段、同义词或歧义语句未澄清？",
                "输出语义是否与期望一致？",
            ],
            "checklist": [
                "对照规格逐条核语义",
                "检查阈值与触发条件定义",
                "标出歧义和待补证据点",
            ],
        },
        {
            "slug": "evidence",
            "title": "阈值与数据证据",
            "summary": "确认参数、阈值和判定逻辑有足够数据或经验依据。",
            "questions": [
                "阈值、默认参数和规则是否有证据支撑？",
                "样例、实验或历史数据是否足够说明当前方案？",
                "是否存在参数拍脑袋或证据链断裂？",
            ],
            "checklist": [
                "检查参数与阈值来源",
                "检查实验、样例和验证数据",
                "指出证据缺失或不充分之处",
            ],
        },
        {
            "slug": "alignment",
            "title": "实现对齐",
            "summary": "确认规格、实现、测试和输出字段彼此对齐。",
            "questions": [
                "实现行为是否真正对应规格与输出定义？",
                "测试断言是否覆盖关键行为和异常路径？",
                "配置、代码和文档之间是否出现漂移？",
            ],
            "checklist": [
                "对照规格、实现、测试三方",
                "检查输出字段和默认值对齐",
                "指出实现漂移和同步缺口",
            ],
        },
    ],
    "document": [
        {
            "slug": "readability",
            "title": "结构可读性",
            "summary": "确认文档结构是否清晰、导航是否顺畅、信息分层是否合理。",
            "questions": [
                "读者是否能快速找到入口、步骤和结论？",
                "章节划分、标题层级和示例顺序是否合理？",
                "是否存在整段堆砌、重复描述或难以导航的部分？",
            ],
            "checklist": [
                "检查标题层级和目录结构",
                "检查示例与说明顺序",
                "指出冗长、重复或跳跃位置",
            ],
        },
        {
            "slug": "consistency",
            "title": "事实一致性",
            "summary": "确认文档表述与当前配置、代码和其他主入口文档一致。",
            "questions": [
                "路径、命令、数量和状态描述是否与仓库现状一致？",
                "是否存在旧路径、旧命令或已失效表述残留？",
                "多处入口对同一机制的描述是否一致？",
            ],
            "checklist": [
                "对照关键文件和配置",
                "检查状态描述和命名一致性",
                "标出冲突表述和漂移点",
            ],
        },
        {
            "slug": "links",
            "title": "路径与链接漂移",
            "summary": "确认链接、文件引用和命令入口没有失效或漂移。",
            "questions": [
                "路径、文件名和引用文档是否真实存在？",
                "是否存在历史重命名后的旧引用残留？",
                "命令示例和入口文件是否仍可执行或可定位？",
            ],
            "checklist": [
                "检查链接和路径存在性",
                "检查命令入口与文件引用",
                "标出失效链接和迁移缺口",
            ],
        },
    ],
    "mixed": [
        {
            "slug": "correctness",
            "title": "方案正确性",
            "summary": "确认整体方案是否满足目标与约束。",
            "questions": [
                "方案是否真正响应了需求目标？",
                "关键约束、边界和依赖是否被正确处理？",
                "是否遗漏了会改变结论的重要前提？",
            ],
            "checklist": [
                "检查目标、范围与约束",
                "检查关键路径和边界条件",
                "标出阻塞性偏差",
            ],
        },
        {
            "slug": "risk",
            "title": "实现风险",
            "summary": "确认方案落地时的技术风险、回归风险和维护风险。",
            "questions": [
                "当前方案落地时最大的失败点是什么？",
                "是否存在顺序依赖、环境依赖或集成风险？",
                "哪些风险需要前置验证或拆分任务？",
            ],
            "checklist": [
                "检查实现风险和依赖风险",
                "检查并行、顺序和集成风险",
                "给出优先级最高的风险项",
            ],
        },
        {
            "slug": "evidence",
            "title": "验证与证据闭环",
            "summary": "确认结论是否有足够验证与证据支持。",
            "questions": [
                "当前结论有哪些直接证据支持？",
                "是否还缺测试、截图、日志或实验结果？",
                "哪些结论只是推断，哪些是已验证事实？",
            ],
            "checklist": [
                "检查验证命令和证据材料",
                "区分已验证事实与推断",
                "指出证据链缺口",
            ],
        },
    ],
}


@dataclass
class TaskMeta:
    """任务元数据。"""

    task_id: str
    title: str
    owner_agent: str
    mode: str
    status: str
    allowed_paths: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    doc_targets: list[tuple[str, str]] = field(default_factory=list)
    branch_or_workspace: str = ""
    lane_key: str = ""
    section_anchor: str = ""
    approval_target: dict[str, str] = field(default_factory=dict)
    review_state: str = ""
    merge_state: str = ""
    blocked_from: str = ""
    blocked_reason: str = ""
    blocked_by: str = ""
    blocked_at: str = ""
    updated_at: str = ""
    has_file_leases: bool = False
    task_dir: Path | None = None

    @property
    def is_advanced(self) -> bool:
        return bool(self.lane_key or self.approval_target or self.has_file_leases)


@dataclass
class QueueItem:
    """merge queue 条目。"""

    task_id: str
    merge_ref: str
    queued_at: str


@dataclass
class PreflightReport:
    """任务预检报告。"""

    task_id: str
    title: str
    status: str
    current_collaboration_mode: str
    recommended_collaboration_mode: str
    ready_to_start: bool
    active_task_count: int
    suggested_lane_key: str
    path_overlap_with: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)


@dataclass
class RouteReport:
    """任务草案路由建议。"""

    recommended_collaboration_mode: str
    recommended_execution_mode: str
    recommended_create_flag: str
    active_task_count: int
    path_overlap_with: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)


@dataclass
class ReviewFinding:
    """单条 reviewer 发现。"""

    severity: str
    text: str
    normalized_text: str
    reviewer_task_id: str
    reviewer_title: str
    track_title: str


@dataclass
class ReviewerSummary:
    """单个 reviewer 汇总结果。"""

    task_id: str
    title: str
    track_title: str
    conclusion: str
    evidence: str
    suggested_action: str
    findings: list[ReviewFinding] = field(default_factory=list)


@dataclass
class AggregatedIssue:
    """汇总后的问题项。"""

    text: str
    severity: str
    sources: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class ReviewAggregateResult:
    """多 reviewer 汇总结果。"""

    title: str
    final_decision: str
    reviewers: list[ReviewerSummary]
    consensus_issues: list[AggregatedIssue]
    single_high_value_issues: list[AggregatedIssue]
    divergence_notes: list[str]


def now_iso() -> str:
    """返回本地时区 ISO 时间。"""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def quote_yaml(value_text: str) -> str:
    """输出安全的 YAML 字符串。"""
    escaped_text = value_text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped_text}"'


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


def normalize_path(path_text: str) -> str:
    """标准化路径。"""
    normalized_text = path_text.strip().replace("\\", "/")
    while normalized_text.startswith("./"):
        normalized_text = normalized_text[2:]
    return normalized_text.strip("/")


def slugify_topic(topic_text: str) -> str:
    """将 topic 转为目录 slug。"""
    slug_text = re.sub(r"[^a-z0-9]+", "-", topic_text.strip().lower())
    slug_text = slug_text.strip("-")
    return slug_text or "task"


def validate_task_id(task_id: str) -> str:
    """校验任务 ID 格式。"""
    normalized_id = task_id.strip().upper()
    if not re.fullmatch(r"T\d{3}", normalized_id):
        raise ValueError(f"非法 task_id：{task_id}，格式必须为 T001")
    return normalized_id


def resolve_task_date(date_text: str) -> str:
    """解析任务日期。"""
    if date_text:
        try:
            return datetime.strptime(date_text, "%Y-%m-%d").date().isoformat()
        except ValueError as exc:
            raise ValueError(f"非法日期：{date_text}，格式必须为 YYYY-MM-DD") from exc
    return datetime.now().astimezone().date().isoformat()


def build_task_dir_name(task_id: str, task_date: str, topic_text: str) -> str:
    """构造任务目录名。"""
    return f"{task_id}-{task_date}-{slugify_topic(topic_text)}"


def allocate_next_task_id(project_dir: Path) -> str:
    """分配下一个任务 ID。"""
    max_index = 0
    for task_meta in list_task_meta(project_dir):
        matched = re.fullmatch(r"T(\d{3})", task_meta.task_id)
        if not matched:
            continue
        max_index = max(max_index, int(matched.group(1)))
    return f"T{max_index + 1:03d}"


def split_anchor_ref(raw_text: str, field_name: str) -> tuple[str, str]:
    """解析 path#section_anchor 结构。"""
    path_text, separator, anchor_text = raw_text.partition("#")
    normalized_path = normalize_path(path_text)
    normalized_anchor = anchor_text.strip()
    if not separator or not normalized_path or not normalized_anchor:
        raise ValueError(f"{field_name} 必须使用 path#section_anchor 格式：{raw_text}")
    return normalized_path, normalized_anchor


def format_allowed_paths(allowed_paths: list[str]) -> str:
    """格式化允许路径列表。"""
    normalized_paths = [path for path in allowed_paths if path]
    if not normalized_paths:
        return "—"
    return "<br>".join(f"`{path}`" for path in normalized_paths)


def load_taskctl_config(project_dir: Path) -> dict[str, object]:
    """读取 taskctl 项目配置。"""
    config_data = {
        "auto_advanced": {
            "parallel_active_task_limit": DEFAULT_AUTO_ADVANCED_PARALLEL_LIMIT,
            "approval_target": dict(DEFAULT_AUTO_APPROVAL_TARGET),
        }
    }
    for file_name in ("taskctl.json", "taskctl.local.json"):
        config_path = project_dir / ".claude" / file_name
        if not config_path.exists():
            continue
        raw_data = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(raw_data, dict):
            continue
        auto_advanced_data = raw_data.get("auto_advanced")
        if not isinstance(auto_advanced_data, dict):
            continue
        parallel_limit = auto_advanced_data.get("parallel_active_task_limit")
        if isinstance(parallel_limit, int) and parallel_limit >= 2:
            config_data["auto_advanced"]["parallel_active_task_limit"] = parallel_limit
        approval_data = auto_advanced_data.get("approval_target")
        if isinstance(approval_data, dict):
            for key_text in ("gate", "review", "merge"):
                value_text = approval_data.get(key_text)
                if isinstance(value_text, str) and value_text.strip():
                    config_data["auto_advanced"]["approval_target"][key_text] = value_text.strip()
    return config_data


def get_parallel_active_task_limit(config_data: dict[str, object]) -> int:
    """读取 auto advanced 并行升级阈值。"""
    auto_advanced_data = config_data.get("auto_advanced", {})
    if isinstance(auto_advanced_data, dict):
        value = auto_advanced_data.get("parallel_active_task_limit")
        if isinstance(value, int) and value >= 2:
            return value
    return DEFAULT_AUTO_ADVANCED_PARALLEL_LIMIT


def get_default_approval_target(config_data: dict[str, object]) -> dict[str, str]:
    """读取 auto advanced 审批目标默认值。"""
    approval_target = dict(DEFAULT_AUTO_APPROVAL_TARGET)
    auto_advanced_data = config_data.get("auto_advanced", {})
    if isinstance(auto_advanced_data, dict):
        approval_data = auto_advanced_data.get("approval_target")
        if isinstance(approval_data, dict):
            for key_text in ("gate", "review", "merge"):
                value_text = approval_data.get(key_text)
                if isinstance(value_text, str) and value_text.strip():
                    approval_target[key_text] = value_text.strip()
    return approval_target


def format_queue_items(queue_items: list[QueueItem]) -> str:
    """序列化 merge queue。"""
    lines = [
        "# MERGE_QUEUE.yaml — 并行任务合并队列",
        "# 说明：由 .claude/scripts/taskctl.py 维护；手工编辑前请先确认没有并行会话同时操作。",
        "",
        "version: 1",
        f"updated_at: {quote_yaml(now_iso())}",
        "items:",
    ]
    if not queue_items:
        lines.append("  []")
        return "\n".join(lines) + "\n"

    for item in queue_items:
        lines.extend(
            [
                f'  - task_id: {quote_yaml(item.task_id)}',
                f'    merge_ref: {quote_yaml(item.merge_ref)}',
                f'    queued_at: {quote_yaml(item.queued_at)}',
            ]
        )
    return "\n".join(lines) + "\n"


def load_queue(queue_path: Path) -> list[QueueItem]:
    """读取 merge queue。"""
    if not queue_path.exists():
        return []

    queue_items: list[QueueItem] = []
    current_item: dict[str, str] | None = None
    in_items = False
    for raw_line in queue_path.read_text(encoding="utf-8").splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        indent_size = len(raw_line) - len(raw_line.lstrip(" "))
        if indent_size == 0:
            in_items = stripped_line == "items:"
            continue
        if not in_items:
            continue
        if indent_size == 2 and stripped_line == "[]":
            return []
        if indent_size == 2 and stripped_line.startswith("- "):
            if current_item:
                queue_items.append(
                    QueueItem(
                        task_id=current_item.get("task_id", ""),
                        merge_ref=current_item.get("merge_ref", ""),
                        queued_at=current_item.get("queued_at", ""),
                    )
                )
            current_item = {}
            remainder_text = stripped_line[2:].strip()
            if ":" in remainder_text:
                key_text, value_text = remainder_text.split(":", 1)
                current_item[key_text.strip()] = parse_scalar(value_text)
            continue
        if current_item is not None and indent_size >= 4 and ":" in stripped_line:
            key_text, value_text = stripped_line.split(":", 1)
            current_item[key_text.strip()] = parse_scalar(value_text)
    if current_item:
        queue_items.append(
            QueueItem(
                task_id=current_item.get("task_id", ""),
                merge_ref=current_item.get("merge_ref", ""),
                queued_at=current_item.get("queued_at", ""),
            )
        )
    return [item for item in queue_items if item.task_id]


def write_queue(queue_path: Path, queue_items: list[QueueItem]) -> None:
    """写回 merge queue。"""
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(format_queue_items(queue_items), encoding="utf-8")


def replace_between_markers(source_text: str, begin_marker: str, end_marker: str, block_text: str) -> str:
    """替换标记块内容。"""
    pattern = re.compile(
        rf"{re.escape(begin_marker)}.*?{re.escape(end_marker)}",
        flags=re.DOTALL,
    )
    replacement_text = f"{begin_marker}\n{block_text.rstrip()}\n{end_marker}"
    if pattern.search(source_text):
        return pattern.sub(replacement_text, source_text, count=1)
    return f"{source_text.rstrip()}\n\n{replacement_text}\n"


def replace_section(source_text: str, header_text: str, next_header_text: str, section_body: str) -> str:
    """替换标题之间的整段内容。"""
    pattern = re.compile(
        rf"({re.escape(header_text)}\n\n).*?(?=\n{re.escape(next_header_text)})",
        flags=re.DOTALL,
    )
    replacement_text = f"\\1{section_body.rstrip()}\n"
    if pattern.search(source_text):
        return pattern.sub(replacement_text, source_text, count=1)
    return source_text


def update_top_level_scalar(meta_text: str, key_text: str, value_text: str) -> str:
    """更新或追加顶层标量。"""
    pattern = re.compile(rf"(?m)^{re.escape(key_text)}:\s*.*$")
    replacement_text = f"{key_text}: {value_text}"
    if pattern.search(meta_text):
        return pattern.sub(replacement_text, meta_text, count=1)
    suffix = "" if meta_text.endswith("\n") else "\n"
    return f"{meta_text}{suffix}{replacement_text}\n"


def update_top_level_block(meta_text: str, key_text: str, block_lines: list[str]) -> str:
    """更新或追加顶层块。"""
    block_text = "\n".join(block_lines).rstrip() + "\n"
    pattern = re.compile(
        rf"(?ms)^{re.escape(key_text)}:.*?(?=^[A-Za-z0-9_]+:|\Z)"
    )
    if pattern.search(meta_text):
        return pattern.sub(block_text, meta_text, count=1)
    suffix = "" if meta_text.endswith("\n") else "\n"
    return f"{meta_text}{suffix}{block_text}"


def parse_meta(meta_path: Path) -> TaskMeta:
    """读取任务元数据。"""
    raw_text = meta_path.read_text(encoding="utf-8")
    task_dir = meta_path.parent
    task_id = ""
    title = ""
    owner_agent = ""
    mode = ""
    status = ""
    branch_or_workspace = ""
    lane_key = ""
    section_anchor = ""
    review_state = ""
    merge_state = ""
    blocked_from = ""
    blocked_reason = ""
    blocked_by = ""
    blocked_at = ""
    updated_at = ""
    allowed_paths: list[str] = []
    depends_on: list[str] = []
    doc_targets: list[tuple[str, str]] = []
    approval_target: dict[str, str] = {}
    has_file_leases = False
    active_block = ""
    current_doc_target: dict[str, str] | None = None

    for raw_line in raw_text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            continue
        indent_size = len(raw_line) - len(raw_line.lstrip(" "))
        if indent_size == 0:
            if active_block == "doc_targets" and current_doc_target:
                path_text = normalize_path(current_doc_target.get("path", ""))
                anchor_text = current_doc_target.get("section_anchor", "").strip()
                if path_text and anchor_text:
                    doc_targets.append((path_text, anchor_text))
                current_doc_target = None
            active_block = ""
            if stripped_line.startswith("task_id:"):
                task_id = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("title:"):
                title = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("name:") and not title:
                title = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("owner_agent:"):
                owner_agent = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("agent:") and not owner_agent:
                owner_agent = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("mode:"):
                mode = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("status:"):
                status = parse_scalar(stripped_line.split(":", 1)[1]).lower()
            elif stripped_line.startswith("branch_or_workspace:"):
                branch_or_workspace = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("branch:") and not branch_or_workspace:
                branch_or_workspace = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("lane_key:"):
                lane_key = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("section_anchor:"):
                section_anchor = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("review_state:"):
                review_state = parse_scalar(stripped_line.split(":", 1)[1]).lower()
            elif stripped_line.startswith("merge_state:"):
                merge_state = parse_scalar(stripped_line.split(":", 1)[1]).lower()
            elif stripped_line.startswith("blocked_from:"):
                blocked_from = parse_scalar(stripped_line.split(":", 1)[1]).lower()
            elif stripped_line.startswith("blocked_reason:"):
                blocked_reason = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("blocked_by:"):
                blocked_by = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("blocked_at:"):
                blocked_at = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line.startswith("updated_at:"):
                updated_at = parse_scalar(stripped_line.split(":", 1)[1])
            elif stripped_line == "allowed_paths:":
                active_block = "allowed_paths"
            elif stripped_line == "depends_on:":
                active_block = "depends_on"
            elif stripped_line == "doc_targets:":
                active_block = "doc_targets"
            elif stripped_line == "approval_target:":
                active_block = "approval_target"
            elif stripped_line.startswith("file_leases:"):
                has_file_leases = True
                active_block = "file_leases"
            continue

        if active_block == "allowed_paths" and indent_size >= 2 and stripped_line.startswith("- "):
            allowed_paths.append(normalize_path(parse_scalar(stripped_line[2:])))
        elif active_block == "depends_on" and indent_size >= 2 and stripped_line.startswith("- "):
            depends_on.append(parse_scalar(stripped_line[2:]))
        elif active_block == "approval_target" and indent_size >= 2 and ":" in stripped_line:
            child_key, child_value = stripped_line.split(":", 1)
            parsed_value = parse_scalar(child_value)
            if parsed_value:
                approval_target[child_key.strip()] = parsed_value
        elif active_block == "doc_targets":
            if indent_size >= 2 and stripped_line.startswith("- "):
                if current_doc_target:
                    path_text = normalize_path(current_doc_target.get("path", ""))
                    anchor_text = current_doc_target.get("section_anchor", "").strip()
                    if path_text and anchor_text:
                        doc_targets.append((path_text, anchor_text))
                current_doc_target = {}
                remainder_text = stripped_line[2:].strip()
                if ":" in remainder_text:
                    child_key, child_value = remainder_text.split(":", 1)
                    current_doc_target[child_key.strip()] = parse_scalar(child_value)
            elif current_doc_target is not None and indent_size >= 4 and ":" in stripped_line:
                child_key, child_value = stripped_line.split(":", 1)
                current_doc_target[child_key.strip()] = parse_scalar(child_value)

    if active_block == "doc_targets" and current_doc_target:
        path_text = normalize_path(current_doc_target.get("path", ""))
        anchor_text = current_doc_target.get("section_anchor", "").strip()
        if path_text and anchor_text:
            doc_targets.append((path_text, anchor_text))

    if not task_id:
        task_id = task_dir.name.split("-", 1)[0]
    if not title:
        title = task_dir.name
    if not owner_agent:
        owner_agent = "unassigned"
    if not mode:
        mode = "patch"
    if not status:
        status = "todo"

    return TaskMeta(
        task_id=task_id,
        title=title,
        owner_agent=owner_agent,
        mode=mode,
        status=status,
        allowed_paths=[path for path in allowed_paths if path],
        depends_on=[task for task in depends_on if task],
        doc_targets=[entry for entry in doc_targets if entry[0] and entry[1]],
        branch_or_workspace=branch_or_workspace,
        lane_key=lane_key,
        section_anchor=section_anchor,
        approval_target=approval_target,
        review_state=review_state,
        merge_state=merge_state,
        blocked_from=blocked_from,
        blocked_reason=blocked_reason,
        blocked_by=blocked_by,
        blocked_at=blocked_at,
        updated_at=updated_at,
        has_file_leases=has_file_leases,
        task_dir=task_dir,
    )


def list_task_meta(project_dir: Path) -> list[TaskMeta]:
    """列出全部任务。"""
    tasks_dir = project_dir / "docs" / "plan" / "tasks"
    if not tasks_dir.exists():
        return []

    task_items: list[TaskMeta] = []
    for meta_path in sorted(tasks_dir.glob("*/.meta.yaml")):
        task_items.append(parse_meta(meta_path))
    return sorted(task_items, key=lambda item: item.task_id)


def resolve_task(project_dir: Path, task_ref: str) -> TaskMeta:
    """按 task_id 或目录名定位任务。"""
    for task_meta in list_task_meta(project_dir):
        task_dir_name = task_meta.task_dir.name if task_meta.task_dir else ""
        if task_meta.task_id == task_ref or task_dir_name == task_ref:
            return task_meta
    raise ValueError(f"未找到任务: {task_ref}")


def derive_review_state(task_meta: TaskMeta) -> str:
    """推导 review 状态。"""
    if task_meta.review_state:
        return task_meta.review_state
    if task_meta.status == "in_review":
        return "in_review"
    if task_meta.status in {"approved", "queued", "merged"}:
        return "approved"
    return "pending"


def derive_merge_state(task_meta: TaskMeta) -> str:
    """推导 merge 状态。"""
    if task_meta.merge_state:
        return task_meta.merge_state
    if task_meta.status == "approved":
        return "ready"
    if task_meta.status == "queued":
        return "queued"
    if task_meta.status == "merged":
        return "merged"
    return "blocked"


def has_overlap(left_paths: list[str], right_paths: list[str]) -> bool:
    """判断路径前缀是否重叠。"""
    for left_path in left_paths:
        for right_path in right_paths:
            if not left_path or not right_path:
                continue
            if left_path == right_path:
                return True
            if left_path.startswith(f"{right_path}/") or right_path.startswith(f"{left_path}/"):
                return True
    return False


def validate_advanced_fields(task_meta: TaskMeta) -> None:
    """校验 advanced 任务字段完整性。"""
    missing_fields: list[str] = []
    if not task_meta.lane_key:
        missing_fields.append("lane_key")
    if not task_meta.has_file_leases:
        missing_fields.append("file_leases")
    required_targets = {"gate", "review", "merge"}
    missing_targets = sorted(required_targets - {key for key, value in task_meta.approval_target.items() if value})
    if missing_targets:
        missing_fields.append(f"approval_target({', '.join(missing_targets)})")
    if missing_fields:
        raise ValueError(f"advanced 任务缺少字段: {', '.join(missing_fields)}")


def list_missing_advanced_fields(task_meta: TaskMeta) -> list[str]:
    """列出 advanced 模式缺失字段。"""
    missing_fields: list[str] = []
    if not task_meta.lane_key:
        missing_fields.append("lane_key")
    if not task_meta.has_file_leases:
        missing_fields.append("file_leases")
    required_targets = {"gate", "review", "merge"}
    missing_targets = sorted(required_targets - {key for key, value in task_meta.approval_target.items() if value})
    if missing_targets:
        missing_fields.append(f"approval_target({', '.join(missing_targets)})")
    return missing_fields


def validate_start(task_meta: TaskMeta, all_tasks: list[TaskMeta]) -> None:
    """校验任务能否进入 doing。"""
    if not task_meta.allowed_paths:
        raise ValueError("缺少 allowed_paths，不能开始执行")
    if task_meta.is_advanced:
        validate_advanced_fields(task_meta)

    for other_task in all_tasks:
        if other_task.task_id == task_meta.task_id or other_task.status not in ACTIVE_STATUSES:
            continue
        if not has_overlap(task_meta.allowed_paths, other_task.allowed_paths):
            continue
        if not task_meta.is_advanced or not other_task.is_advanced:
            raise ValueError(
                f"allowed_paths 与活跃任务 {other_task.task_id} 重叠，请升级 advanced 或调整任务边界"
            )
        if task_meta.lane_key and task_meta.lane_key == other_task.lane_key:
            raise ValueError(
                f"lane_key 与活跃任务 {other_task.task_id} 冲突：{task_meta.lane_key}"
            )


def suggest_lane_key(task_meta: TaskMeta, all_tasks: list[TaskMeta]) -> str:
    """为 advanced 模式生成建议 lane_key。"""
    if task_meta.lane_key:
        return task_meta.lane_key

    top_segments: list[str] = []
    for path_text in task_meta.allowed_paths:
        parts = [part for part in path_text.split("/") if part]
        if parts:
            top_segments.append(parts[0].lower())

    if top_segments and all(segment == top_segments[0] for segment in top_segments):
        base_text = re.sub(r"[^a-z0-9]+", "-", top_segments[0]).strip("-")
    else:
        base_text = task_meta.task_id.lower()
    if not base_text:
        base_text = task_meta.task_id.lower() or "task"

    candidate_text = f"lane:{base_text}"
    existing_lanes = {task.lane_key for task in all_tasks if task.task_id != task_meta.task_id and task.lane_key}
    if candidate_text not in existing_lanes:
        return candidate_text

    suffix_index = 1
    while True:
        fallback_text = f"{candidate_text}-{task_meta.task_id.lower()}"
        if suffix_index > 1:
            fallback_text = f"{fallback_text}-{suffix_index}"
        if fallback_text not in existing_lanes:
            return fallback_text
        suffix_index += 1


def build_preflight_report(task_meta: TaskMeta, all_tasks: list[TaskMeta], config_data: dict[str, object]) -> PreflightReport:
    """构建 start 前的预检报告。"""
    active_tasks = [
        other_task
        for other_task in all_tasks
        if other_task.task_id != task_meta.task_id and other_task.status in ACTIVE_STATUSES
    ]
    parallel_limit = get_parallel_active_task_limit(config_data)
    overlapping_tasks = [
        other_task
        for other_task in active_tasks
        if has_overlap(task_meta.allowed_paths, other_task.allowed_paths)
    ]

    current_mode = "advanced" if task_meta.is_advanced else "normal"
    recommended_mode = (
        "advanced"
        if (task_meta.is_advanced or overlapping_tasks or (len(active_tasks) + 1) >= parallel_limit)
        else "normal"
    )
    suggested_lane = suggest_lane_key(task_meta, all_tasks) if recommended_mode == "advanced" else "-"

    reasons: list[str] = []
    actions: list[str] = []

    if task_meta.status not in {"todo", "blocked"}:
        reasons.append(f"current_status_not_startable: {task_meta.status}")
        actions.append("use_next_transition_instead_of_start")

    if not task_meta.allowed_paths:
        reasons.append("missing_allowed_paths")
        actions.append("add_allowed_paths")

    if (len(active_tasks) + 1) >= parallel_limit and not task_meta.is_advanced:
        reasons.append(f"parallel_active_tasks: {len(active_tasks) + 1}")
        if "upgrade_to_advanced" not in actions:
            actions.append("upgrade_to_advanced")

    if overlapping_tasks:
        if "upgrade_to_advanced" not in actions:
            if not task_meta.is_advanced:
                actions.append("upgrade_to_advanced")
        if any(not other_task.is_advanced for other_task in overlapping_tasks):
            actions.append("wait_for_overlap_to_finish_or_upgrade_peer_tasks")

    if recommended_mode == "advanced":
        missing_fields = list_missing_advanced_fields(task_meta)
        if missing_fields:
            reasons.append(f"advanced_fields_missing: {', '.join(missing_fields)}")
        if not task_meta.lane_key:
            actions.append(f"set_lane_key: {suggested_lane}")
        if not task_meta.has_file_leases:
            actions.append("declare_file_leases")
        missing_targets = sorted({"gate", "review", "merge"} - set(task_meta.approval_target))
        if missing_targets:
            actions.append(f"declare_approval_target: {', '.join(missing_targets)}")

    try:
        validate_start(task_meta, all_tasks)
        start_error = ""
    except ValueError as exc:
        start_error = str(exc)
        reasons.append(f"start_gate: {start_error}")

    if task_meta.is_advanced and task_meta.lane_key:
        conflicting_lane_tasks = [
            other_task.task_id
            for other_task in active_tasks
            if other_task.is_advanced and other_task.lane_key == task_meta.lane_key
        ]
        if conflicting_lane_tasks:
            joined_ids = ", ".join(conflicting_lane_tasks)
            reasons.append(f"lane_conflict_with: {joined_ids}")
            actions.append(f"change_lane_key_from: {task_meta.lane_key}")

    deduped_reasons: list[str] = []
    for reason_text in reasons:
        if reason_text and reason_text not in deduped_reasons:
            deduped_reasons.append(reason_text)

    deduped_actions: list[str] = []
    for action_text in actions:
        if action_text and action_text not in deduped_actions:
            deduped_actions.append(action_text)

    ready_to_start = not deduped_reasons and task_meta.status in {"todo", "blocked"} and not start_error
    return PreflightReport(
        task_id=task_meta.task_id,
        title=task_meta.title,
        status=task_meta.status,
        current_collaboration_mode=current_mode,
        recommended_collaboration_mode=recommended_mode,
        ready_to_start=ready_to_start,
        active_task_count=len(active_tasks),
        suggested_lane_key=suggested_lane,
        path_overlap_with=[other_task.task_id for other_task in overlapping_tasks],
        reasons=deduped_reasons,
        actions=deduped_actions,
    )


def render_preflight_report(report: PreflightReport) -> str:
    """渲染预检报告文本。"""
    lines = [
        "# taskctl preflight",
        f"task_id: {report.task_id}",
        f"title: {report.title}",
        f"status: {report.status}",
        f"current_collaboration_mode: {report.current_collaboration_mode}",
        f"recommended_collaboration_mode: {report.recommended_collaboration_mode}",
        f"ready_to_start: {'yes' if report.ready_to_start else 'no'}",
        f"active_task_count: {report.active_task_count}",
        f"path_overlap_with: {', '.join(report.path_overlap_with) if report.path_overlap_with else '-'}",
        f"suggested_lane_key: {report.suggested_lane_key}",
        "reasons:",
    ]
    if report.reasons:
        lines.extend(f"- {reason_text}" for reason_text in report.reasons)
    else:
        lines.append("- none")
    lines.append("actions:")
    if report.actions:
        lines.extend(f"- {action_text}" for action_text in report.actions)
    else:
        lines.append("- none")
    return "\n".join(lines)


def build_route_report(
    project_dir: Path,
    allowed_paths: list[str],
    doc_target_texts: list[str],
    requires_worktree: bool,
    requires_stack: bool,
) -> RouteReport:
    """为任务草案生成模式路由建议。"""
    if requires_worktree and requires_stack:
        raise ValueError("route 不能同时指定 --requires-worktree 和 --requires-stack")

    normalized_paths = [normalize_path(path_text) for path_text in allowed_paths if normalize_path(path_text)]
    if not normalized_paths:
        raise ValueError("route 至少需要一个 --path")
    normalized_doc_targets = [split_anchor_ref(value_text, "--doc-target") for value_text in doc_target_texts]

    draft_task = TaskMeta(
        task_id="DRAFT",
        title="draft",
        owner_agent="coordinator",
        mode="patch",
        status="todo",
        allowed_paths=normalized_paths,
        doc_targets=normalized_doc_targets,
    )
    all_tasks = list_task_meta(project_dir)
    config_data = load_taskctl_config(project_dir)
    preflight_report = build_preflight_report(draft_task, all_tasks, config_data)

    if requires_worktree:
        execution_mode = "worktree"
    elif requires_stack:
        execution_mode = "stack"
    else:
        execution_mode = "patch"

    reasons = list(preflight_report.reasons)
    actions = list(preflight_report.actions)
    if requires_worktree:
        reasons.append("execution_mode_reason: explicit_worktree_request")
    elif requires_stack:
        reasons.append("execution_mode_reason: explicit_stack_request")
    else:
        reasons.append("execution_mode_reason: default_patch")

    deduped_reasons: list[str] = []
    for reason_text in reasons:
        if reason_text and reason_text not in deduped_reasons:
            deduped_reasons.append(reason_text)

    deduped_actions: list[str] = []
    for action_text in actions:
        if action_text and action_text not in deduped_actions:
            deduped_actions.append(action_text)

    return RouteReport(
        recommended_collaboration_mode=preflight_report.recommended_collaboration_mode,
        recommended_execution_mode=execution_mode,
        recommended_create_flag="--auto-advanced"
        if preflight_report.recommended_collaboration_mode == "advanced"
        else "-",
        active_task_count=preflight_report.active_task_count,
        path_overlap_with=preflight_report.path_overlap_with,
        reasons=deduped_reasons,
        actions=deduped_actions,
    )


def render_route_report(report: RouteReport) -> str:
    """渲染路由建议。"""
    lines = [
        "# taskctl route",
        f"recommended_collaboration_mode: {report.recommended_collaboration_mode}",
        f"recommended_execution_mode: {report.recommended_execution_mode}",
        f"recommended_create_flag: {report.recommended_create_flag}",
        f"active_task_count: {report.active_task_count}",
        f"path_overlap_with: {', '.join(report.path_overlap_with) if report.path_overlap_with else '-'}",
        "reasons:",
    ]
    if report.reasons:
        lines.extend(f"- {reason_text}" for reason_text in report.reasons)
    else:
        lines.append("- none")
    lines.append("actions:")
    if report.actions:
        lines.extend(f"- {action_text}" for action_text in report.actions)
    else:
        lines.append("- none")
    return "\n".join(lines)


def derive_file_leases(task_meta: TaskMeta, file_lease_texts: list[str]) -> list[tuple[str, str]]:
    """推导 file_leases。"""
    if file_lease_texts:
        return [split_anchor_ref(value_text, "--file-lease") for value_text in file_lease_texts]
    if task_meta.doc_targets:
        return list(task_meta.doc_targets)
    if task_meta.section_anchor:
        file_candidates = [path_text for path_text in task_meta.allowed_paths if "." in Path(path_text).name]
        if file_candidates:
            return [(file_candidates[0], task_meta.section_anchor)]
    return []


def upgrade_task_to_advanced(
    project_dir: Path,
    task_ref: str,
    lane_key: str,
    approval_gate: str,
    approval_review: str,
    approval_merge: str,
    file_lease_texts: list[str],
) -> int:
    """将任务元数据补齐为 advanced 所需字段。"""
    task_meta = resolve_task(project_dir, task_ref)
    if task_meta.status == "merged":
        raise ValueError("merged 任务不能再升级 advanced")
    if task_meta.task_dir is None:
        raise ValueError("任务目录不存在")

    all_tasks = list_task_meta(project_dir)
    config_data = load_taskctl_config(project_dir)
    applied_lane_key = lane_key.strip() or suggest_lane_key(task_meta, all_tasks)
    default_approval_target = get_default_approval_target(config_data)
    approval_target = {
        "gate": approval_gate.strip() or default_approval_target["gate"],
        "review": approval_review.strip() or default_approval_target["review"],
        "merge": approval_merge.strip() or default_approval_target["merge"],
    }
    missing_targets = [key_text for key_text, value_text in approval_target.items() if not value_text]
    if missing_targets:
        raise ValueError(f"upgrade-advanced 缺少审批目标：{', '.join(missing_targets)}")

    derived_file_leases = derive_file_leases(task_meta, file_lease_texts)
    meta_path = task_meta.task_dir / ".meta.yaml"
    meta_text = meta_path.read_text(encoding="utf-8")
    meta_text = update_top_level_scalar(meta_text, "lane_key", quote_yaml(applied_lane_key))
    meta_text = update_top_level_block(
        meta_text,
        "approval_target",
        [
            "approval_target:",
            f"  gate: {quote_yaml(approval_target['gate'])}",
            f"  review: {quote_yaml(approval_target['review'])}",
            f"  merge: {quote_yaml(approval_target['merge'])}",
        ],
    )
    if derived_file_leases:
        file_lease_lines = ["file_leases:"]
        for path_text, anchor_text in derived_file_leases:
            file_lease_lines.extend(
                [
                    f"  - path: {quote_yaml(path_text)}",
                    f"    section_anchor: {quote_yaml(anchor_text)}",
                    f"    lease_owner: {quote_yaml(task_meta.task_id)}",
                    '    lease_state: "active"',
                ]
            )
    elif task_meta.has_file_leases:
        file_lease_lines = []
    else:
        file_lease_lines = ["file_leases: []"]
    if file_lease_lines:
        meta_text = update_top_level_block(meta_text, "file_leases", file_lease_lines)
    meta_text = update_top_level_scalar(meta_text, "updated_at", quote_yaml(now_iso()))
    meta_path.write_text(meta_text, encoding="utf-8")

    print(f"[OK] {task_meta.task_id} upgraded to advanced")
    print(f"lane_key: {applied_lane_key}")
    print(
        "approval_target: "
        f"gate={approval_target['gate']}, review={approval_target['review']}, merge={approval_target['merge']}"
    )
    print(f"file_leases: {len(derived_file_leases) if derived_file_leases else (1 if not task_meta.has_file_leases else 0)}")
    return 0


def validate_approve(task_meta: TaskMeta) -> None:
    """校验任务能否 approved。"""
    if task_meta.is_advanced:
        validate_advanced_fields(task_meta)


def validate_enqueue(task_meta: TaskMeta, task_map: dict[str, TaskMeta], queue_items: list[QueueItem]) -> None:
    """校验任务能否进入 merge queue。"""
    validate_approve(task_meta)
    if not task_meta.branch_or_workspace:
        raise ValueError("缺少 branch_or_workspace，无法入队 merge queue")
    for dependency_id in task_meta.depends_on:
        dependency_task = task_map.get(dependency_id)
        if dependency_task is None:
            raise ValueError(f"depends_on 引用了不存在的任务: {dependency_id}")
        if dependency_task.status != "merged":
            raise ValueError(f"依赖任务尚未 merged: {dependency_id}")
    if any(item.task_id == task_meta.task_id for item in queue_items):
        raise ValueError(f"任务已在 merge queue 中: {task_meta.task_id}")


def validate_merge(task_meta: TaskMeta, queue_items: list[QueueItem]) -> None:
    """校验任务能否 merged。"""
    if not queue_items:
        raise ValueError("merge queue 为空，无法执行 merged")
    head_item = queue_items[0]
    if head_item.task_id != task_meta.task_id:
        raise ValueError(f"任务不在队首：当前队首是 {head_item.task_id}")


def get_session_id() -> str:
    """返回当前会话 ID，无环境变量时用 deterministic fallback。"""
    session_id = os.getenv("CLAUDE_SESSION_ID", "").strip()
    if session_id:
        return session_id
    host_name = platform.node().strip() or "unknown-host"
    return f"fallback-{host_name}-{os.getpid()}"


def get_session_runtime_dir(project_dir: Path) -> Path:
    """返回当前会话 runtime 目录。"""
    return project_dir / ".claude" / "state" / "runtime" / "sessions" / get_session_id()


def get_session_focus_path(project_dir: Path) -> Path:
    """返回当前会话焦点文件路径。"""
    return get_session_runtime_dir(project_dir) / "focus.json"


def load_session_focus(project_dir: Path) -> dict[str, object]:
    """读取当前会话焦点。"""
    focus_path = get_session_focus_path(project_dir)
    if not focus_path.exists():
        return {}
    try:
        raw_data = json.loads(focus_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return raw_data if isinstance(raw_data, dict) else {}


def update_manifest_focus(
    project_dir: Path,
    task_meta: TaskMeta | None,
    phase: str = "",
) -> None:
    """更新当前会话焦点（只写 session focus.json，不写 MANIFEST）。"""
    focus_path = get_session_focus_path(project_dir)
    focus_path.parent.mkdir(parents=True, exist_ok=True)
    if task_meta is None:
        focus_data: dict[str, object] = {
            "task_id": "",
            "task_name": "",
            "phase": "",
            "context": "",
            "plan_subdir": "",
            "started": None,
        }
    else:
        plan_subdir = (
            task_meta.task_dir.relative_to(project_dir).as_posix()
            if task_meta.task_dir is not None
            else ""
        )
        focus_data = {
            "task_id": task_meta.task_id,
            "task_name": task_meta.title,
            "phase": phase or task_meta.status,
            "context": "",
            "plan_subdir": plan_subdir,
            "started": now_iso(),
        }
    focus_path.write_text(
        json.dumps(focus_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def get_manifest_focus_task_id(project_dir: Path) -> str:
    """读取当前会话焦点任务（只读 session focus.json）。"""
    task_id = load_session_focus(project_dir).get("task_id")
    return str(task_id).strip() if isinstance(task_id, str) else ""


def update_task_meta_fields(task_meta: TaskMeta, fields: dict[str, str]) -> None:
    """批量写回任务顶层字段。"""
    if task_meta.task_dir is None:
        raise ValueError("任务目录不存在")
    meta_path = task_meta.task_dir / ".meta.yaml"
    meta_text = meta_path.read_text(encoding="utf-8")
    for key_text, value_text in fields.items():
        meta_text = update_top_level_scalar(meta_text, key_text, value_text)
    meta_path.write_text(meta_text, encoding="utf-8")


def update_task_meta(task_meta: TaskMeta, new_status: str, review_state: str, merge_state: str) -> None:
    """写回任务状态字段。"""
    update_task_meta_fields(
        task_meta,
        {
            "status": quote_yaml(new_status),
            "review_state": quote_yaml(review_state),
            "merge_state": quote_yaml(merge_state),
            "updated_at": quote_yaml(now_iso()),
        },
    )


def build_status_summary(all_tasks: list[TaskMeta]) -> str:
    """生成状态总览表。"""
    counts = {status: 0 for status in STATUS_ORDER}
    for task_meta in all_tasks:
        counts[task_meta.status] = counts.get(task_meta.status, 0) + 1
    lines = ["| 状态 | 数量 |", "|------|------|"]
    for status in STATUS_ORDER:
        lines.append(f"| `{status}` | {counts.get(status, 0)} |")
    return "\n".join(lines)


def build_task_table(all_tasks: list[TaskMeta], project_dir: Path) -> str:
    """生成任务总表。"""
    lines = [
        "| ID | Task | Owner | Mode | Lane | Allowed Paths | Branch / Workspace | Review | Merge | Status | Task Dir | 更新时间 |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    if not all_tasks:
        lines.append("| — | _暂无任务_ | — | — | — | — | — | — | — | — | — | — |")
        return "\n".join(lines)

    for task_meta in all_tasks:
        task_dir_text = task_meta.task_dir.relative_to(project_dir).as_posix() if task_meta.task_dir else "—"
        lines.append(
            "| {task_id} | {title} | {owner} | {mode} | {lane} | {paths} | {branch} | {review} | {merge} | {status} | {task_dir} | {updated} |".format(
                task_id=task_meta.task_id,
                title=task_meta.title.replace("|", "\\|"),
                owner=task_meta.owner_agent.replace("|", "\\|"),
                mode=task_meta.mode or "patch",
                lane=task_meta.lane_key or "—",
                paths=format_allowed_paths(task_meta.allowed_paths),
                branch=task_meta.branch_or_workspace or "—",
                review=derive_review_state(task_meta),
                merge=derive_merge_state(task_meta),
                status=task_meta.status,
                task_dir=task_dir_text,
                updated=task_meta.updated_at or "—",
            )
        )
    return "\n".join(lines)


def build_queue_table(queue_items: list[QueueItem], task_map: dict[str, TaskMeta]) -> str:
    """生成 merge queue 表。"""
    lines = [
        "| 顺位 | Task | Branch / Workspace | 状态 | 入队时间 |",
        "|------|------|--------------------|------|----------|",
    ]
    if not queue_items:
        lines.append("| — | _队列为空_ | — | — | — |")
        return "\n".join(lines)
    for index_value, item in enumerate(queue_items, start=1):
        task_meta = task_map.get(item.task_id)
        lines.append(
            f"| {index_value} | {item.task_id} | {item.merge_ref or '—'} | {task_meta.status if task_meta else 'missing'} | {item.queued_at or '—'} |"
        )
    return "\n".join(lines)


def sync_plan(project_dir: Path) -> None:
    """刷新 PLAN.md 的状态总览、任务表和 merge queue。"""
    plan_path = project_dir / "docs" / "plan" / "PLAN.md"
    queue_path = project_dir / "docs" / "plan" / "MERGE_QUEUE.yaml"
    all_tasks = list_task_meta(project_dir)
    task_map = {task.task_id: task for task in all_tasks}
    queue_items = load_queue(queue_path)
    plan_text = plan_path.read_text(encoding="utf-8")
    plan_text = replace_between_markers(plan_text, PLAN_STATUS_BEGIN, PLAN_STATUS_END, build_status_summary(all_tasks))
    plan_text = replace_between_markers(plan_text, PLAN_TABLE_BEGIN, PLAN_TABLE_END, build_task_table(all_tasks, project_dir))
    plan_text = replace_between_markers(plan_text, PLAN_QUEUE_BEGIN, PLAN_QUEUE_END, build_queue_table(queue_items, task_map))
    plan_path.write_text(plan_text, encoding="utf-8")


def render_task_file(task_id: str, title: str, heading_text: str) -> str:
    """渲染任务文档骨架。"""
    return "\n".join(
        [
            f"# {heading_text}",
            "",
            f"- 任务编号：{task_id}",
            f"- 标题：{title}",
            "",
            "## 内容",
            "",
            "- 待补充",
            "",
        ]
    )


def render_review_bundle_task_file(
    task_id: str,
    title: str,
    review_kind: str,
    track_definition: dict[str, object],
    source_paths: list[str],
) -> str:
    """渲染 reviewer task.md。"""
    track_title = str(track_definition["title"])
    summary_text = str(track_definition["summary"])
    question_items = [str(item) for item in track_definition["questions"]]
    lines = [
        "# 任务说明",
        "",
        f"- 任务编号：{task_id}",
        f"- 标题：{title}",
        f"- 评审类型：{review_kind}",
        f"- 评审视角：{track_title}",
        "",
        f"> {summary_text}",
        "",
        "## 只读输入",
        "",
    ]
    lines.extend(f"- `{path_text}`" for path_text in source_paths)
    lines.extend(
        [
            "",
            "## 本任务要回答",
            "",
        ]
    )
    lines.extend(f"- {question_text}" for question_text in question_items)
    lines.extend(
        [
            "",
            "## 输出要求",
            "",
            "- 仅更新当前任务目录下的 `review.md`、`handoff.md` 等交付文档",
            "- 不直接修改业务源码、算法实现或主说明文档",
            "- 所有结论都要标注证据来源和严重程度",
            "",
        ]
    )
    return "\n".join(lines)


def render_review_bundle_steps_file(track_definition: dict[str, object], source_paths: list[str]) -> str:
    """渲染 reviewer steps.md。"""
    lines = [
        "# 执行步骤",
        "",
        "- [ ] 阅读输入材料，确认范围与上下文",
        "- [ ] 按评审视角完成逐项检查",
        "- [ ] 将问题按 blocker / major / minor / question 分级",
        "- [ ] 在 `review.md` 中写出证据、结论与建议动作",
        "",
        "## 输入范围",
        "",
    ]
    lines.extend(f"- `{path_text}`" for path_text in source_paths)
    return "\n".join(lines)


def render_review_bundle_acceptance_file(track_definition: dict[str, object]) -> str:
    """渲染 reviewer acceptance.md。"""
    checklist_items = [str(item) for item in track_definition["checklist"]]
    lines = [
        "# 验收标准",
        "",
        "- [ ] 明确当前评审视角与目标",
        "- [ ] 已给出问题分级",
        "- [ ] 每条结论都附有证据或引用来源",
        "- [ ] 已区分已验证事实与推断",
        "",
        "## 专项检查清单",
        "",
    ]
    lines.extend(f"- [ ] {item_text}" for item_text in checklist_items)
    return "\n".join(lines)


def render_review_bundle_handoff_file(track_definition: dict[str, object]) -> str:
    """渲染 reviewer handoff.md。"""
    track_title = str(track_definition["title"])
    return "\n".join(
        [
            "# 交接记录",
            "",
            f"- 评审视角：{track_title}",
            "- 当前进展：待开始",
            "- 下一步：完成独立评审并更新 `review.md`",
            "- 注意事项：不要直接修改源码，只提交结论和证据",
            "",
        ]
    )


def render_review_bundle_report_file(
    review_kind: str,
    track_definition: dict[str, object],
    source_paths: list[str],
) -> str:
    """渲染 reviewer review.md。"""
    track_title = str(track_definition["title"])
    question_items = [str(item) for item in track_definition["questions"]]
    checklist_items = [str(item) for item in track_definition["checklist"]]
    lines = [
        "# 审查记录",
        "",
        f"- 评审类型：{review_kind}",
        f"- 评审视角：{track_title}",
        "",
        "## 输入材料",
        "",
    ]
    lines.extend(f"- `{path_text}`" for path_text in source_paths)
    lines.extend(
        [
            "",
            "## 检查问题",
            "",
        ]
    )
    lines.extend(f"- {question_text}" for question_text in question_items)
    lines.extend(
        [
            "",
            "## 检查清单",
            "",
        ]
    )
    lines.extend(f"- [ ] {item_text}" for item_text in checklist_items)
    lines.extend(
        [
            "",
            "## 发现",
            "",
            "### blocker",
            "",
            "- 待填写",
            "",
            "### major",
            "",
            "- 待填写",
            "",
            "### minor",
            "",
            "- 待填写",
            "",
            "### question",
            "",
            "- 待填写",
            "",
            "## 结论",
            "",
            "- 结论：approved / changes_requested / blocked",
            "- 证据：待填写",
            "- 建议动作：待填写",
            "",
        ]
    )
    return "\n".join(lines)


def normalize_review_item_text(text: str) -> str:
    """标准化 reviewer 发现文本，便于聚合。"""
    normalized_text = re.sub(r"\s+", " ", text.strip())
    normalized_text = normalized_text.strip("-*`'\".。,，;；:：!?！？[]()（）")
    return normalized_text.lower()


def is_placeholder_review_text(text: str) -> bool:
    """判断 reviewer 文本是否仍为占位内容。"""
    normalized_text = normalize_review_item_text(text)
    return normalized_text in {
        "",
        "待填写",
        "approved / changes_requested / blocked",
    }


def parse_review_conclusion(value_text: str) -> str:
    """解析 reviewer 结论。"""
    normalized_text = value_text.strip().lower()
    for decision_text in ("blocked", "changes_requested", "approved"):
        if decision_text in normalized_text:
            return decision_text
    return ""


def severity_sort_key(severity_text: str) -> int:
    """返回严重程度排序值。"""
    return SEVERITY_ORDER.get(severity_text, 99)


def pick_higher_severity(left_text: str, right_text: str) -> str:
    """返回更高严重程度。"""
    if severity_sort_key(left_text) <= severity_sort_key(right_text):
        return left_text
    return right_text


def infer_track_title(task_meta: TaskMeta, fallback_title: str = "") -> str:
    """推断 reviewer 视角标题。"""
    if fallback_title:
        return fallback_title
    if " - " in task_meta.title:
        return task_meta.title.rsplit(" - ", 1)[1].strip()
    return task_meta.title


def parse_reviewer_summary(task_meta: TaskMeta) -> ReviewerSummary:
    """解析 reviewer 的 review.md。"""
    if task_meta.task_dir is None:
        raise ValueError(f"任务缺少 task_dir：{task_meta.task_id}")
    review_path = task_meta.task_dir / "review.md"
    if not review_path.exists():
        raise ValueError(f"{task_meta.task_id} 缺少 review.md")

    track_title = ""
    conclusion = ""
    evidence = ""
    suggested_action = ""
    current_severity = ""
    in_findings = False
    findings: list[ReviewFinding] = []

    for raw_line in review_path.read_text(encoding="utf-8").splitlines():
        stripped_line = raw_line.strip()
        if stripped_line.startswith("- 评审视角："):
            track_title = stripped_line.split("：", 1)[1].strip()
            continue
        if stripped_line == "## 发现":
            in_findings = True
            current_severity = ""
            continue
        if stripped_line.startswith("## ") and stripped_line != "## 发现":
            in_findings = False
            current_severity = ""

        if in_findings and stripped_line.startswith("### "):
            current_severity = stripped_line[4:].strip().lower()
            continue

        if in_findings and current_severity and stripped_line.startswith("- "):
            finding_text = stripped_line[2:].strip()
            if is_placeholder_review_text(finding_text):
                continue
            findings.append(
                ReviewFinding(
                    severity=current_severity,
                    text=finding_text,
                    normalized_text=normalize_review_item_text(finding_text),
                    reviewer_task_id=task_meta.task_id,
                    reviewer_title=task_meta.title,
                    track_title=track_title or infer_track_title(task_meta),
                )
            )
            continue

        if stripped_line.startswith("- 结论："):
            conclusion = parse_review_conclusion(stripped_line.split("：", 1)[1])
        elif stripped_line.startswith("- 证据："):
            evidence_text = stripped_line.split("：", 1)[1].strip()
            if not is_placeholder_review_text(evidence_text):
                evidence = evidence_text
        elif stripped_line.startswith("- 建议动作："):
            action_text = stripped_line.split("：", 1)[1].strip()
            if not is_placeholder_review_text(action_text):
                suggested_action = action_text

    return ReviewerSummary(
        task_id=task_meta.task_id,
        title=task_meta.title,
        track_title=infer_track_title(task_meta, track_title),
        conclusion=conclusion,
        evidence=evidence,
        suggested_action=suggested_action,
        findings=findings,
    )


def build_aggregated_issue(grouped_findings: list[ReviewFinding]) -> AggregatedIssue:
    """把同一问题组装为汇总项。"""
    highest_severity = grouped_findings[0].severity
    preferred_text = grouped_findings[0].text
    source_pairs: list[tuple[str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()

    for finding in grouped_findings:
        highest_severity = pick_higher_severity(highest_severity, finding.severity)
        if severity_sort_key(finding.severity) < severity_sort_key(grouped_findings[0].severity):
            preferred_text = finding.text
        source_pair = (finding.reviewer_task_id, finding.track_title)
        if source_pair not in seen_pairs:
            seen_pairs.add(source_pair)
            source_pairs.append(source_pair)

    return AggregatedIssue(
        text=preferred_text,
        severity=highest_severity,
        sources=source_pairs,
    )


def decide_final_review_conclusion(reviewers: list[ReviewerSummary], issues: list[AggregatedIssue]) -> str:
    """基于 reviewer 结论和问题严重程度决定最终结论。"""
    conclusions = [reviewer.conclusion for reviewer in reviewers]
    if any(not conclusion for conclusion in conclusions):
        return "blocked"
    if any(conclusion == "blocked" for conclusion in conclusions):
        return "blocked"
    if any(conclusion == "changes_requested" for conclusion in conclusions):
        return "changes_requested"
    if any(issue.severity == "blocker" for issue in issues):
        return "changes_requested"
    if any(issue.severity == "major" for issue in issues):
        return "changes_requested"
    return "approved"


def derive_aggregate_title(
    explicit_title: str,
    target_task_meta: TaskMeta | None,
    reviewers: list[ReviewerSummary],
) -> str:
    """推导汇总标题。"""
    if explicit_title.strip():
        return explicit_title.strip()
    if target_task_meta is not None:
        return target_task_meta.title

    base_titles: list[str] = []
    for reviewer in reviewers:
        if " - " in reviewer.title:
            base_titles.append(reviewer.title.rsplit(" - ", 1)[0].strip())
        else:
            base_titles.append(reviewer.title.strip())
    if base_titles and all(title == base_titles[0] for title in base_titles):
        base_title = base_titles[0]
        if base_title.endswith("汇总") or base_title.endswith("总评审"):
            return base_title
        return f"{base_title}汇总"
    return "多专家评审汇总"


def build_divergence_notes(reviewers: list[ReviewerSummary]) -> list[str]:
    """生成分歧说明。"""
    divergence_notes: list[str] = []
    conclusion_counter = Counter(
        reviewer.conclusion or "missing"
        for reviewer in reviewers
    )
    if len(conclusion_counter) > 1:
        summary_text = "，".join(
            f"{decision_text}={count_value}"
            for decision_text, count_value in sorted(conclusion_counter.items())
        )
        divergence_notes.append(f"评审结论存在分歧：{summary_text}")
    elif "missing" in conclusion_counter:
        divergence_notes.append("至少有一个 reviewer 未填写有效结论")
    return divergence_notes


def build_review_aggregate_result(
    reviewers: list[ReviewerSummary],
    explicit_title: str,
    target_task_meta: TaskMeta | None,
) -> ReviewAggregateResult:
    """生成 review 汇总结果。"""
    grouped_findings: dict[str, list[ReviewFinding]] = {}
    for reviewer in reviewers:
        for finding in reviewer.findings:
            grouped_findings.setdefault(finding.normalized_text, []).append(finding)

    consensus_issues: list[AggregatedIssue] = []
    single_high_value_issues: list[AggregatedIssue] = []
    all_issues: list[AggregatedIssue] = []

    for finding_group in grouped_findings.values():
        task_ids = {finding.reviewer_task_id for finding in finding_group}
        aggregated_issue = build_aggregated_issue(finding_group)
        all_issues.append(aggregated_issue)
        if len(task_ids) >= 2:
            consensus_issues.append(aggregated_issue)
            continue
        if aggregated_issue.severity in {"blocker", "major"}:
            single_high_value_issues.append(aggregated_issue)

    consensus_issues.sort(key=lambda issue: (severity_sort_key(issue.severity), issue.text))
    single_high_value_issues.sort(key=lambda issue: (severity_sort_key(issue.severity), issue.text))

    return ReviewAggregateResult(
        title=derive_aggregate_title(explicit_title, target_task_meta, reviewers),
        final_decision=decide_final_review_conclusion(reviewers, all_issues),
        reviewers=reviewers,
        consensus_issues=consensus_issues,
        single_high_value_issues=single_high_value_issues,
        divergence_notes=build_divergence_notes(reviewers),
    )


def render_aggregate_issue_lines(issues: list[AggregatedIssue]) -> list[str]:
    """渲染问题列表。"""
    if not issues:
        return ["- 无"]

    lines: list[str] = []
    for issue in issues:
        source_text = "；".join(f"{task_id} {track_title}" for task_id, track_title in issue.sources)
        lines.extend(
            [
                f"- [{issue.severity}] {issue.text}",
                f"  来源：{source_text}",
            ]
        )
    return lines


def render_review_aggregate_report(result: ReviewAggregateResult) -> str:
    """渲染多 reviewer 汇总报告。"""
    lines = [
        f"# {result.title}",
        "",
        f"- 生成时间：{now_iso()}",
        f"- 汇总 reviewer 数：{len(result.reviewers)}",
        f"- 最终结论：{result.final_decision}",
        "",
        "## Reviewer 概览",
        "",
        "| Task | 视角 | 结论 | 证据 | 建议动作 |",
        "|---|---|---|---|---|",
    ]
    for reviewer in result.reviewers:
        lines.append(
            f"| {reviewer.task_id} | {reviewer.track_title} | {reviewer.conclusion or 'missing'} | "
            f"{reviewer.evidence or '—'} | {reviewer.suggested_action or '—'} |"
        )

    lines.extend(
        [
            "",
            "## 共识问题",
            "",
            *render_aggregate_issue_lines(result.consensus_issues),
            "",
            "## 单路高价值问题",
            "",
            *render_aggregate_issue_lines(result.single_high_value_issues),
            "",
            "## 分歧问题",
            "",
        ]
    )
    if result.divergence_notes:
        lines.extend(f"- {note_text}" for note_text in result.divergence_notes)
    else:
        lines.append("- 无")

    suggested_next_action = {
        "blocked": "先补齐缺失结论或阻塞性问题，再重新汇总。",
        "changes_requested": "优先处理共识问题，再回看单路高价值问题。",
        "approved": "可进入后续收尾或 merge queue。",
    }[result.final_decision]
    lines.extend(
        [
            "",
            "## 最终结论",
            "",
            f"- 结论：{result.final_decision}",
            f"- 建议动作：{suggested_next_action}",
            "",
        ]
    )
    return "\n".join(lines)


def resolve_review_aggregate_output(
    project_dir: Path,
    output_text: str,
    target_task_text: str,
) -> tuple[Path, TaskMeta | None]:
    """解析 review 汇总输出位置。"""
    has_output = bool(output_text.strip())
    has_target_task = bool(target_task_text.strip())
    if has_output == has_target_task:
        raise ValueError("review-aggregate 必须二选一：--output 或 --target-task")

    if has_target_task:
        target_task_meta = resolve_task(project_dir, target_task_text)
        if target_task_meta.task_dir is None:
            raise ValueError(f"目标任务缺少 task_dir：{target_task_meta.task_id}")
        return target_task_meta.task_dir / "review.md", target_task_meta

    normalized_output = normalize_path(output_text)
    if not normalized_output:
        raise ValueError("--output 不能为空")
    output_path = (project_dir / normalized_output).resolve()
    if not output_path.is_relative_to(project_dir.resolve()):
        raise ValueError("--output 必须位于项目目录内")
    return output_path, None


def aggregate_review_reports(
    project_dir: Path,
    review_tasks: list[str],
    output_text: str,
    target_task_text: str,
    title: str,
) -> int:
    """汇总多路 reviewer 的 review.md。"""
    normalized_review_tasks = [task_text.strip() for task_text in review_tasks if task_text.strip()]
    if len(normalized_review_tasks) < 2:
        raise ValueError("review-aggregate 至少需要两个 --review-task")
    if len(set(normalized_review_tasks)) != len(normalized_review_tasks):
        raise ValueError("review-aggregate 的 --review-task 不能重复")

    output_path, target_task_meta = resolve_review_aggregate_output(project_dir, output_text, target_task_text)
    if target_task_meta is not None and target_task_meta.task_id in normalized_review_tasks:
        raise ValueError("目标任务不能同时作为 reviewer 任务")

    reviewers = [parse_reviewer_summary(resolve_task(project_dir, task_ref)) for task_ref in normalized_review_tasks]
    aggregate_result = build_review_aggregate_result(reviewers, title, target_task_meta)
    report_text = render_review_aggregate_report(aggregate_result)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")

    relative_output = output_path.relative_to(project_dir.resolve()).as_posix()
    print(f"[OK] 已生成汇总报告：{relative_output}")
    print(f"final_decision: {aggregate_result.final_decision}")
    if target_task_meta is not None:
        print(f"target_task: {target_task_meta.task_id}")
    return 0


def render_meta_text(
    task_id: str,
    title: str,
    owner_agent: str,
    mode: str,
    branch_or_workspace: str,
    allowed_paths: list[str],
    depends_on: list[str],
    doc_targets: list[tuple[str, str]],
    advanced_enabled: bool,
    lane_key: str,
    approval_target: dict[str, str],
    file_leases: list[tuple[str, str]],
) -> str:
    """渲染 .meta.yaml 文本。"""
    lines = [
        f"task_id: {quote_yaml(task_id)}",
        f"title: {quote_yaml(title)}",
        f"owner_agent: {quote_yaml(owner_agent)}",
        f"mode: {quote_yaml(mode)}",
        'status: "todo"',
        f"branch_or_workspace: {quote_yaml(branch_or_workspace)}",
        "allowed_paths:",
    ]
    for path_text in allowed_paths:
        lines.append(f"  - {quote_yaml(path_text)}")

    if depends_on:
        lines.append("depends_on:")
        for dependency_id in depends_on:
            lines.append(f"  - {quote_yaml(dependency_id)}")
    else:
        lines.append("depends_on: []")

    if doc_targets:
        lines.append("doc_targets:")
        for path_text, anchor_text in doc_targets:
            lines.extend(
                [
                    f"  - path: {quote_yaml(path_text)}",
                    f"    section_anchor: {quote_yaml(anchor_text)}",
                ]
            )

    lines.extend(
        [
            'review_state: "pending"',
            'merge_state: "blocked"',
        ]
    )

    if advanced_enabled:
        lines.append(f"lane_key: {quote_yaml(lane_key)}")
        lines.append("approval_target:")
        for key_text in ("gate", "review", "merge"):
            lines.append(f"  {key_text}: {quote_yaml(approval_target[key_text])}")
        if file_leases:
            lines.append("file_leases:")
            for path_text, anchor_text in file_leases:
                lines.extend(
                    [
                        f"  - path: {quote_yaml(path_text)}",
                        f"    section_anchor: {quote_yaml(anchor_text)}",
                        f"    lease_owner: {quote_yaml(task_id)}",
                        '    lease_state: "active"',
                    ]
                )
        else:
            lines.append("file_leases: []")

    lines.append(f"updated_at: {quote_yaml(now_iso())}")
    return "\n".join(lines) + "\n"


def build_review_tracks(review_kind: str) -> list[dict[str, object]]:
    """根据 review 类型返回固定视角。"""
    track_definitions = REVIEW_TRACK_TEMPLATES.get(review_kind, [])
    if not track_definitions:
        raise ValueError(f"不支持的 review_kind：{review_kind}")
    return track_definitions


def create_review_split(
    project_dir: Path,
    title: str,
    topic: str,
    review_kind: str,
    source_paths: list[str],
    task_date: str,
    owner_prefix: str,
    branch_prefix: str,
    approval_gate: str,
    approval_review: str,
    approval_merge: str,
) -> int:
    """按固定视角拆分多专家评审任务骨架。"""
    normalized_source_paths = [normalize_path(path_text) for path_text in source_paths if normalize_path(path_text)]
    if not normalized_source_paths:
        raise ValueError("review-split 至少需要一个 --source-path")

    track_definitions = build_review_tracks(review_kind)
    config_data = load_taskctl_config(project_dir)
    default_approval_target = get_default_approval_target(config_data)
    resolved_approval_target = {
        "gate": approval_gate.strip() or default_approval_target["gate"],
        "review": approval_review.strip() or default_approval_target["review"],
        "merge": approval_merge.strip() or default_approval_target["merge"],
    }
    missing_targets = [key_text for key_text, value_text in resolved_approval_target.items() if not value_text]
    if missing_targets:
        raise ValueError(f"review-split 缺少审批目标：{', '.join(missing_targets)}")

    normalized_owner_prefix = owner_prefix.strip() or "reviewer"
    normalized_branch_prefix = branch_prefix.strip().strip("/") or "review"
    base_topic_slug = slugify_topic(topic)
    created_items: list[tuple[str, str, str]] = []

    for track_definition in track_definitions:
        track_slug = str(track_definition["slug"])
        track_title = str(track_definition["title"])
        task_id = allocate_next_task_id(project_dir)
        track_topic = f"{topic}-{track_slug}"
        task_dir_name = build_task_dir_name(task_id, task_date, track_topic)
        task_dir_path = project_dir / "docs" / "plan" / "tasks" / task_dir_name
        relative_task_path = normalize_path(task_dir_path.relative_to(project_dir).as_posix())
        task_title = f"{title} - {track_title}"
        owner_agent = f"{normalized_owner_prefix}-{track_slug}"
        branch_or_workspace = f"{normalized_branch_prefix}/{base_topic_slug}-{track_slug}"

        create_task(
            project_dir=project_dir,
            task_id_text=task_id,
            title=task_title,
            owner_agent=owner_agent,
            mode="patch",
            branch_or_workspace=branch_or_workspace,
            topic=track_topic,
            allowed_paths=[relative_task_path],
            depends_on=[],
            doc_target_texts=[],
            task_date=task_date,
            advanced_enabled=True,
            auto_advanced=False,
            lane_key=f"lane:review-{track_slug}",
            approval_gate=resolved_approval_target["gate"],
            approval_review=resolved_approval_target["review"],
            approval_merge=resolved_approval_target["merge"],
            file_lease_texts=[],
        )

        (task_dir_path / "task.md").write_text(
            render_review_bundle_task_file(task_id, task_title, review_kind, track_definition, normalized_source_paths),
            encoding="utf-8",
        )
        (task_dir_path / "steps.md").write_text(
            render_review_bundle_steps_file(track_definition, normalized_source_paths),
            encoding="utf-8",
        )
        (task_dir_path / "acceptance.md").write_text(
            render_review_bundle_acceptance_file(track_definition),
            encoding="utf-8",
        )
        (task_dir_path / "handoff.md").write_text(
            render_review_bundle_handoff_file(track_definition),
            encoding="utf-8",
        )
        (task_dir_path / "review.md").write_text(
            render_review_bundle_report_file(review_kind, track_definition, normalized_source_paths),
            encoding="utf-8",
        )
        created_items.append((task_id, track_title, task_dir_path.relative_to(project_dir).as_posix()))

    print(f"[OK] 已创建 {len(created_items)} 个 reviewer 任务")
    for task_id, track_title, relative_path in created_items:
        print(f"- {task_id} | {track_title} | {relative_path}")
    return 0


def create_task(
    project_dir: Path,
    task_id_text: str,
    title: str,
    owner_agent: str,
    mode: str,
    branch_or_workspace: str,
    topic: str,
    allowed_paths: list[str],
    depends_on: list[str],
    doc_target_texts: list[str],
    task_date: str,
    advanced_enabled: bool,
    auto_advanced: bool,
    lane_key: str,
    approval_gate: str,
    approval_review: str,
    approval_merge: str,
    file_lease_texts: list[str],
) -> int:
    """创建任务目录与骨架文件。"""
    tasks_dir = project_dir / "docs" / "plan" / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    config_data = load_taskctl_config(project_dir)

    task_id = validate_task_id(task_id_text) if task_id_text else allocate_next_task_id(project_dir)
    all_tasks = list_task_meta(project_dir)
    existing_task_ids = {task.task_id for task in all_tasks}
    if task_id in existing_task_ids:
        raise ValueError(f"任务已存在：{task_id}")

    normalized_paths: list[str] = []
    for path_text in allowed_paths:
        normalized_path = normalize_path(path_text)
        if normalized_path:
            normalized_paths.append(normalized_path)
    if not normalized_paths:
        raise ValueError("create 至少需要一个 --path")

    normalized_depends = [validate_task_id(dependency_id) for dependency_id in depends_on if dependency_id.strip()]
    normalized_doc_targets = [split_anchor_ref(value_text, "--doc-target") for value_text in doc_target_texts]
    active_tasks = [task for task in all_tasks if task.status in ACTIVE_STATUSES]
    overlapping_tasks = [task for task in active_tasks if has_overlap(normalized_paths, task.allowed_paths)]
    parallel_limit = get_parallel_active_task_limit(config_data)
    auto_triggered = auto_advanced and bool(overlapping_tasks or (len(active_tasks) + 1) >= parallel_limit)
    auto_reasons: list[str] = []
    if auto_triggered:
        if overlapping_tasks:
            auto_reasons.append("path_overlap")
        if (len(active_tasks) + 1) >= parallel_limit:
            auto_reasons.append(f"parallel_active_tasks={len(active_tasks) + 1}")

    draft_task_meta = TaskMeta(
        task_id=task_id,
        title=title,
        owner_agent=owner_agent,
        mode=mode,
        status="todo",
        allowed_paths=normalized_paths,
        depends_on=normalized_depends,
        doc_targets=normalized_doc_targets,
        branch_or_workspace=branch_or_workspace,
    )
    final_advanced_enabled = advanced_enabled or auto_triggered

    if final_advanced_enabled:
        if advanced_enabled and not auto_triggered and not lane_key.strip():
            raise ValueError("advanced 模式必须提供 --lane-key")
        applied_lane_key = lane_key.strip() or suggest_lane_key(draft_task_meta, all_tasks)
        default_approval_target = get_default_approval_target(config_data)
        approval_target = {
            "gate": approval_gate.strip() or (default_approval_target["gate"] if auto_triggered else ""),
            "review": approval_review.strip() or (default_approval_target["review"] if auto_triggered else ""),
            "merge": approval_merge.strip() or (default_approval_target["merge"] if auto_triggered else ""),
        }
        missing_keys = [key_text for key_text, value_text in approval_target.items() if not value_text]
        if missing_keys:
            raise ValueError(f"advanced 模式缺少审批目标：{', '.join(missing_keys)}")
        if file_lease_texts:
            normalized_file_leases = [split_anchor_ref(value_text, "--file-lease") for value_text in file_lease_texts]
        elif auto_triggered:
            normalized_file_leases = derive_file_leases(draft_task_meta, [])
        else:
            normalized_file_leases = []
    else:
        applied_lane_key = ""
        approval_target = {}
        normalized_file_leases = []

    task_dir_name = build_task_dir_name(task_id, task_date, topic)
    task_dir = tasks_dir / task_dir_name
    if task_dir.exists():
        raise ValueError(f"任务已存在：{task_dir_name}")
    task_dir.mkdir(parents=True, exist_ok=False)

    file_map = {
        "task.md": render_task_file(task_id, title, "任务说明"),
        "steps.md": render_task_file(task_id, title, "执行步骤"),
        "acceptance.md": render_task_file(task_id, title, "验收标准"),
        "handoff.md": render_task_file(task_id, title, "交接记录"),
        "review.md": render_task_file(task_id, title, "审查记录"),
        ".meta.yaml": render_meta_text(
            task_id=task_id,
            title=title,
            owner_agent=owner_agent,
            mode=mode,
            branch_or_workspace=branch_or_workspace,
            allowed_paths=normalized_paths,
            depends_on=normalized_depends,
            doc_targets=normalized_doc_targets,
            advanced_enabled=final_advanced_enabled,
            lane_key=applied_lane_key,
            approval_target=approval_target,
            file_leases=normalized_file_leases,
        ),
    }
    for file_name, content_text in file_map.items():
        (task_dir / file_name).write_text(content_text, encoding="utf-8")

    sync_plan(project_dir)
    print(f"[OK] 已创建任务 {task_id}: {task_dir.relative_to(project_dir).as_posix()}")
    if auto_triggered:
        print(f"[AUTO] advanced enabled: {', '.join(auto_reasons)}")
    return 0


def block_task(project_dir: Path, task_ref: str, reason: str, blocked_by: str) -> int:
    """显式阻塞任务。"""
    task_meta = resolve_task(project_dir, task_ref)
    if task_meta.status == "merged":
        raise ValueError("merged 任务不能再 block")
    if not reason.strip():
        raise ValueError("block 必须提供非空 reason")

    queue_path = project_dir / "docs" / "plan" / "MERGE_QUEUE.yaml"
    queue_items = load_queue(queue_path)
    filtered_queue = [item for item in queue_items if item.task_id != task_meta.task_id]
    if len(filtered_queue) != len(queue_items):
        write_queue(queue_path, filtered_queue)

    if task_meta.status == "blocked":
        previous_status = task_meta.blocked_from or "blocked"
    else:
        previous_status = task_meta.status
    review_state = derive_review_state(task_meta)
    update_task_meta_fields(
        task_meta,
        {
            "status": '"blocked"',
            "review_state": quote_yaml(review_state),
            'merge_state': '"blocked"',
            "blocked_from": quote_yaml(previous_status),
            "blocked_reason": quote_yaml(reason.strip()),
            "blocked_by": quote_yaml((blocked_by or "coordinator").strip()),
            "blocked_at": quote_yaml(now_iso()),
            "updated_at": quote_yaml(now_iso()),
        },
    )

    if get_manifest_focus_task_id(project_dir) == task_meta.task_id:
        update_manifest_focus(project_dir, None)

    sync_plan(project_dir)
    print(f"[OK] {task_meta.task_id}: {previous_status} -> blocked")
    return 0


def preflight_task(project_dir: Path, task_ref: str) -> int:
    """输出任务预检结果。"""
    task_meta = resolve_task(project_dir, task_ref)
    all_tasks = list_task_meta(project_dir)
    config_data = load_taskctl_config(project_dir)
    report = build_preflight_report(task_meta, all_tasks, config_data)
    print(render_preflight_report(report))
    return 0 if report.ready_to_start else 2


def proceed_task(project_dir: Path, task_ref: str) -> int:
    """先执行 preflight，通过后再推进到 doing。"""
    task_meta = resolve_task(project_dir, task_ref)
    all_tasks = list_task_meta(project_dir)
    config_data = load_taskctl_config(project_dir)
    report = build_preflight_report(task_meta, all_tasks, config_data)
    print(render_preflight_report(report))
    if not report.ready_to_start:
        return 2
    return transition_task(project_dir, task_ref, "doing")


def route_task(
    project_dir: Path,
    allowed_paths: list[str],
    doc_target_texts: list[str],
    requires_worktree: bool,
    requires_stack: bool,
) -> int:
    """输出任务草案的模式路由建议。"""
    report = build_route_report(project_dir, allowed_paths, doc_target_texts, requires_worktree, requires_stack)
    print(render_route_report(report))
    return 0


def create_task_from_route(
    project_dir: Path,
    title: str,
    owner_agent: str,
    branch_or_workspace: str,
    topic: str,
    allowed_paths: list[str],
    doc_target_texts: list[str],
    requires_worktree: bool,
    requires_stack: bool,
    task_date: str,
) -> int:
    """根据 route 建议直接创建任务。"""
    report = build_route_report(project_dir, allowed_paths, doc_target_texts, requires_worktree, requires_stack)
    print(render_route_report(report))
    return create_task(
        project_dir=project_dir,
        task_id_text="",
        title=title,
        owner_agent=owner_agent,
        mode=report.recommended_execution_mode,
        branch_or_workspace=branch_or_workspace,
        topic=topic,
        allowed_paths=allowed_paths,
        depends_on=[],
        doc_target_texts=doc_target_texts,
        task_date=task_date,
        advanced_enabled=False,
        auto_advanced=report.recommended_create_flag == "--auto-advanced",
        lane_key="",
        approval_gate="",
        approval_review="",
        approval_merge="",
        file_lease_texts=[],
    )


def load_project_dir(project_dir_text: str) -> Path:
    """解析项目根目录。"""
    if project_dir_text:
        return Path(project_dir_text).resolve()
    return Path.cwd().resolve()


def transition_task(project_dir: Path, task_ref: str, target_status: str) -> int:
    """执行状态迁移。"""
    task_meta = resolve_task(project_dir, task_ref)
    allowed_previous = TRANSITION_RULES[target_status]
    if task_meta.status not in allowed_previous:
        raise ValueError(f"非法状态迁移：{task_meta.status} -> {target_status}")

    all_tasks = list_task_meta(project_dir)
    task_map = {task.task_id: task for task in all_tasks}
    queue_path = project_dir / "docs" / "plan" / "MERGE_QUEUE.yaml"
    queue_items = load_queue(queue_path)

    if target_status == "doing":
        validate_start(task_meta, all_tasks)
        update_task_meta(task_meta, "doing", "pending", "blocked")
        update_manifest_focus(project_dir, task_meta)
    elif target_status == "in_review":
        update_task_meta(task_meta, "in_review", "in_review", "blocked")
        update_manifest_focus(project_dir, task_meta)
    elif target_status == "approved":
        validate_approve(task_meta)
        update_task_meta(task_meta, "approved", "approved", "ready")
    elif target_status == "queued":
        validate_enqueue(task_meta, task_map, queue_items)
        queue_items.append(
            QueueItem(
                task_id=task_meta.task_id,
                merge_ref=task_meta.branch_or_workspace,
                queued_at=now_iso(),
            )
        )
        write_queue(queue_path, queue_items)
        update_task_meta(task_meta, "queued", "approved", "queued")
    elif target_status == "merged":
        validate_merge(task_meta, queue_items)
        queue_items = [item for item in queue_items if item.task_id != task_meta.task_id]
        write_queue(queue_path, queue_items)
        update_task_meta(task_meta, "merged", "approved", "merged")
        update_manifest_focus(project_dir, None)
    else:
        raise ValueError(f"不支持的目标状态: {target_status}")

    sync_plan(project_dir)
    print(f"[OK] {task_meta.task_id}: {task_meta.status} -> {target_status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """构建命令行解析器。"""
    parser = argparse.ArgumentParser(description="维护并行协作任务状态机与 merge queue")
    parser.add_argument("--project-dir", default="", help="项目根目录，可选")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sync", help="刷新 PLAN.md 状态汇总")

    create_parser = subparsers.add_parser("create", help="创建任务目录与元数据骨架")
    create_parser.add_argument("--task", default="", help="任务 ID，可选，格式 T001")
    create_parser.add_argument("--title", required=True, help="任务标题")
    create_parser.add_argument("--owner", required=True, help="任务 owner_agent")
    create_parser.add_argument("--mode", required=True, help="任务执行模式，如 patch / stack / worktree")
    create_parser.add_argument("--branch", required=True, help="branch_or_workspace")
    create_parser.add_argument("--topic", required=True, help="目录 slug 来源")
    create_parser.add_argument("--path", action="append", required=True, help="允许改动路径，可重复")
    create_parser.add_argument("--depends", action="append", default=[], help="依赖任务 ID，可重复")
    create_parser.add_argument("--doc-target", action="append", default=[], help="文档目标，格式 path#section_anchor")
    create_parser.add_argument("--date", default="", help="任务日期，可选，格式 YYYY-MM-DD")
    create_parser.add_argument("--advanced", action="store_true", help="是否启用 advanced 模式")
    create_parser.add_argument("--auto-advanced", action="store_true", help="命中升级条件时自动切到 advanced，并补默认字段")
    create_parser.add_argument("--lane-key", default="", help="advanced 模式 lane_key")
    create_parser.add_argument("--approval-gate", default="", help="advanced 模式 gate 审批目标；auto-advanced 时可走项目默认值")
    create_parser.add_argument("--approval-review", default="", help="advanced 模式 review 审批目标；auto-advanced 时可走项目默认值")
    create_parser.add_argument("--approval-merge", default="", help="advanced 模式 merge 审批目标；auto-advanced 时可走项目默认值")
    create_parser.add_argument("--file-lease", action="append", default=[], help="advanced file lease，格式 path#section_anchor")

    block_parser = subparsers.add_parser("block", help="将任务显式标记为 blocked")
    block_parser.add_argument("--task", required=True, help="任务 ID 或任务目录名")
    block_parser.add_argument("--reason", required=True, help="阻塞原因")
    block_parser.add_argument("--by", default="coordinator", help="阻塞执行者")

    preflight_parser = subparsers.add_parser("preflight", help="预检任务能否进入 doing，并给出模式路由建议")
    preflight_parser.add_argument("--task", required=True, help="任务 ID 或任务目录名")

    proceed_parser = subparsers.add_parser("proceed", help="先执行 preflight，通过后再推进到 doing")
    proceed_parser.add_argument("--task", required=True, help="任务 ID 或任务目录名")

    review_split_parser = subparsers.add_parser("review-split", help="按固定视角拆分 3 路多专家评审任务")
    review_split_parser.add_argument("--title", required=True, help="评审任务标题")
    review_split_parser.add_argument("--topic", required=True, help="目录 slug 来源")
    review_split_parser.add_argument(
        "--review-kind",
        required=True,
        choices=sorted(REVIEW_TRACK_TEMPLATES.keys()),
        help="评审类型：code / algorithm / document / mixed",
    )
    review_split_parser.add_argument("--source-path", action="append", required=True, help="只读输入路径，可重复")
    review_split_parser.add_argument("--date", default="", help="任务日期，可选，格式 YYYY-MM-DD")
    review_split_parser.add_argument("--owner-prefix", default="reviewer", help="reviewer owner 前缀")
    review_split_parser.add_argument("--branch-prefix", default="review", help="branch_or_workspace 前缀")
    review_split_parser.add_argument("--approval-gate", default="", help="gate 审批目标；未传时使用项目默认值")
    review_split_parser.add_argument("--approval-review", default="", help="review 审批目标；未传时使用项目默认值")
    review_split_parser.add_argument("--approval-merge", default="", help="merge 审批目标；未传时使用项目默认值")

    review_aggregate_parser = subparsers.add_parser("review-aggregate", help="汇总多路 reviewer 的 review.md")
    review_aggregate_parser.add_argument("--review-task", action="append", required=True, help="reviewer 任务 ID，可重复")
    review_aggregate_parser.add_argument("--output", default="", help="输出路径，项目根目录相对路径")
    review_aggregate_parser.add_argument("--target-task", default="", help="将结果写回目标任务的 review.md")
    review_aggregate_parser.add_argument("--title", default="", help="汇总标题，可选")

    route_parser = subparsers.add_parser("route", help="为任务草案输出协作模式与执行模式建议")
    route_parser.add_argument("--path", action="append", required=True, help="任务草案允许改动路径，可重复")
    route_parser.add_argument("--doc-target", action="append", default=[], help="文档目标，格式 path#section_anchor")
    route_mode_group = route_parser.add_mutually_exclusive_group()
    route_mode_group.add_argument("--requires-worktree", action="store_true", help="独立编译 / 运行 / 测试需求，建议 worktree")
    route_mode_group.add_argument("--requires-stack", action="store_true", help="分支级顺序集成需求，建议 stack")

    create_from_route_parser = subparsers.add_parser("create-from-route", help="先 route 再 create，一步创建任务")
    create_from_route_parser.add_argument("--title", required=True, help="任务标题")
    create_from_route_parser.add_argument("--owner", required=True, help="任务 owner_agent")
    create_from_route_parser.add_argument("--branch", required=True, help="branch_or_workspace")
    create_from_route_parser.add_argument("--topic", required=True, help="目录 slug 来源")
    create_from_route_parser.add_argument("--path", action="append", required=True, help="任务草案允许改动路径，可重复")
    create_from_route_parser.add_argument("--doc-target", action="append", default=[], help="文档目标，格式 path#section_anchor")
    create_from_route_parser.add_argument("--date", default="", help="任务日期，可选，格式 YYYY-MM-DD")
    create_from_route_mode_group = create_from_route_parser.add_mutually_exclusive_group()
    create_from_route_mode_group.add_argument("--requires-worktree", action="store_true", help="独立编译 / 运行 / 测试需求，建议 worktree")
    create_from_route_mode_group.add_argument("--requires-stack", action="store_true", help="分支级顺序集成需求，建议 stack")

    upgrade_parser = subparsers.add_parser("upgrade-advanced", help="根据 preflight 建议补齐 advanced 所需字段")
    upgrade_parser.add_argument("--task", required=True, help="任务 ID 或任务目录名")
    upgrade_parser.add_argument("--lane-key", default="", help="可选，手工指定 lane_key；默认使用建议值")
    upgrade_parser.add_argument("--approval-gate", default="", help="gate 审批目标；未传时使用项目默认值")
    upgrade_parser.add_argument("--approval-review", default="", help="review 审批目标；未传时使用项目默认值")
    upgrade_parser.add_argument("--approval-merge", default="", help="merge 审批目标；未传时使用项目默认值")
    upgrade_parser.add_argument("--file-lease", action="append", default=[], help="可重复，格式 path#section_anchor")

    for command_name in ("start", "submit", "approve", "enqueue", "merge"):
        command_parser = subparsers.add_parser(command_name, help=f"将任务推进到 {command_name} 对应状态")
        command_parser.add_argument("--task", required=True, help="任务 ID 或任务目录名")

    return parser


def main(argv: list[str] | None = None) -> int:
    """脚本入口。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    project_dir = load_project_dir(args.project_dir)

    try:
        if args.command == "sync":
            sync_plan(project_dir)
            print("[OK] PLAN.md 已同步")
            return 0
        if args.command == "create":
            return create_task(
                project_dir=project_dir,
                task_id_text=args.task,
                title=args.title,
                owner_agent=args.owner,
                mode=args.mode,
                branch_or_workspace=args.branch,
                topic=args.topic,
                allowed_paths=args.path,
                depends_on=args.depends,
                doc_target_texts=args.doc_target,
                task_date=resolve_task_date(args.date),
                advanced_enabled=args.advanced,
                auto_advanced=args.auto_advanced,
                lane_key=args.lane_key,
                approval_gate=args.approval_gate,
                approval_review=args.approval_review,
                approval_merge=args.approval_merge,
                file_lease_texts=args.file_lease,
            )
        if args.command == "block":
            return block_task(project_dir, args.task, args.reason, args.by)
        if args.command == "preflight":
            return preflight_task(project_dir, args.task)
        if args.command == "proceed":
            return proceed_task(project_dir, args.task)
        if args.command == "review-split":
            return create_review_split(
                project_dir=project_dir,
                title=args.title,
                topic=args.topic,
                review_kind=args.review_kind,
                source_paths=args.source_path,
                task_date=resolve_task_date(args.date),
                owner_prefix=args.owner_prefix,
                branch_prefix=args.branch_prefix,
                approval_gate=args.approval_gate,
                approval_review=args.approval_review,
                approval_merge=args.approval_merge,
            )
        if args.command == "review-aggregate":
            return aggregate_review_reports(
                project_dir=project_dir,
                review_tasks=args.review_task,
                output_text=args.output,
                target_task_text=args.target_task,
                title=args.title,
            )
        if args.command == "route":
            return route_task(project_dir, args.path, args.doc_target, args.requires_worktree, args.requires_stack)
        if args.command == "create-from-route":
            return create_task_from_route(
                project_dir=project_dir,
                title=args.title,
                owner_agent=args.owner,
                branch_or_workspace=args.branch,
                topic=args.topic,
                allowed_paths=args.path,
                doc_target_texts=args.doc_target,
                requires_worktree=args.requires_worktree,
                requires_stack=args.requires_stack,
                task_date=resolve_task_date(args.date),
            )
        if args.command == "upgrade-advanced":
            return upgrade_task_to_advanced(
                project_dir,
                args.task,
                args.lane_key,
                args.approval_gate,
                args.approval_review,
                args.approval_merge,
                args.file_lease,
            )
        if args.command == "start":
            return transition_task(project_dir, args.task, "doing")
        if args.command == "submit":
            return transition_task(project_dir, args.task, "in_review")
        if args.command == "approve":
            return transition_task(project_dir, args.task, "approved")
        if args.command == "enqueue":
            return transition_task(project_dir, args.task, "queued")
        if args.command == "merge":
            return transition_task(project_dir, args.task, "merged")
        raise ValueError(f"未知命令: {args.command}")
    except Exception as exc:
        print(f"[taskctl] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
