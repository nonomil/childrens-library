"""generate-docs 子命令：从 scan-data.json 代码生成 01-06 结构化文档模板。

只做数据→文档的结构化映射，将 Mermaid/SVG 图、表格、目录等
机械性工作用代码完成，留给 AI 的只剩语义填充。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from scan_shared import (
    get_module_rows,
    get_function_rows,
    get_dataflow_rows,
    get_datastructure_rows,
    get_constraint_rows,
    get_impact_rows,
)


# ── 数据加载 ──────────────────────────────────────────────


def _load_scan_data(scan_data_path: Path) -> dict:
    """加载 scan-data.json，失败则中止。"""
    if not scan_data_path.exists():
        print(f"[ERR] 文件不存在: {scan_data_path}", file=sys.stderr)
        sys.exit(1)
    with scan_data_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# ── Mermaid 生成器 ────────────────────────────────────────


def _mermaid_module_deps(modules: list[dict]) -> str:
    """01 架构图：模块依赖关系 Mermaid graph TD。"""
    lines = ["graph TD"]
    for mod in modules:
        mid = _safe_id(mod.get("module_id", "") or mod.get("name", ""))
        label = mod.get("name", "")
        loc = mod.get("loc") or mod.get("function_count", "")
        lines.append(f"    {mid}[\"{label} ({loc})\"]")
        for dep in mod.get("dependencies") or []:
            dep_id = _safe_id(dep)
            lines.append(f"    {mid} -->|依赖| {dep_id}")
    return "\n".join(lines)


def _mermaid_file_deps(modules: list[dict]) -> str:
    """01 架构图：文件级依赖 Mermaid graph LR。"""
    lines = ["graph LR"]
    for mod in modules:
        mid = _safe_id(mod.get("module_id", "") or mod.get("name", ""))
        files = mod.get("files") or []
        for fname in files[:5]:
            fid = _safe_id(fname)
            lines.append(f"    {fid}[\"{fname}\"] -->|属于| {mid}")
    return "\n".join(lines)


def _mermaid_data_flow_lr(flows: list[dict]) -> str:
    """02 数据流图：端到端数据流 Mermaid graph LR。"""
    lines = ["graph LR"]
    for flow in flows:
        fid = _safe_id(flow.get("id", "") or flow.get("name", ""))
        steps = flow.get("steps") or []
        for i, step in enumerate(steps):
            if isinstance(step, dict):
                step_name = step.get("name", "")
            else:
                step_name = str(step)
            sid = f"{fid}_s{i}"
            lines.append(f"    {sid}[\"{step_name}\"]")
            if i > 0:
                prev_id = f"{fid}_s{i - 1}"
                lines.append(f"    {prev_id} -->|数据传递| {sid}")
    return "\n".join(lines)


def _mermaid_class_diagram(structures: list[dict]) -> str:
    """02 数据流图：核心数据结构 classDiagram。"""
    lines = ["classDiagram"]
    for ds in structures:
        name = ds.get("name", "Unknown")
        sid = _safe_id(name)
        fields = ds.get("key_fields") or ds.get("fields") or []
        lines.append(f"    class {sid} {{")
        for field in fields[:8]:
            lines.append(f"        +{field}")
        lines.append("    }")
    return "\n".join(lines)


def _mermaid_sequence(apis: list[dict]) -> str:
    """03 API 文档：关键调用链 sequenceDiagram。"""
    lines = ["sequenceDiagram"]
    participants = set()
    for api in apis[:8]:
        module = api.get("module", "") or api.get("file_line", "")
        mod_label = module.split("/")[0] if "/" in module else module or "main"
        if mod_label not in participants:
            participants.add(mod_label)
            lines.append(f"    participant {mod_label}")
        name = api.get("name", "")
        lines.append(f"    {mod_label}->>{mod_label}: {name}()")
    return "\n".join(lines)


def _mermaid_impact_propagation(impacts: list[dict]) -> str:
    """05 影响矩阵：影响传播图 Mermaid graph TD。"""
    lines = ["graph TD"]
    for item in impacts[:6]:
        iid = _safe_id(item.get("id", "") or item.get("change_point", ""))
        cp = item.get("change_point", "")
        risk = item.get("risk_level", "")
        fill = "#fecaca" if risk == "high" else "#fef3c7"
        lines.append(f"    {iid}[\"{cp}\"]")
        for mod in item.get("affected_modules") or []:
            mid = _safe_id(mod)
            lines.append(f"    {iid} -->|影响| {mid}[\"{mod}\"]")
    return "\n".join(lines)


def _mermaid_task_deps(modules: list[dict]) -> str:
    """06 执行摘要：任务依赖图 Mermaid graph TD。"""
    lines = ["graph TD"]
    for mod in modules:
        mid = _safe_id(mod.get("module_id", "") or mod.get("name", ""))
        name = mod.get("name", "")
        lines.append(f"    {mid}[\"{name}\"]")
        for dep in mod.get("dependencies") or []:
            dep_id = _safe_id(dep)
            lines.append(f"    {mid} -->|依赖| {dep_id}")
    return "\n".join(lines)


# ── SVG 生成器 ────────────────────────────────────────────


def _svg_wrap(inner: str, view_w: int = 800, view_h: int = 300) -> str:
    """通用 SVG 包装器。"""
    return (
        f'<svg viewBox="0 0 {view_w} {view_h}" xmlns="http://www.w3.org/2000/svg">'
        f"\n{inner}\n</svg>"
    )


def _svg_layered_arch(modules: list[dict]) -> str:
    """01 架构图：分层架构 SVG。"""
    colors = ["#dbeafe", "#dcfce7", "#ffedd5", "#ede9fe"]
    y = 20
    rects = []
    labels = []
    for i, mod in enumerate(modules):
        color = colors[i % len(colors)]
        name = mod.get("name", "")
        func_count = mod.get("function_count", 0)
        rects.append(
            f'<rect x="80" y="{y}" width="640" height="50" rx="8" '
            f'fill="{color}" stroke="#94a3b8" stroke-width="1"/>'
        )
        labels.append(
            f'<text x="400" y="{y + 30}" text-anchor="middle" '
            f'font-size="14" font-weight="600" fill="#1e293b">'
            f"{name} ({func_count} 函数)</text>"
        )
        y += 64
    h = y + 20
    inner = (
        '<g id="background">'
        f'<rect x="20" y="10" width="760" height="{h - 10}" rx="12" '
        f'fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/></g>\n'
        f'<g id="nodes">\n' + "\n".join(rects) + "\n</g>\n"
        f'<g id="labels">\n' + "\n".join(labels) + "\n</g>"
    )
    return _svg_wrap(inner, 800, h)


def _svg_file_tree(modules: list[dict]) -> str:
    """01 架构图：文件树 SVG。"""
    y = 40
    items = []
    for mod in modules:
        name = mod.get("name", "")
        items.append(
            f'<text x="40" y="{y}" font-size="13" font-weight="700" '
            f'fill="#1e293b">{name}/</text>'
        )
        y += 22
        for f in (mod.get("files") or [])[:5]:
            items.append(
                f'<text x="64" y="{y}" font-size="11" fill="#64748b">'
                f"{f}</text>"
            )
            y += 18
        y += 8
    h = y + 20
    inner = (
        '<g id="background">'
        f'<rect x="20" y="10" width="500" height="{h - 10}" rx="12" '
        f'fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/></g>\n'
        f'<g id="labels">\n' + "\n".join(items) + "\n</g>"
    )
    return _svg_wrap(inner, 540, h)


def _svg_storage_layer(structures: list[dict]) -> str:
    """02 数据流图：存储层 SVG。"""
    y = 30
    rects = []
    labels = []
    for ds in structures:
        name = ds.get("name", "")
        kind = ds.get("kind", "")
        fields = ds.get("key_fields") or []
        rects.append(
            f'<rect x="40" y="{y}" width="720" height="60" rx="8" '
            f'fill="#dbeafe" stroke="#3b82f6" stroke-width="1"/>'
        )
        labels.append(
            f'<text x="60" y="{y + 24}" font-size="13" font-weight="600" '
            f'fill="#1e40af">{name} ({kind})</text>'
        )
        labels.append(
            f'<text x="60" y="{y + 46}" font-size="11" fill="#64748b">'
            f'字段: {", ".join(fields[:6])}</text>'
        )
        y += 74
    h = y + 20
    inner = (
        f'<g id="nodes">\n' + "\n".join(rects) + "\n</g>\n"
        f'<g id="labels">\n' + "\n".join(labels) + "\n</g>"
    )
    return _svg_wrap(inner, 800, max(h, 100))


def _svg_api_cards(apis: list[dict]) -> str:
    """03 API 文档：API 分类卡片 SVG。"""
    groups: dict[str, list[dict]] = {}
    for api in apis[:20]:
        mod = api.get("module", "") or "other"
        groups.setdefault(mod, []).append(api)
    colors = ["#dbeafe", "#dcfce7", "#ffedd5", "#ede9fe"]
    y = 30
    rects = []
    labels = []
    for i, (mod, items) in enumerate(groups.items()):
        color = colors[i % len(colors)]
        rects.append(
            f'<rect x="30" y="{y}" width="740" height="40" rx="6" '
            f'fill="{color}" stroke="#94a3b8" stroke-width="1"/>'
        )
        names = ", ".join(a.get("name", "") for a in items[:5])
        labels.append(
            f'<text x="50" y="{y + 25}" font-size="12" fill="#1e293b">'
            f"{mod}: {names}</text>"
        )
        y += 52
    h = y + 20
    inner = (
        f'<g id="nodes">\n' + "\n".join(rects) + "\n</g>\n"
        f'<g id="labels">\n' + "\n".join(labels) + "\n</g>"
    )
    return _svg_wrap(inner, 800, max(h, 100))


def _svg_constraint_matrix(constraints: list[dict]) -> str:
    """04 约束文档：约束分类矩阵 SVG。"""
    y = 30
    items = []
    for c in constraints[:12]:
        content = (c.get("content") or "")[:60]
        source = (c.get("source_doc") or "")[:30]
        items.append(
            f'<rect x="40" y="{y}" width="720" height="30" rx="4" '
            f'fill="#fef3c7" stroke="#f59e0b" stroke-width="0.8"/>'
        )
        items.append(
            f'<text x="50" y="{y + 20}" font-size="10" fill="#1e293b">'
            f"{content}</text>"
        )
        items.append(
            f'<text x="700" y="{y + 20}" font-size="9" fill="#64748b">'
            f"{source}</text>"
        )
        y += 38
    h = y + 20
    inner = '<g id="nodes">\n' + "\n".join(items) + "\n</g>"
    return _svg_wrap(inner, 800, max(h, 80))


def _svg_impact_heatmap(impacts: list[dict], modules: list[dict]) -> str:
    """05 影响矩阵：影响范围热力图 SVG。"""
    mod_names = [m.get("name", "") for m in modules]
    cell_w = 80
    cell_h = 28
    label_w = 140
    header_h = 40
    total_w = label_w + len(mod_names) * cell_w + 40
    total_h = header_h + len(impacts) * (cell_h + 4) + 40
    items = []
    for j, mn in enumerate(mod_names):
        x = label_w + j * cell_w
        items.append(
            f'<text x="{x + cell_w // 2}" y="{header_h}" text-anchor="middle" '
            f'font-size="10" font-weight="600" fill="#334155">{mn}</text>'
        )
    for i, imp in enumerate(impacts[:8]):
        y = header_h + 10 + i * (cell_h + 4)
        cp = (imp.get("change_point") or "")[:18]
        items.append(
            f'<text x="{label_w - 5}" y="{y + cell_h // 2 + 4}" '
            f'text-anchor="end" font-size="9" fill="#1e293b">{cp}</text>'
        )
        affected = set(imp.get("affected_modules") or [])
        risk = imp.get("risk_level", "medium")
        for j, mn in enumerate(mod_names):
            x = label_w + j * cell_w
            if mn in affected:
                fill = "#fecaca" if risk == "high" else "#fef3c7"
                stroke = "#ef4444" if risk == "high" else "#f59e0b"
            else:
                fill = "#f1f5f9"
                stroke = "#e2e8f0"
            items.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 4}" height="{cell_h}" '
                f'rx="4" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>'
            )
    inner = '<g id="labels">\n' + "\n".join(items) + "\n</g>"
    return _svg_wrap(inner, max(total_w, 400), max(total_h, 100))


def _svg_priority_matrix(impacts: list[dict]) -> str:
    """06 执行摘要：四象限优先级矩阵 SVG。"""
    w, h = 800, 400
    cx, cy = w // 2, h // 2
    quadrants = [
        (f'<rect x="40" y="30" width="{cx - 40}" height="{cy - 30}" rx="0" fill="#fef3c7" opacity="0.3"/>'),
        (f'<rect x="{cx}" y="30" width="{cx - 40}" height="{cy - 30}" rx="0" fill="#fecaca" opacity="0.3"/>'),
        (f'<rect x="40" y="{cy}" width="{cx - 40}" height="{cy - 30}" rx="0" fill="#e2e8f0" opacity="0.3"/>'),
        (f'<rect x="{cx}" y="{cy}" width="{cx - 40}" height="{cy - 30}" rx="0" fill="#dcfce7" opacity="0.3"/>'),
    ]
    q_labels = [
        f'<text x="{(cx + 40) // 2}" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#92400e">低影响·高频变更</text>',
        f'<text x="{(cx + w - 40) // 2}" y="50" text-anchor="middle" font-size="11" font-weight="700" fill="#991b1b">高影响·高频变更</text>',
        f'<text x="{(cx + 40) // 2}" y="{cy + 20}" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">低影响·稳定</text>',
        f'<text x="{(cx + w - 40) // 2}" y="{cy + 20}" text-anchor="middle" font-size="11" font-weight="700" fill="#14532d">高影响·稳定</text>',
    ]
    dots = []
    for i, imp in enumerate(impacts[:6]):
        risk = imp.get("risk_level", "medium")
        x = (cx + 60 + (i * 47)) % (w - 120) + 60
        y = (80 + (i * 53)) % (h - 120) + 60
        fill = "#ef4444" if risk == "high" else "#f59e0b"
        r = 16 if risk == "high" else 12
        dots.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="0.7"/>'
        )
        name = (imp.get("change_point") or "")[:12]
        dots.append(
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="8" fill="#fff">{name}</text>'
        )
    inner = (
        f'<g id="background"><rect x="30" y="20" width="{w - 60}" height="{h - 40}" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/></g>\n'
        f'<g id="edges"><line x1="{cx}" y1="30" x2="{cx}" y2="{h - 30}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="6,4"/><line x1="40" y1="{cy}" x2="{w - 40}" y2="{cy}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="6,4"/></g>\n'
        f'<g id="nodes">\n' + "\n".join(quadrants) + "\n" + "\n".join(dots) + "\n</g>\n"
        f'<g id="labels">\n' + "\n".join(q_labels) + "\n</g>"
    )
    return _svg_wrap(inner, w, h)


def _svg_bar_chart(modules: list[dict]) -> str:
    """06 执行摘要：模块 LOC/函数数 水平条形图 SVG。"""
    colors = ["#4ade80", "#38bdf8", "#fb923c", "#a78bfa", "#f472b6"]
    max_val = max((m.get("function_count", 0) for m in modules), default=1) or 1
    bar_h = 28
    gap = 10
    label_w = 100
    chart_w = 600
    y = 50
    bars = []
    labels = []
    for i, mod in enumerate(modules):
        color = colors[i % len(colors)]
        val = mod.get("function_count", 0)
        bw = int(val / max_val * chart_w) if max_val else 0
        name = mod.get("name", "")
        bars.append(
            f'<rect x="{label_w}" y="{y}" width="{bw}" height="{bar_h}" '
            f'rx="6" fill="{color}"/>'
        )
        labels.append(
            f'<text x="{label_w - 10}" y="{y + bar_h // 2 + 4}" '
            f'text-anchor="end" font-size="11" fill="#334155">{name}</text>'
        )
        labels.append(
            f'<text x="{label_w + bw + 8}" y="{y + bar_h // 2 + 4}" '
            f'font-size="10" fill="#64748b">{val} 函数</text>'
        )
        y += bar_h + gap
    h = y + 20
    inner = (
        f'<g id="background"><rect x="20" y="10" width="800" height="{h}" rx="14" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/></g>\n'
        f'<g id="labels"><text x="400" y="38" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">模块规模对比</text></g>\n'
        f'<g id="nodes">\n' + "\n".join(bars) + "\n</g>\n"
        f'<g id="labels">\n' + "\n".join(labels) + "\n</g>"
    )
    return _svg_wrap(inner, 840, h + 10)


# ── 辅助工具 ──────────────────────────────────────────────


def _safe_id(text: str) -> str:
    """将文本转为合法 Mermaid 节点 ID（仅英文字母数字下划线）。"""
    import re

    return re.sub(r"[^a-zA-Z0-9_]", "_", text)[:40] or "node"


def _toc(headings: list[str]) -> str:
    """生成目录 Markdown。"""
    lines = ["## 目录", ""]
    for h in headings:
        anchor = h.strip().lower().replace(" ", "-")
        lines.append(f"- [{h}](#{anchor})")
    lines.append("")
    return "\n".join(lines)


def _module_table(modules: list[dict]) -> str:
    """生成模块概览表格。"""
    lines = [
        "| 模块 | 文件数 | 函数数 | 职责 |",
        "|------|--------|--------|------|",
    ]
    for m in modules:
        name = m.get("name", "")
        fc = m.get("function_count", 0)
        filec = m.get("file_count", 0)
        resp = (m.get("responsibility") or "")[:50]
        lines.append(f"| {name} | {filec} | {fc} | {resp} |")
    lines.append("")
    return "\n".join(lines)


def _entry_point_table(entries: list[dict]) -> str:
    """生成入口点表格。"""
    lines = [
        "| 入口点 | 文件 | 触发方式 |",
        "|--------|------|---------|",
    ]
    for e in entries:
        name = e.get("name", "")
        file = (e.get("file") or "")[:40]
        trigger = e.get("trigger", "")
        lines.append(f"| `{name}()` | `{file}` | {trigger} |")
    lines.append("")
    return "\n".join(lines)


def _flow_table(flows: list[dict]) -> str:
    """生成数据流表格。"""
    lines = [
        "| 流程 | 步骤数 | 涉及模块 |",
        "|------|--------|---------|",
    ]
    for f in flows:
        name = f.get("name", "")
        steps = len(f.get("steps") or [])
        mods = ", ".join(f.get("modules_involved") or [])
        lines.append(f"| {name} | {steps} | {mods} |")
    lines.append("")
    return "\n".join(lines)


def _constraint_table(constraints: list[dict]) -> str:
    """生成约束表格。"""
    lines = [
        "| 约束 | 来源 | 类型 |",
        "|------|------|------|",
    ]
    for c in constraints[:20]:
        content = (c.get("content") or "")[:60]
        source = (c.get("source_doc") or "")[:30]
        ctype = c.get("constraint_type") or c.get("adopt", "")[:20]
        lines.append(f"| {content} | {source} | {ctype} |")
    lines.append("")
    return "\n".join(lines)


def _impact_table(impacts: list[dict]) -> str:
    """生成影响矩阵表格。"""
    lines = [
        "| 变更点 | 风险 | 直接影响 |",
        "|--------|------|---------|",
    ]
    for imp in impacts:
        cp = (imp.get("change_point") or "")[:25]
        risk = imp.get("risk_level", "")
        direct = (imp.get("direct_impact") or "")[:50]
        lines.append(f"| {cp} | {risk} | {direct} |")
    lines.append("")
    return "\n".join(lines)


# ── 文档生成器（01-06） ──────────────────────────────────


def _gen_01_architecture(data: dict) -> str:
    """01-architecture.md 模板。"""
    meta = data.get("scan_meta", {})
    modules = get_module_rows(data)
    entries = data.get("entry_points") or []
    topic = meta.get("scan_topic", "")

    sections = [
        "概览图",
        "模块依赖",
        "分层架构",
        "文件结构",
        "入口点",
        "关键约束",
    ]
    parts = [
        f"# 01 架构文档（{topic}）",
        "",
        f"> {len(modules)} 模块 · {sum(m.get('function_count', 0) for m in modules)} 函数 · "
        f"{len(entries)} 入口点",
        "",
        _toc(sections),
        "## 概览图",
        "",
        "```mermaid",
        _mermaid_module_deps(modules),
        "```",
        "",
        "## 模块依赖",
        "",
        _module_table(modules),
        "## 分层架构",
        "",
        _svg_layered_arch(modules),
        "",
        "## 文件结构",
        "",
        _svg_file_tree(modules),
        "",
        "## 入口点",
        "",
        _entry_point_table(entries),
        "## 关键约束",
        "",
        "<!-- AI: 从 scan-data.json 的 reference_constraints 和代码约束中提取 -->",
        "",
        _constraint_table(get_constraint_rows(data)),
    ]
    return "\n".join(parts)


def _gen_02_dataflow(data: dict) -> str:
    """02-dataflow.md 模板。"""
    meta = data.get("scan_meta", {})
    flows = get_dataflow_rows(data)
    structures = get_datastructure_rows(data)
    topic = meta.get("scan_topic", "")

    sections = [
        "概览图",
        "核心流程",
        "数据结构",
        "存储层",
    ]
    parts = [
        f"# 02 数据流文档（{topic}）",
        "",
        f"> {len(flows)} 条核心流程 · {len(structures)} 种数据结构",
        "",
        _toc(sections),
        "## 概览图",
        "",
        "```mermaid",
        _mermaid_data_flow_lr(flows),
        "```",
        "",
        "## 核心流程",
        "",
        _flow_table(flows),
        "<!-- AI: 对每条流程展开步骤描述、输入输出格式 -->",
        "",
        "## 数据结构",
        "",
        "```mermaid",
        _mermaid_class_diagram(structures),
        "```",
        "",
        "<!-- AI: 补充每个数据结构的字段说明和用途 -->",
        "",
        "## 存储层",
        "",
        _svg_storage_layer(structures),
        "",
    ]
    return "\n".join(parts)


def _gen_03_api_surface(data: dict) -> str:
    """03-api-surface.md 模板。"""
    meta = data.get("scan_meta", {})
    apis = data.get("api_surface") or get_function_rows(data)
    topic = meta.get("scan_topic", "")
    public_apis = [a for a in apis if a.get("is_public")] if apis and apis[0].get("is_public") is not None else apis[:30]

    sections = [
        "概览图",
        "API 分类",
        "关键调用链",
        "公开接口清单",
    ]
    parts = [
        f"# 03 API 文档（{topic}）",
        "",
        f"> {len(public_apis)} 个公开接口",
        "",
        _toc(sections),
        "## 概览图",
        "",
        _svg_api_cards(public_apis),
        "",
        "## API 分类",
        "",
        "<!-- AI: 按职责分组（检测/分析/导出/UI/工具），每组列出关键函数 -->",
        "",
        "## 关键调用链",
        "",
        "```mermaid",
        _mermaid_sequence(public_apis),
        "```",
        "",
        "## 公开接口清单",
        "",
        "| 函数 | 文件位置 | 签名 |",
        "|------|---------|------|",
    ]
    for api in public_apis[:30]:
        name = api.get("name", "")
        fl = (api.get("file_line") or "")[:40]
        sig = (api.get("signature") or "")[:50]
        parts.append(f"| `{name}()` | `{fl}` | `{sig}` |")
    parts.append("")
    return "\n".join(parts)


def _gen_04_constraints(data: dict) -> str:
    """04-reference-constraints.md 模板。"""
    meta = data.get("scan_meta", {})
    constraints = get_constraint_rows(data)
    topic = meta.get("scan_topic", "")

    sections = [
        "概览图",
        "约束分类",
        "约束详述",
        "冲突热力图",
    ]
    parts = [
        f"# 04 参考约束文档（{topic}）",
        "",
        f"> {len(constraints)} 条参考约束",
        "",
        _toc(sections),
        "## 概览图",
        "",
        _svg_constraint_matrix(constraints),
        "",
        "## 约束分类",
        "",
        "<!-- AI: 将约束分为架构层/数据契约/配置依赖/外部依赖 四大类 -->",
        "",
        _constraint_table(constraints),
        "## 约束详述",
        "",
        "<!-- AI: 对每条约束展开说明——规则/存在原因/违反后果/验证方法 -->",
        "",
        "## 冲突热力图",
        "",
        "<!-- AI: 生成约束×模块的影响热力图 -->",
        "",
    ]
    return "\n".join(parts)


def _gen_05_impact(data: dict) -> str:
    """05-impact-matrix.md 模板。"""
    meta = data.get("scan_meta", {})
    impacts = get_impact_rows(data)
    modules = get_module_rows(data)
    topic = meta.get("scan_topic", "")

    sections = [
        "概览图",
        "影响热力图",
        "影响传播图",
        "逐项分析",
        "验证清单",
    ]
    parts = [
        f"# 05 影响矩阵（{topic}）",
        "",
        f"> {len(impacts)} 个影响变更点",
        "",
        _toc(sections),
        "## 概览图",
        "",
        "<!-- AI: 一句话总结最关键的发现 -->",
        "",
        "## 影响热力图",
        "",
        _svg_impact_heatmap(impacts, modules),
        "",
        "## 影响传播图",
        "",
        "```mermaid",
        _mermaid_impact_propagation(impacts),
        "```",
        "",
        "## 逐项分析",
        "",
        _impact_table(impacts),
        "<!-- AI: 对每个影响项展开——风险级别/位置/直接影响/间接影响/验证点 -->",
        "",
        "## 验证清单",
        "",
        "<!-- AI: 生成变更验证清单 SVG -->",
        "",
    ]
    return "\n".join(parts)


def _gen_06_exec_brief(data: dict) -> str:
    """06-exec-brief.md 模板。"""
    meta = data.get("scan_meta", {})
    modules = get_module_rows(data)
    impacts = get_impact_rows(data)
    entries = data.get("entry_points") or []
    stats = meta.get("stats", {})
    topic = meta.get("scan_topic", "")
    total_func = stats.get("function_count", 0)
    total_mod = stats.get("module_count", 0)

    sections = [
        "概览图",
        "扫描摘要",
        "优先级矩阵",
        "模块依赖",
        "模块规模对比",
        "关键发现",
        "下一步建议",
    ]
    parts = [
        f"# 06 执行摘要（{topic}）",
        "",
        f"> {total_mod} 模块 · {total_func} 函数 · {len(entries)} 入口点",
        "",
        _toc(sections),
        "## 概览图",
        "",
        "<!-- AI: 补充概览 SVG 仪表盘 -->",
        "",
        "## 扫描摘要",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 模块数 | {total_mod} |",
        f"| 函数数 | {total_func} |",
        f"| 入口点 | {len(entries)} |",
        f"| 数据流 | {stats.get('data_flow_count', 0)} |",
        f"| 约束 | {stats.get('constraint_count', len(get_constraint_rows(data)))} |",
        "",
        "## 优先级矩阵",
        "",
        _svg_priority_matrix(impacts),
        "",
        "## 模块依赖",
        "",
        "```mermaid",
        _mermaid_task_deps(modules),
        "```",
        "",
        "## 模块规模对比",
        "",
        _svg_bar_chart(modules),
        "",
        "## 关键发现",
        "",
        "<!-- AI: 提炼 3-5 条最重要的发现 -->",
        "",
        "## 下一步建议",
        "",
        "<!-- AI: 按优先级给出改进建议表格 -->",
        "",
    ]
    return "\n".join(parts)


# ── 文档编号到生成器映射 ─────────────────────────────────

_DOC_GENERATORS = {
    "01": ("01-architecture.md", _gen_01_architecture),
    "02": ("02-dataflow.md", _gen_02_dataflow),
    "03": ("03-api-surface.md", _gen_03_api_surface),
    "04": ("04-reference-constraints.md", _gen_04_constraints),
    "05": ("05-impact-matrix.md", _gen_05_impact),
    "06": ("06-exec-brief.md", _gen_06_exec_brief),
}


# ── 子命令入口 ────────────────────────────────────────────


def cmd_generate_docs(args) -> None:
    """从 scan-data.json 代码生成 01-06 结构化文档模板。"""
    scan_data_path = Path(args.scan_data)
    data = _load_scan_data(scan_data_path)

    output_dir = Path(args.output) if args.output else scan_data_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    docs_to_gen = args.docs or list(_DOC_GENERATORS.keys())
    generated = []

    for doc_id in docs_to_gen:
        gen_info = _DOC_GENERATORS.get(doc_id)
        if not gen_info:
            print(f"[WARN] 未知文档编号: {doc_id}，跳过", file=sys.stderr)
            continue
        filename, generator = gen_info
        content = generator(data)
        out_path = output_dir / filename
        out_path.write_text(content, encoding="utf-8")
        generated.append(filename)
        print(f"  [OK] {out_path}")

    print(f"\n[OK] 文档生成完成: {len(generated)} 个文件")
    print("  提示: <!-- AI: --> 标记的注释块需要 AI 填充语义内容")
    print(f"  输出目录: {output_dir}")
