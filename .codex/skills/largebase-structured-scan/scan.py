#!/usr/bin/env python3
"""
largebase-structured-scan: 结构化代码库扫描辅助工具

用法示例:
  python .claude/skills/largebase-structured-scan/scan.py scan --mode M4 --scope . --topic refactor-core
  python .claude/skills/largebase-structured-scan/scan.py scan --mode M2 --scope src docs --topic feature-x --refs docs/api.md docs/config.md
  python .claude/skills/largebase-structured-scan/scan.py load --load docs/scan/2026-02-26-refactor-core/scan-data.json --db docs/scan/2026-02-26-refactor-core/scan.db
  python .claude/skills/largebase-structured-scan/scan.py query --query hybrid_search --type all --db docs/scan/2026-02-26-refactor-core/scan.db
  python .claude/skills/largebase-structured-scan/scan.py export-to-claude-md --db docs/scan/2026-02-26-refactor-core/scan.db --claude-md CLAUDE.md
  python .claude/skills/largebase-structured-scan/scan.py measure --scope . src --output docs/scan/measure.json
"""

import argparse
import ast
import json
import os
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def compute_sha256(file_path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    h.update(file_path.read_bytes())
    return h.hexdigest()


def is_file_changed(conn, rel_path: str, current_hash: str) -> bool:
    row = conn.execute("SELECT sha256 FROM file_hashes WHERE path = ?", (rel_path,)).fetchone()
    return row is None or row[0] != current_hash


def update_file_hash(conn, rel_path: str, sha256: str):
    conn.execute(
        "INSERT OR REPLACE INTO file_hashes(path, sha256, scanned_at) VALUES(?,?,?)",
        (rel_path, sha256, datetime.now().isoformat()),
    )


SCAN_MODES = {
    "M1": "快速架构扫描",
    "M2": "数据流扫描",
    "M3": "API 表面扫描",
    "M4": "全量深度扫描",
}

REQUIRED_BY_MODE = {
    "M1": ["00-scan-meta.json", "01-architecture.md", "06-exec-brief.md"],
    "M2": ["00-scan-meta.json", "01-architecture.md", "02-dataflow.md", "05-impact-matrix.md", "06-exec-brief.md", "scan.db"],
    "M3": ["00-scan-meta.json", "01-architecture.md", "03-api-surface.md", "05-impact-matrix.md", "06-exec-brief.md", "scan.db"],
    "M4": [
        "00-scan-meta.json",
        "01-architecture.md",
        "02-dataflow.md",
        "03-api-surface.md",
        "04-reference-constraints.md",
        "05-impact-matrix.md",
        "06-exec-brief.md",
        "scan-data.json",
        "scan.db",
    ],
}

SPECIAL_QUERY_MODES = {"impact", "callers", "risks", "module-deps"}

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".cs",
    ".php",
    ".rb",
    ".kt",
    ".swift",
    ".scala",
}

DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt"}

MEASURE_SKIP_DIR_NAMES = {"node_modules", "__pycache__", ".venv"}


def setup_stdio_encoding():
    """统一标准输出编码，降低 Windows 终端乱码概率。"""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


def get_mode_template_hint(mode: str) -> str:
    """返回当前模式建议使用的模板路径。"""
    skill_root = Path(__file__).resolve().parent
    mode_template = skill_root / "templates" / f"codex-prompt-{mode}.txt"
    if mode_template.exists():
        mode_template_text = str(mode_template).replace("\\", "/")
        return mode_template_text
    fallback_template = skill_root / "references" / "prompt-pack.md"
    fallback_template_text = str(fallback_template).replace("\\", "/")
    return f"{fallback_template_text}（查找 {mode} 段）"


def normalize_list(value) -> list[str]:
    """将字符串/列表统一转成字符串列表。"""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, str):
        if not value.strip():
            return []
        # 兼容逗号分隔字符串
        if "," in value:
            return [v.strip() for v in value.split(",") if v.strip()]
        return [value.strip()]
    return [str(value)]


def normalize_scope_paths(raw_scopes: list[str]) -> list[str]:
    """将 scope 参数统一成路径列表，支持空格和逗号两种分隔。"""
    scope_paths: list[str] = []
    for raw_item in raw_scopes:
        if raw_item is None:
            continue
        for raw_part in str(raw_item).split(","):
            scope_path = raw_part.strip()
            if scope_path:
                scope_paths.append(scope_path)
    return scope_paths


def list_to_text(value) -> str:
    """列表序列化为逗号分隔文本。"""
    return ",".join(normalize_list(value))


def parse_file_line(file_line: str) -> tuple[str, int | None]:
    """解析 'path:line' 格式。"""
    if not file_line:
        return "", None
    parts = file_line.rsplit(":", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0], int(parts[1])
    return file_line, None


def make_id(prefix: str, value: str, fallback_index: int) -> str:
    """构造稳定主键。"""
    base = value.strip().replace("\\", "/").replace(" ", "_")
    if not base:
        base = f"item_{fallback_index}"
    return f"{prefix}:{base}"


def init_db(db_path: str) -> sqlite3.Connection:
    """初始化 SQLite 数据库和索引。"""
    db_parent = Path(db_path).parent
    db_parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS scan_meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS modules (
            id                TEXT PRIMARY KEY,
            path              TEXT NOT NULL,
            name              TEXT NOT NULL,
            responsibility    TEXT,
            exported_symbols  TEXT,
            dependencies      TEXT,
            file_count        INTEGER,
            loc               INTEGER
        );
        CREATE TABLE IF NOT EXISTS functions (
            id                TEXT PRIMARY KEY,
            module_id         TEXT NOT NULL,
            name              TEXT NOT NULL,
            signature         TEXT,
            file_path         TEXT,
            line_number       INTEGER,
            called_by         TEXT,
            calls             TEXT,
            is_public         BOOLEAN
        );
        CREATE TABLE IF NOT EXISTS dataflows (
            id                TEXT PRIMARY KEY,
            name              TEXT NOT NULL,
            input_format      TEXT,
            output_format     TEXT,
            steps             TEXT,
            side_effects      TEXT,
            related_functions TEXT
        );
        CREATE TABLE IF NOT EXISTS data_structures (
            id                TEXT PRIMARY KEY,
            name              TEXT NOT NULL,
            fields            TEXT,
            used_by           TEXT,
            storage_layer     TEXT
        );
        CREATE TABLE IF NOT EXISTS constraints (
            id                TEXT PRIMARY KEY,
            source_doc        TEXT,
            constraint_type   TEXT,
            content           TEXT,
            impact_scope      TEXT,
            priority          TEXT
        );
        CREATE TABLE IF NOT EXISTS impact_items (
            id                  TEXT PRIMARY KEY,
            change_point        TEXT,
            direct_impact       TEXT,
            indirect_impact     TEXT,
            verification_points TEXT,
            risk_level          TEXT
        );
        CREATE TABLE IF NOT EXISTS reference_docs (
            id             TEXT PRIMARY KEY,
            path           TEXT NOT NULL,
            purpose        TEXT,
            key_sections   TEXT,
            conflicts_with TEXT
        );
        CREATE TABLE IF NOT EXISTS file_hashes (
            path       TEXT PRIMARY KEY,
            sha256     TEXT NOT NULL,
            scanned_at TEXT NOT NULL
        );
        """
    )
    conn.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_modules_path ON modules(path);
        CREATE INDEX IF NOT EXISTS idx_functions_module ON functions(module_id);
        CREATE INDEX IF NOT EXISTS idx_functions_name ON functions(name);
        CREATE INDEX IF NOT EXISTS idx_constraints_type ON constraints(constraint_type);
        CREATE INDEX IF NOT EXISTS idx_impact_risk ON impact_items(risk_level);
        """
    )
    conn.commit()
    return conn


def cmd_scan(args):
    """初始化扫描目录与数据库。"""
    mode = args.mode
    scope_paths = normalize_scope_paths(args.scope)
    if not scope_paths:
        print("[ERR] --scope 不能为空，至少提供一个扫描路径")
        return
    topic = args.topic.strip().replace(" ", "-")
    refs = args.refs or []

    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"docs/scan/{timestamp}-{topic}")
    output_dir.mkdir(parents=True, exist_ok=True)

    db_path = output_dir / "scan.db"
    conn = init_db(str(db_path))

    meta = {
        "scan_date": datetime.now().isoformat(),
        "scan_mode": mode,
        "scan_scope": json.dumps(scope_paths, ensure_ascii=False),
        "scan_topic": topic,
        "reference_docs": ",".join(refs),
    }
    for key, value in meta.items():
        conn.execute(
            "INSERT OR REPLACE INTO scan_meta(key, value) VALUES(?, ?)",
            (key, str(value)),
        )
    conn.commit()
    conn.close()
    template_hint = get_mode_template_hint(mode)
    missing_paths = [scope_path for scope_path in scope_paths if not Path(scope_path).exists()]

    print("[OK] 扫描初始化完成")
    print(f"  模式: {SCAN_MODES.get(mode, mode)}")
    print(f"  输出: {output_dir}")
    print(f"  数据库: {db_path}")
    if missing_paths:
        print("[WARN] 以下 scope 路径不存在，请在生成 scan-data.json 前确认：")
        for missing_path in missing_paths:
            print(f"    - {missing_path}")
    # 移除"下一步"提示，避免 CC 看到后停下来等待
    # SKILL.md 已定义连续执行规则，CC 应自动执行 Step 3


def get_module_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回模块列表。"""
    if "module_inventory" in data:
        return data.get("module_inventory", [])
    return data.get("modules", [])


def get_function_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回函数/API列表。"""
    rows = []
    rows.extend(data.get("functions", []))
    rows.extend(data.get("api_surface", []))
    return rows


def get_dataflow_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回数据流列表。"""
    if "data_flows" in data:
        return data.get("data_flows", [])
    return data.get("dataflows", [])


def get_datastructure_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回数据结构列表。"""
    return data.get("data_structures", [])


def get_constraint_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回约束列表。"""
    if "reference_constraints" in data:
        return data.get("reference_constraints", [])
    return data.get("constraints", [])


def get_impact_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回影响矩阵列表。"""
    if "impact_matrix" in data:
        return data.get("impact_matrix", [])
    return data.get("impact_items", [])


def get_reference_doc_rows(data: dict) -> list[dict]:
    """兼容新旧字段名，返回参考文档列表。"""
    return data.get("reference_docs", [])


def infer_module_id(file_path: str, module_rows: list[dict], fallback_idx: int) -> str:
    """根据文件路径推断模块 ID。"""
    if not file_path:
        return f"mod:unknown_{fallback_idx}"
    file_path_norm = file_path.replace("\\", "/")
    for idx, mod in enumerate(module_rows, start=1):
        mod_path = (mod.get("path") or "").replace("\\", "/").rstrip("/")
        mod_id = mod.get("id") or make_id("mod", mod_path or mod.get("name", ""), idx)
        if mod_path and file_path_norm.startswith(mod_path):
            return mod_id
    return make_id("mod", Path(file_path_norm).parent.as_posix(), fallback_idx)


def validate_scan_data(data: dict) -> tuple[bool, list[str]]:
    """校验 scan-data.json 结构。返回 (is_valid, error_list)。"""
    errors: list[str] = []

    # 1. 顶层 key 检查
    if "scan_meta" not in data:
        errors.append("缺少顶层字段: scan_meta")

    # 2. 至少有一种数据
    has_data = any(
        data.get(k)
        for k in ["modules", "module_inventory", "functions", "api_surface"]
    )
    if not has_data:
        errors.append("scan_meta 之外没有任何数据（modules/functions 均为空）")

    # 3. scan_meta 字段检查
    meta = data.get("scan_meta", {})
    for field in ["scan_date", "scan_mode"]:
        if field not in meta:
            errors.append(f"scan_meta 缺少必填字段: {field}")

    # 4. modules 每项检查（前 5 个）
    for i, mod in enumerate(get_module_rows(data)[:5]):
        if not mod.get("name"):
            errors.append(f"modules[{i}] 缺少 name 字段")

    # 5. functions 每项检查（前 5 个）
    for i, func in enumerate(get_function_rows(data)[:5]):
        if not func.get("name"):
            errors.append(f"functions[{i}] 缺少 name 字段")

    return len(errors) == 0, errors


def cmd_load(args):
    """将 scan-data.json 写入 SQLite。"""
    json_path = Path(args.load)
    db_path = Path(args.db)

    if not json_path.exists():
        print(f"[ERR] 文件不存在: {json_path}")
        return

    with json_path.open("r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    # schema 校验（新增）
    is_valid, errors = validate_scan_data(data)
    if not is_valid:
        print("[ERR] scan-data.json 校验失败，以下字段缺失或不符合 schema：")
        for err in errors:
            print(f"  - {err}")
        print("请修复后重新运行 load 命令。")
        sys.exit(1)

    conn = init_db(str(db_path))

    # 1) 元数据
    scan_meta = data.get("scan_meta", {})
    for key, value in scan_meta.items():
        conn.execute(
            "INSERT OR REPLACE INTO scan_meta(key, value) VALUES(?, ?)",
            (str(key), json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)),
        )

    module_rows = get_module_rows(data)
    function_rows = get_function_rows(data)
    dataflow_rows = get_dataflow_rows(data)
    datastructure_rows = get_datastructure_rows(data)
    constraint_rows = get_constraint_rows(data)
    impact_rows = get_impact_rows(data)
    reference_doc_rows = get_reference_doc_rows(data)

    # 2) modules
    for idx, mod in enumerate(module_rows, start=1):
        mod_path = mod.get("path", "")
        mod_name = mod.get("name") or Path(mod_path).name or f"module_{idx}"
        mod_id = mod.get("id") or make_id("mod", mod_path or mod_name, idx)
        conn.execute(
            """
            INSERT OR REPLACE INTO modules(
                id, path, name, responsibility, exported_symbols, dependencies, file_count, loc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                mod_id,
                mod_path,
                mod_name,
                mod.get("responsibility"),
                list_to_text(mod.get("exported_symbols") or mod.get("public_symbols")),
                list_to_text(mod.get("dependencies")),
                mod.get("file_count"),
                mod.get("loc"),
            ),
        )

    # 3) functions / api_surface
    for idx, func in enumerate(function_rows, start=1):
        func_name = func.get("name", f"func_{idx}")
        file_path = func.get("file_path", "")
        line_number = func.get("line_number")

        # 兼容 api_surface 的 file_line
        if not file_path and func.get("file_line"):
            file_path, parsed_line = parse_file_line(func.get("file_line", ""))
            line_number = line_number or parsed_line

        module_id = func.get("module_id") or infer_module_id(file_path, module_rows, idx)
        func_id = func.get("id") or make_id("func", f"{func_name}_{file_path}_{line_number}", idx)

        conn.execute(
            """
            INSERT OR REPLACE INTO functions(
                id, module_id, name, signature, file_path, line_number, called_by, calls, is_public
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                func_id,
                module_id,
                func_name,
                func.get("signature"),
                file_path,
                line_number,
                list_to_text(func.get("called_by") or func.get("callers")),
                list_to_text(func.get("calls")),
                bool(func.get("is_public", True)),
            ),
        )

    # 4) dataflows
    for idx, flow in enumerate(dataflow_rows, start=1):
        flow_name = flow.get("name", f"flow_{idx}")
        flow_id = flow.get("id") or make_id("flow", flow_name, idx)
        conn.execute(
            """
            INSERT OR REPLACE INTO dataflows(
                id, name, input_format, output_format, steps, side_effects, related_functions
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                flow_id,
                flow_name,
                flow.get("input") or flow.get("input_format"),
                flow.get("output") or flow.get("output_format"),
                list_to_text(flow.get("stages") or flow.get("steps")),
                list_to_text(flow.get("side_effects")),
                list_to_text(flow.get("related_functions")),
            ),
        )

    # 5) data structures
    for idx, ds in enumerate(datastructure_rows, start=1):
        ds_name = ds.get("name", f"ds_{idx}")
        ds_id = ds.get("id") or make_id("ds", ds_name, idx)
        conn.execute(
            """
            INSERT OR REPLACE INTO data_structures(
                id, name, fields, used_by, storage_layer
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                ds_id,
                ds_name,
                json.dumps(ds.get("fields", []), ensure_ascii=False),
                list_to_text(ds.get("used_by")),
                ds.get("storage_layer") or ds.get("source"),
            ),
        )

    # 6) constraints
    for idx, item in enumerate(constraint_rows, start=1):
        item_id = item.get("id") or make_id("cons", item.get("constraint", "") or item.get("content", ""), idx)
        conn.execute(
            """
            INSERT OR REPLACE INTO constraints(
                id, source_doc, constraint_type, content, impact_scope, priority
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                item.get("source") or item.get("source_doc"),
                item.get("constraint_type", "general"),
                item.get("constraint") or item.get("content"),
                item.get("impact") or item.get("impact_scope"),
                item.get("priority", "medium"),
            ),
        )

    # 7) impact items
    for idx, impact in enumerate(impact_rows, start=1):
        impact_id = impact.get("id") or make_id("impact", impact.get("change_point", ""), idx)
        direct_impact = impact.get("direct_impact")
        indirect_impact = impact.get("indirect_impact")
        verification_points = impact.get("verification_points") or impact.get("validation_point")
        conn.execute(
            """
            INSERT OR REPLACE INTO impact_items(
                id, change_point, direct_impact, indirect_impact, verification_points, risk_level
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                impact_id,
                impact.get("change_point"),
                list_to_text(direct_impact),
                list_to_text(indirect_impact),
                list_to_text(verification_points),
                str(impact.get("risk_level", "medium")).lower(),
            ),
        )

    # 8) reference docs
    for idx, doc in enumerate(reference_doc_rows, start=1):
        doc_path = doc.get("path", "")
        doc_id = doc.get("id") or make_id("ref", doc_path, idx)
        conn.execute(
            """
            INSERT OR REPLACE INTO reference_docs(
                id, path, purpose, key_sections, conflicts_with
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                doc_path,
                doc.get("purpose"),
                list_to_text(doc.get("key_sections")),
                list_to_text(doc.get("conflicts_with")),
            ),
        )

    # 统计信息写回 meta
    stats = {
        "module_count": len(module_rows),
        "function_count": len(function_rows),
        "dataflow_count": len(dataflow_rows),
        "data_structure_count": len(datastructure_rows),
        "constraint_count": len(constraint_rows),
        "impact_item_count": len(impact_rows),
        "reference_doc_count": len(reference_doc_rows),
    }
    for key, value in stats.items():
        conn.execute(
            "INSERT OR REPLACE INTO scan_meta(key, value) VALUES(?, ?)",
            (key, str(value)),
        )

    conn.commit()

    # 记录校验通过标记
    conn.execute(
        "INSERT OR REPLACE INTO scan_meta(key, value) VALUES('load_validated', 'true')"
    )
    conn.commit()
    conn.close()

    print("[OK] 数据加载完成")
    print(f"  模块: {stats['module_count']}")
    print(f"  函数/API: {stats['function_count']}")
    print(f"  数据流: {stats['dataflow_count']}")
    print(f"  约束: {stats['constraint_count']}")
    print(f"  影响项: {stats['impact_item_count']}")


def print_query_result(title: str, rows: list[tuple], formatter):
    """统一打印查询结果。"""
    if not rows:
        return 0
    print(f"\n[{title}] {len(rows)} 条")
    for row in rows:
        print(formatter(row))
    return len(rows)


def get_meta_value(conn: sqlite3.Connection, key: str) -> str:
    """读取 scan_meta 的单个值。"""
    row = conn.execute(
        "SELECT value FROM scan_meta WHERE key = ?",
        (key,),
    ).fetchone()
    if not row:
        return ""
    return row[0] or ""


def get_existing_tables(conn: sqlite3.Connection) -> set[str]:
    """读取数据库里当前存在的表。"""
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    return {row[0] for row in rows}


def parse_scope_text(raw_scope: str) -> str:
    """将 scope 元信息转为可读文本。"""
    if not raw_scope:
        return "未记录"
    try:
        parsed = json.loads(raw_scope)
        if isinstance(parsed, list):
            return ", ".join(str(item) for item in parsed if str(item).strip()) or "未记录"
    except json.JSONDecodeError:
        pass
    return raw_scope


def cmd_query(args):
    """查询扫描数据库。"""
    query = args.query
    query_type = args.type
    filter_text = (args.filter or "").strip()
    limit = max(1, args.limit)
    db_path = Path(args.db)

    if not db_path.exists():
        print(f"[ERR] 数据库不存在: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    try:
        if query in SPECIAL_QUERY_MODES:
            tables = get_existing_tables(conn)
            total_hits = 0

            if query == "impact":
                if not filter_text:
                    print("[ERR] --query impact 需要配合 --filter 使用")
                    return
                missing_tables = [name for name in ("functions", "impact_items") if name not in tables]
                if missing_tables:
                    print(f"[ERR] 数据库缺少表: {', '.join(missing_tables)}")
                    return

                like_filter = f"%{filter_text}%"
                rows = conn.execute(
                    """
                    SELECT name, file_path, called_by
                    FROM functions
                    WHERE file_path LIKE ?
                      AND is_public = 1
                    ORDER BY name
                    LIMIT ?
                    """,
                    (like_filter, limit),
                ).fetchall()
                total_hits += print_query_result(
                    "影响分析 / 公开函数",
                    rows,
                    lambda r: f"  - {r[0]} ({r[1]}) | 调用方: {r[2] if r[2] else '未记录'}",
                )

                rows = conn.execute(
                    """
                    SELECT change_point, direct_impact, indirect_impact, risk_level
                    FROM impact_items
                    WHERE change_point LIKE ?
                    ORDER BY
                        CASE risk_level
                            WHEN 'critical' THEN 0
                            WHEN 'high' THEN 1
                            WHEN 'medium' THEN 2
                            WHEN 'low' THEN 3
                            ELSE 4
                        END,
                        change_point
                    LIMIT ?
                    """,
                    (like_filter, limit),
                ).fetchall()
                total_hits += print_query_result(
                    "影响分析 / 影响矩阵",
                    rows,
                    lambda r: f"  - 变更点: {r[0]} | 直接影响: {r[1] if r[1] else '未填写'} | 间接影响: {r[2] if r[2] else '未填写'} | 风险: {r[3]}",
                )

            elif query == "callers":
                if not filter_text:
                    print("[ERR] --query callers 需要配合 --filter 使用")
                    return
                if "functions" not in tables:
                    print("[ERR] 数据库缺少表: functions")
                    return

                rows = conn.execute(
                    """
                    SELECT name, file_path, line_number, called_by
                    FROM functions
                    WHERE name = ?
                       OR called_by LIKE ?
                    ORDER BY name
                    LIMIT ?
                    """,
                    (filter_text, f"%{filter_text}%", limit),
                ).fetchall()
                total_hits += print_query_result(
                    "调用链",
                    rows,
                    lambda r: f"  - {r[0]} ({r[1]}:{r[2] if r[2] else '?'}) | 调用方: {r[3] if r[3] else '未记录'}",
                )

            elif query == "risks":
                if "impact_items" not in tables:
                    print("[ERR] 数据库缺少表: impact_items")
                    return

                rows = conn.execute(
                    """
                    SELECT change_point, direct_impact, risk_level, verification_points
                    FROM impact_items
                    WHERE risk_level IN ('high', 'critical')
                    ORDER BY
                        CASE risk_level WHEN 'critical' THEN 0 WHEN 'high' THEN 1 END,
                        change_point
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
                total_hits += print_query_result(
                    "高风险点",
                    rows,
                    lambda r: f"  - 变更点: {r[0]} | 直接影响: {r[1] if r[1] else '未填写'} | 风险: {r[2]} | 验证点: {r[3] if r[3] else '未填写'}",
                )

            elif query == "module-deps":
                if not filter_text:
                    print("[ERR] --query module-deps 需要配合 --filter 使用")
                    return
                if "modules" not in tables:
                    print("[ERR] 数据库缺少表: modules")
                    return

                like_filter = f"%{filter_text}%"
                rows = conn.execute(
                    """
                    SELECT name, path, dependencies, exported_symbols
                    FROM modules
                    WHERE name LIKE ?
                       OR dependencies LIKE ?
                    ORDER BY name
                    LIMIT ?
                    """,
                    (like_filter, like_filter, limit),
                ).fetchall()
                total_hits += print_query_result(
                    "模块依赖",
                    rows,
                    lambda r: f"  - {r[0]} ({r[1]}) | 依赖: {r[2] if r[2] else '无'} | 导出: {r[3] if r[3] else '无'}",
                )

            if total_hits == 0:
                target_text = filter_text or query
                print(f"[WARN] 未找到匹配 '{target_text}' 的结果")
            return

        like_text = f"%{query}%"
        total_hits = 0

        if query_type in ("all", "function"):
            rows = conn.execute(
                """
                SELECT name, signature, file_path, line_number
                FROM functions
                WHERE name LIKE ? OR signature LIKE ? OR file_path LIKE ?
                ORDER BY name
                LIMIT ?
                """,
                (like_text, like_text, like_text, limit),
            ).fetchall()
            total_hits += print_query_result(
                "函数/API",
                rows,
                lambda r: f"  - {r[0]} ({r[2]}:{r[3] if r[3] else '?'}) | {r[1] if r[1] else '无签名'}",
            )

        if query_type in ("all", "module"):
            rows = conn.execute(
                """
                SELECT name, path, responsibility, dependencies
                FROM modules
                WHERE name LIKE ? OR path LIKE ? OR responsibility LIKE ? OR dependencies LIKE ?
                ORDER BY name
                LIMIT ?
                """,
                (like_text, like_text, like_text, like_text, limit),
            ).fetchall()
            total_hits += print_query_result(
                "模块",
                rows,
                lambda r: f"  - {r[0]} ({r[1]}) | 职责: {r[2] if r[2] else '未填写'}",
            )

        if query_type in ("all", "constraint"):
            rows = conn.execute(
                """
                SELECT source_doc, content, impact_scope, priority
                FROM constraints
                WHERE source_doc LIKE ? OR content LIKE ? OR impact_scope LIKE ?
                ORDER BY priority DESC
                LIMIT ?
                """,
                (like_text, like_text, like_text, limit),
            ).fetchall()
            total_hits += print_query_result(
                "约束",
                rows,
                lambda r: f"  - 来源: {r[0]} | 约束: {r[1]} | 影响: {r[2] if r[2] else '未填写'} | 优先级: {r[3]}",
            )

        if query_type in ("all", "impact"):
            rows = conn.execute(
                """
                SELECT change_point, direct_impact, indirect_impact, verification_points, risk_level
                FROM impact_items
                WHERE change_point LIKE ? OR direct_impact LIKE ? OR indirect_impact LIKE ? OR verification_points LIKE ?
                ORDER BY risk_level DESC
                LIMIT ?
                """,
                (like_text, like_text, like_text, like_text, limit),
            ).fetchall()
            total_hits += print_query_result(
                "影响矩阵",
                rows,
                lambda r: f"  - 变更点: {r[0]} | 风险: {r[4]} | 验证: {r[3] if r[3] else '未填写'}",
            )

        if query_type in ("all", "dataflow"):
            rows = conn.execute(
                """
                SELECT name, input_format, output_format, side_effects
                FROM dataflows
                WHERE name LIKE ? OR input_format LIKE ? OR output_format LIKE ? OR steps LIKE ?
                ORDER BY name
                LIMIT ?
                """,
                (like_text, like_text, like_text, like_text, limit),
            ).fetchall()
            total_hits += print_query_result(
                "数据流",
                rows,
                lambda r: f"  - {r[0]} | 输入: {r[1] if r[1] else '未填写'} | 输出: {r[2] if r[2] else '未填写'}",
            )

        if total_hits == 0:
            print(f"[WARN] 未找到匹配 '{query}' 的结果")
    finally:
        conn.close()


def should_skip_measure_dir(path: Path) -> bool:
    """判断目录是否需要在 measure 子命令中跳过。"""
    dir_name = path.name
    if dir_name.startswith("."):
        return True
    if dir_name in MEASURE_SKIP_DIR_NAMES:
        return True

    lowered_parts = [part.lower() for part in path.parts if part]
    for index in range(len(lowered_parts) - 1):
        if lowered_parts[index] == "docs" and lowered_parts[index + 1] == "scan":
            return True
    return False


def count_code_lines(file_path: Path) -> int:
    """统计代码文件行数，读取失败时返回 0。"""
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as file_obj:
            return sum(1 for _ in file_obj)
    except OSError:
        return 0


def init_scope_bucket() -> dict[str, int]:
    """初始化按 scope 聚合的统计桶。"""
    return {
        "files": 0,
        "code_files": 0,
        "doc_files": 0,
        "loc": 0,
        "bytes": 0,
    }


def update_measure_stats(
    file_path: Path,
    result: dict,
    scope_bucket: dict[str, int],
):
    """将单个文件纳入 measure 统计结果。"""
    try:
        file_bytes = file_path.stat().st_size
    except OSError:
        return

    extension = file_path.suffix.lower() or "<no_ext>"
    is_code_file = extension in CODE_EXTENSIONS
    is_doc_file = extension in DOC_EXTENSIONS
    file_loc = count_code_lines(file_path) if is_code_file else 0

    result["total_files"] += 1
    result["total_bytes"] += file_bytes
    if is_code_file:
        result["code_files"] += 1
        result["total_loc"] += file_loc
    if is_doc_file:
        result["doc_files"] += 1

    scope_bucket["files"] += 1
    scope_bucket["bytes"] += file_bytes
    if is_code_file:
        scope_bucket["code_files"] += 1
        scope_bucket["loc"] += file_loc
    if is_doc_file:
        scope_bucket["doc_files"] += 1

    extension_bucket = result["by_extension"].setdefault(
        extension,
        {"files": 0, "loc": 0, "bytes": 0},
    )
    extension_bucket["files"] += 1
    extension_bucket["loc"] += file_loc
    extension_bucket["bytes"] += file_bytes


def walk_scope_and_measure(scope_path: Path, result: dict, scope_bucket: dict[str, int]):
    """递归遍历单个 scope 路径并统计。"""
    if scope_path.is_file():
        update_measure_stats(scope_path, result, scope_bucket)
        return

    for root, dir_names, file_names in os.walk(scope_path):
        current_root = Path(root)
        dir_names[:] = [
            dir_name
            for dir_name in dir_names
            if not should_skip_measure_dir(current_root / dir_name)
        ]

        for file_name in file_names:
            file_path = current_root / file_name
            if file_path.is_file():
                update_measure_stats(file_path, result, scope_bucket)


def cmd_measure(args):
    """统计 scope 路径内文件规模并输出 JSON。"""
    scope_paths = normalize_scope_paths(args.scope)
    if not scope_paths:
        print("[ERR] --scope 不能为空，至少提供一个扫描路径")
        return

    result = {
        "measured_at": datetime.now().isoformat(),
        "total_files": 0,
        "code_files": 0,
        "doc_files": 0,
        "total_loc": 0,
        "total_bytes": 0,
        "by_extension": {},
        "by_scope": {},
    }

    for raw_scope in scope_paths:
        scope_path = Path(raw_scope)
        scope_key = str(scope_path)
        scope_bucket = init_scope_bucket()
        result["by_scope"][scope_key] = scope_bucket

        if not scope_path.exists():
            print(f"[WARN] scope 路径不存在，已跳过: {scope_path}", file=sys.stderr)
            continue
        if scope_path.is_dir() and should_skip_measure_dir(scope_path):
            print(f"[WARN] scope 路径命中跳过规则，已跳过: {scope_path}", file=sys.stderr)
            continue

        walk_scope_and_measure(scope_path, result, scope_bucket)

    result["estimated_tokens"] = result["total_bytes"] // 4
    result["by_extension"] = dict(sorted(result["by_extension"].items(), key=lambda item: item[0]))

    output_text = json.dumps(result, ensure_ascii=False, indent=2)
    output_path = args.output
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(f"{output_text}\n", encoding="utf-8")
        print(f"[OK] 统计结果已写入: {output_file}", file=sys.stderr)
    else:
        print(output_text)

    print("[OK] 规模统计完成", file=sys.stderr)
    print(f"  总文件数: {result['total_files']}", file=sys.stderr)
    print(f"  代码文件数: {result['code_files']}", file=sys.stderr)
    print(f"  总 LOC: {result['total_loc']}", file=sys.stderr)
    print(f"  总字节数: {result['total_bytes']}", file=sys.stderr)
    print(f"  估算 Token 数: {result['estimated_tokens']}", file=sys.stderr)



# ============================================================
# extract 子命令：本地代码结构提取（零 AI token 消耗）
# ============================================================

EXTRACT_SKIP_DIRS = {
    "node_modules", "__pycache__", ".venv", ".git", ".hg",
    ".svn", "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
    "docs/scan", ".claude",
}


def _get_decorator_name(node: ast.expr) -> str:
    """从装饰器 AST 节点提取可读名称。"""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _get_decorator_name(node.value) if isinstance(node.value, (ast.Name, ast.Attribute)) else ""
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return _get_decorator_name(node.func)
    return ast.dump(node)[:60]


def _get_docstring(node: ast.AST) -> str:
    """提取节点的 docstring（前 100 字符）。"""
    ds = ast.get_docstring(node)
    if ds:
        return ds[:100]
    return ""


def _extract_python(file_path: Path) -> dict:
    """用 ast.walk() 提取 Python 文件的完整结构信息（含类方法、异步、装饰器、常量、docstring）。"""
    result = {
        "imports": [],
        "functions": [],
        "classes": [],
        "constants": [],
        "is_entry": False,
        "loc": 0,
    }
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, ValueError):
        return result

    result["loc"] = source.count("\n") + 1

    # 附加 parent 引用，用于判断函数所属类
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child._parent = node  # type: ignore[attr-defined]

    def _get_docstring(node: ast.AST) -> str:
        """提取节点 docstring 的前 100 字符。"""
        ds = ast.get_docstring(node)
        return (ds[:100] + "...") if ds and len(ds) > 100 else (ds or "")

    def _get_decorator_name(dec: ast.expr) -> str:
        """提取装饰器名称（简化表示）。"""
        if isinstance(dec, ast.Name):
            return dec.id
        if isinstance(dec, ast.Attribute):
            return dec.attr
        if isinstance(dec, ast.Call):
            return _get_decorator_name(dec.func)
        return ast.dump(dec)[:60]

    def _get_bases_str(b: ast.expr) -> str:
        """提取基类名称。"""
        if isinstance(b, ast.Name):
            return b.id
        if isinstance(b, ast.Attribute):
            return b.attr
        return ast.dump(b)[:60]

    # 记录已作为类方法提取的函数节点 id，避免在顶层重复提取
    method_node_ids: set[int] = set()

    # 第一遍：提取类（及类内方法）
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(item.name)
                    method_node_ids.add(id(item))

                    # 类方法也加入 functions 列表
                    args_list = [a.arg for a in item.args.args if a.arg != "self" and a.arg != "cls"]
                    decorators = [_get_decorator_name(d) for d in item.decorator_list][:3]
                    result["functions"].append({
                        "name": item.name,
                        "line": item.lineno,
                        "args": args_list,
                        "is_public": not item.name.startswith("_"),
                        "is_async": isinstance(item, ast.AsyncFunctionDef),
                        "decorators": decorators,
                        "class_name": node.name,
                        "docstring": _get_docstring(item),
                    })

            bases = [_get_bases_str(b) for b in node.bases][:5]
            result["classes"].append({
                "name": node.name,
                "line": node.lineno,
                "methods": methods,
                "bases": bases,
                "docstring": _get_docstring(node),
            })

    # 第二遍：提取顶层函数、导入、常量、入口点
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 跳过已作为类方法提取的
            if id(node) in method_node_ids:
                continue
            # 跳过非顶层（嵌套在函数内的）
            parent = getattr(node, "_parent", None)
            if parent is not None and not isinstance(parent, ast.Module):
                continue

            args_list = [a.arg for a in node.args.args]
            decorators = [_get_decorator_name(d) for d in node.decorator_list][:3]
            result["functions"].append({
                "name": node.name,
                "line": node.lineno,
                "args": args_list,
                "is_public": not node.name.startswith("_"),
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "decorators": decorators,
                "class_name": None,
                "docstring": _get_docstring(node),
            })

        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module:
                result["imports"].append(module)

        elif isinstance(node, ast.If):
            # 检测 if __name__ == "__main__" 入口
            try:
                if (isinstance(node.test, ast.Compare)
                        and isinstance(node.test.left, ast.Name)
                        and node.test.left.id == "__name__"):
                    result["is_entry"] = True
            except AttributeError:
                pass

        elif isinstance(node, ast.Assign):
            # 顶层常量：全大写赋值
            parent = getattr(node, "_parent", None)
            if isinstance(parent, ast.Module):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper() and "_" in target.id:
                        result["constants"].append(target.id)

    result["imports"] = sorted(set(result["imports"]))
    result["constants"] = sorted(set(result["constants"]))
    return result


# tree-sitter 可选依赖
try:
    import tree_sitter_javascript as _tsjs
    import tree_sitter_typescript as _tsts
    from tree_sitter import Language, Parser as TSParser
    _HAS_TREE_SITTER = True
except ImportError:
    _HAS_TREE_SITTER = False

# JS/TS import/export 正则
_RE_JS_IMPORT = re.compile(
    r"""(?:import\s+(?:(?:\{[^}]*\}|[\w*]+)\s+from\s+)?['"]([^'"]+)['"]"""
    r"""|require\s*\(\s*['"]([^'"]+)['"]\s*\))""",
    re.MULTILINE,
)
_RE_JS_EXPORT_FUNC = re.compile(
    r"""export\s+(?:default\s+)?(?:async\s+)?function\s+(\w+)""",
    re.MULTILINE,
)
_RE_JS_EXPORT_CLASS = re.compile(
    r"""export\s+(?:default\s+)?class\s+(\w+)""",
    re.MULTILINE,
)
_RE_JS_FUNC_DEF = re.compile(
    r"""(?:^|\n)\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)""",
    re.MULTILINE,
)
# 增强：箭头函数
_RE_ARROW_FUNC = re.compile(
    r"""export\s+(?:const|let)\s+(\w+)\s*=\s*(?:async\s*)?\(""",
    re.MULTILINE,
)
# 增强：TypeScript interface
_RE_TS_INTERFACE = re.compile(
    r"""^(?:export\s+)?interface\s+(\w+)""",
    re.MULTILINE,
)
# 增强：TypeScript type alias
_RE_TS_TYPE = re.compile(
    r"""^(?:export\s+)?type\s+(\w+)\s*=""",
    re.MULTILINE,
)


def _extract_js_ts_regex(file_path: Path) -> dict:
    """用增强正则提取 JS/TS 文件结构信息（tree-sitter 不可用时的降级方案）。"""
    result = {
        "imports": [],
        "functions": [],
        "classes": [],
        "interfaces": [],
        "constants": [],
        "is_entry": False,
    }
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return result

    def _line_at(pos: int) -> int:
        return source[:pos].count("\n") + 1

    captured_names: set[str] = set()

    # imports
    for m in _RE_JS_IMPORT.finditer(source):
        imp = m.group(1) or m.group(2)
        if imp:
            result["imports"].append(imp)

    # exported functions
    for m in _RE_JS_EXPORT_FUNC.finditer(source):
        name = m.group(1)
        captured_names.add(name)
        result["functions"].append({
            "name": name,
            "line": _line_at(m.start()),
            "args": [],
            "is_public": True,
            "is_async": False,
            "decorators": [],
            "class_name": None,
            "docstring": "",
        })

    # all top-level function definitions
    for m in _RE_JS_FUNC_DEF.finditer(source):
        name = m.group(1)
        if name not in captured_names:
            args_text = m.group(2).strip()
            args = [a.strip().split(":")[0].strip() for a in args_text.split(",") if a.strip()] if args_text else []
            captured_names.add(name)
            result["functions"].append({
                "name": name,
                "line": _line_at(m.start()),
                "args": args,
                "is_public": True,
                "is_async": "async" in source[max(0, m.start() - 10):m.start()],
                "decorators": [],
                "class_name": None,
                "docstring": "",
            })

    # 箭头函数：export const fn = (...) =>
    for m in _RE_ARROW_FUNC.finditer(source):
        name = m.group(1)
        if name not in captured_names:
            captured_names.add(name)
            result["functions"].append({
                "name": name,
                "line": _line_at(m.start()),
                "args": [],
                "is_public": True,
                "is_async": "async" in m.group(0),
                "decorators": [],
                "class_name": None,
                "docstring": "",
            })

    # classes
    for m in _RE_JS_EXPORT_CLASS.finditer(source):
        result["classes"].append({
            "name": m.group(1),
            "line": _line_at(m.start()),
            "methods": [],
            "bases": [],
        })

    # TypeScript interface
    for m in _RE_TS_INTERFACE.finditer(source):
        result["interfaces"].append({"name": m.group(1), "line": _line_at(m.start())})

    # TypeScript type alias
    for m in _RE_TS_TYPE.finditer(source):
        result["constants"].append(m.group(1))

    result["imports"] = sorted(set(result["imports"]))
    return result


def _extract_js_ts_treesitter(file_path: Path) -> dict:
    """用 tree-sitter 精确提取 JS/TS 文件结构信息。"""
    result = {
        "imports": [],
        "functions": [],
        "classes": [],
        "interfaces": [],
        "constants": [],
        "is_entry": False,
    }
    try:
        source_bytes = file_path.read_bytes()
    except OSError:
        return result

    ext = file_path.suffix.lower()
    try:
        if ext in (".ts", ".tsx"):
            language = Language(_tsts.language_typescript())
        else:
            language = Language(_tsjs.language_javascript())
        parser = TSParser(language)
        tree = parser.parse(source_bytes)
    except Exception:
        return _extract_js_ts_regex(file_path)

    def _node_text(node) -> str:
        return source_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="replace")

    def _walk(node, depth=0):
        if depth > 20:
            return
        t = node.type

        if t == "import_statement":
            for child in node.children:
                if child.type == "string":
                    text = _node_text(child).strip("'\"")
                    if text:
                        result["imports"].append(text)
        elif t == "function_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                result["functions"].append({
                    "name": _node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "args": [],
                    "is_public": True,
                    "is_async": False,
                    "decorators": [],
                    "class_name": None,
                    "docstring": "",
                })
        elif t == "lexical_declaration":
            for child in node.children:
                if child.type == "variable_declarator":
                    name_node = child.child_by_field_name("name")
                    value_node = child.child_by_field_name("value")
                    if name_node and value_node and value_node.type == "arrow_function":
                        result["functions"].append({
                            "name": _node_text(name_node),
                            "line": node.start_point[0] + 1,
                            "args": [],
                            "is_public": True,
                            "is_async": False,
                            "decorators": [],
                            "class_name": None,
                            "docstring": "",
                        })
        elif t == "class_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                methods = []
                for child in node.children:
                    if child.type == "class_body":
                        for member in child.children:
                            if member.type == "method_definition":
                                mname = member.child_by_field_name("name")
                                if mname:
                                    methods.append(_node_text(mname))
                result["classes"].append({
                    "name": _node_text(name_node),
                    "line": node.start_point[0] + 1,
                    "methods": methods,
                    "bases": [],
                })
        elif t == "interface_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                result["interfaces"].append({
                    "name": _node_text(name_node),
                    "line": node.start_point[0] + 1,
                })
        elif t == "type_alias_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                result["constants"].append(_node_text(name_node))

        for child in node.children:
            _walk(child, depth + 1)

    _walk(tree.root_node)
    result["imports"] = sorted(set(result["imports"]))
    return result


def _extract_js_ts(file_path: Path) -> dict:
    """提取 JS/TS 文件结构信息。优先 tree-sitter，不可用时降级为增强正则。"""
    if _HAS_TREE_SITTER:
        return _extract_js_ts_treesitter(file_path)
    return _extract_js_ts_regex(file_path)


def _extract_file(file_path: Path) -> dict | None:
    """分派到对应语言的提取器（返回 None 则跳过）。"""
    ext = file_path.suffix.lower()
    if ext == ".py":
        return _extract_python(file_path)
    elif ext in (".js", ".ts", ".tsx", ".jsx", ".mjs"):
        return _extract_js_ts(file_path)
    return None


# MD 标题正则
_RE_MD_HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
# MD 代码块正则（捕获语言+内容）
_RE_MD_CODE_BLOCK = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
# MD 表格行（含 | 的行）
_RE_MD_TABLE_ROW = re.compile(r"^\|(.+)\|$", re.MULTILINE)


def _extract_markdown(file_path: Path) -> dict:
    """提取 Markdown 文档的结构信息：标题大纲 + 代码块 + 首段摘要。"""
    result = {
        "headings": [],       # [{level, text, line}]
        "code_blocks": [],    # [{lang, preview, line}]
        "has_tables": False,
        "summary": "",        # 文档首段文字（≤200字）
        "char_count": 0,
    }
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return result

    result["char_count"] = len(source)

    # 标题
    for m in _RE_MD_HEADING.finditer(source):
        result["headings"].append({
            "level": len(m.group(1)),
            "text": m.group(2).strip(),
            "line": source[:m.start()].count("\n") + 1,
        })

    # 代码块（取前 8 个，每个预览前 3 行）
    for m in _RE_MD_CODE_BLOCK.finditer(source):
        lang = m.group(1).strip() or "text"
        content_lines = m.group(2).splitlines()
        preview = "\n".join(content_lines[:3])
        if len(content_lines) > 3:
            preview += f"\n... ({len(content_lines)} 行)"
        result["code_blocks"].append({
            "lang": lang,
            "preview": preview[:200],
            "line": source[:m.start()].count("\n") + 1,
        })
        if len(result["code_blocks"]) >= 8:
            break

    # 是否包含表格
    result["has_tables"] = bool(_RE_MD_TABLE_ROW.search(source))

    # 首段摘要：跳过 H1 标题和空行，取第一段正文
    lines = source.splitlines()
    para_lines = []
    in_para = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("---") or stripped.startswith("```"):
            if in_para:
                break
            continue
        if stripped:
            para_lines.append(stripped)
            in_para = True
        elif in_para:
            break
    summary_raw = " ".join(para_lines)
    result["summary"] = summary_raw[:200] + ("..." if len(summary_raw) > 200 else "")

    return result


def _should_skip_extract_dir(dir_path: Path) -> bool:
    """判断目录是否应在 extract 中跳过。"""
    name = dir_path.name
    if name.startswith("."):
        return True
    # 检查完整路径中的片段
    parts_lower = {p.lower() for p in dir_path.parts}
    return bool(parts_lower & EXTRACT_SKIP_DIRS)


def _aggregate_modules(file_results: dict[str, dict], scope_paths: list[str]) -> list[dict]:
    """将文件级结果聚合为模块级信息。每个一级子目录 = 一个模块。"""
    modules: dict[str, dict] = {}

    for rel_path, info in file_results.items():
        # 确定模块名：取 scope 下的第一级目录
        parts = Path(rel_path).parts
        if len(parts) >= 2:
            mod_name = parts[0]
        else:
            mod_name = "(root)"

        if mod_name not in modules:
            modules[mod_name] = {
                "name": mod_name,
                "path": mod_name if mod_name != "(root)" else ".",
                "files": [],
                "all_imports": set(),
                "all_functions": [],
                "all_classes": [],
                "has_entry": False,
                "file_count": 0,
                "loc": 0,
            }

        mod = modules[mod_name]
        mod["files"].append(rel_path)
        mod["file_count"] += 1
        if info.get("loc"):
            mod["loc"] += info["loc"]
        if info.get("is_entry"):
            mod["has_entry"] = True

        for imp in info.get("imports", []):
            mod["all_imports"].add(imp)

        for func in info.get("functions", []):
            func_copy = dict(func)
            func_copy["file_path"] = rel_path
            mod["all_functions"].append(func_copy)

        for cls in info.get("classes", []):
            cls_copy = dict(cls)
            cls_copy["file_path"] = rel_path
            mod["all_classes"].append(cls_copy)

    # 转换 set → sorted list
    for mod in modules.values():
        mod["all_imports"] = sorted(mod["all_imports"])

    return list(modules.values())


def _generate_codebase_map(modules: list[dict], scope_paths: list[str], topic: str) -> str:
    """生成 CODEBASE_MAP.md。"""
    lines = [
        f"# Codebase Map: {topic}",
        "",
        f"> Generated at: {datetime.now().isoformat(timespec='minutes')}",
        f"> Scope: {', '.join(scope_paths)}",
        "",
        "## 模块概览",
        "",
        "| 模块 | 文件数 | LOC | 入口点 | 公开函数 | 内部依赖 |",
        "|------|--------|-----|--------|----------|----------|",
    ]

    for mod in sorted(modules, key=lambda m: m["name"]):
        pub_funcs = sum(1 for f in mod["all_functions"] if f.get("is_public"))
        # 内部依赖 = imports 中匹配其他模块名的
        mod_names = {m["name"] for m in modules}
        internal_deps = sorted({
            imp.split(".")[0] for imp in mod["all_imports"]
            if imp.split(".")[0] in mod_names and imp.split(".")[0] != mod["name"]
        })
        entry_mark = "✓" if mod["has_entry"] else ""
        deps_text = ", ".join(internal_deps[:5]) or "-"
        lines.append(
            f"| `{mod['name']}` | {mod['file_count']} | {mod['loc']} "
            f"| {entry_mark} | {pub_funcs} | {deps_text} |"
        )

    lines.append("")

    # 每个模块的详细信息
    for mod in sorted(modules, key=lambda m: m["name"]):
        lines.append(f"## {mod['name']}")
        lines.append("")
        lines.append(f"路径: `{mod['path']}`")
        lines.append("")

        # 入口点
        if mod["has_entry"]:
            lines.append("**入口点**: 包含 `__main__` 或默认导出")
            lines.append("")

        # 公开函数
        pub_funcs = [f for f in mod["all_functions"] if f.get("is_public")]
        if pub_funcs:
            lines.append("### 公开函数")
            lines.append("")
            for func in pub_funcs[:20]:
                args_text = ", ".join(func.get("args", [])[:5])
                loc = f"{func.get('file_path', '?')}:{func.get('line', '?')}"
                lines.append(f"- `{func['name']}({args_text})` — {loc}")
            if len(pub_funcs) > 20:
                lines.append(f"- ... 共 {len(pub_funcs)} 个公开函数")
            lines.append("")

        # 类
        if mod["all_classes"]:
            lines.append("### 类定义")
            lines.append("")
            for cls in mod["all_classes"][:15]:
                methods_preview = ", ".join(cls.get("methods", [])[:5])
                loc = f"{cls.get('file_path', '?')}:{cls.get('line', '?')}"
                lines.append(f"- `{cls['name']}` [{methods_preview}] — {loc}")
            if len(mod["all_classes"]) > 15:
                lines.append(f"- ... 共 {len(mod['all_classes'])} 个类")
            lines.append("")

        # 依赖
        if mod["all_imports"]:
            lines.append("### 依赖")
            lines.append("")
            # 分内部和外部
            mod_names = {m["name"] for m in modules}
            internal = sorted({i for i in mod["all_imports"] if i.split(".")[0] in mod_names})
            external = sorted({i for i in mod["all_imports"] if i.split(".")[0] not in mod_names})
            if internal:
                lines.append(f"内部: {', '.join(internal[:10])}")
            if external:
                lines.append(f"外部: {', '.join(external[:15])}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _build_extract_data(
    modules: list[dict],
    scope_paths: list[str],
    topic: str,
    file_results: dict[str, dict],
) -> dict:
    """构建兼容 scan-data.json 格式的 extract-data.json。"""
    # modules → scan-data 的 modules 格式
    sd_modules = []
    for mod in modules:
        mod_names = {m["name"] for m in modules}
        internal_deps = sorted({
            imp.split(".")[0] for imp in mod["all_imports"]
            if imp.split(".")[0] in mod_names and imp.split(".")[0] != mod["name"]
        })
        sd_modules.append({
            "name": mod["name"],
            "path": mod["path"],
            "responsibility": f"包含 {mod['file_count']} 个文件，{len(mod['all_functions'])} 个函数",
            "exported_symbols": [
                f["name"] for f in mod["all_functions"] if f.get("is_public")
            ][:20],
            "dependencies": internal_deps,
            "file_count": mod["file_count"],
            "loc": mod["loc"],
        })

    # functions → scan-data 的 functions 格式
    sd_functions = []
    for mod in modules:
        mod_id = f"mod:{mod['name']}"
        for func in mod["all_functions"]:
            sd_functions.append({
                "name": func["name"],
                "module_id": mod_id,
                "signature": f"{func['name']}({', '.join(func.get('args', []))})",
                "file_path": func.get("file_path", ""),
                "line_number": func.get("line"),
                "is_public": func.get("is_public", True),
            })

    return {
        "scan_meta": {
            "scan_date": datetime.now().isoformat(),
            "scan_mode": "extract",
            "scan_scope": scope_paths,
            "scan_topic": topic,
            "extraction_method": "local_ast_regex",
            "ai_tokens_used": 0,
        },
        "modules": sd_modules,
        "functions": sd_functions,
        "data_structures": [],
        "data_flows": [],
        "constraints": [],
        "impact_items": [],
        "reference_docs": [],
    }


def _load_extract_cache(cache_path: Path) -> tuple[dict[str, dict], dict[str, dict]]:
    """读取 extract 缓存，增量模式下复用未变更文件的旧结果。"""
    if not cache_path.exists():
        return {}, {}

    try:
        cache_data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}, {}

    file_results = cache_data.get("file_results")
    doc_results = cache_data.get("doc_results")
    return (
        file_results if isinstance(file_results, dict) else {},
        doc_results if isinstance(doc_results, dict) else {},
    )


def _save_extract_cache(
    cache_path: Path,
    scope_paths: list[str],
    topic: str,
    file_results: dict[str, dict],
    doc_results: dict[str, dict],
):
    """保存 extract 缓存，供下次增量扫描复用。"""
    cache_data = {
        "cached_at": datetime.now().isoformat(),
        "scan_scope": scope_paths,
        "scan_topic": topic,
        "file_results": file_results,
        "doc_results": doc_results,
    }
    cache_path.write_text(
        json.dumps(cache_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _generate_docs_index(doc_results: dict[str, dict], scope_paths: list[str], topic: str) -> str:
    """生成 docs-index.md：MD 文档标题大纲导航。"""
    lines = [
        f"# Docs Index: {topic}",
        "",
        f"> Generated at: {datetime.now().isoformat(timespec='minutes')}",
        f"> Scope: {', '.join(scope_paths)}",
        f"> 文档数: {len(doc_results)}",
        "",
        "## 文档列表",
        "",
        "| 文档 | 字数 | 含代码块 | 含表格 | 摘要 |",
        "|------|------|----------|--------|------|",
    ]

    for rel_path, info in sorted(doc_results.items()):
        fname = Path(rel_path).name
        char_k = f"{info.get('char_count', 0) // 1000}K" if info.get("char_count", 0) >= 1000 else str(info.get("char_count", 0))
        has_code = "✓" if info.get("code_blocks") else ""
        has_table = "✓" if info.get("has_tables") else ""
        summary = info.get("summary", "")[:60].replace("|", "｜")
        if len(info.get("summary", "")) > 60:
            summary += "..."
        lines.append(f"| `{fname}` | {char_k} | {has_code} | {has_table} | {summary} |")

    lines.append("")

    # 每篇文档的详细大纲
    for rel_path, info in sorted(doc_results.items()):
        fname = Path(rel_path).name
        lines.append(f"## {fname}")
        lines.append("")
        lines.append(f"路径: `{rel_path}`")
        if info.get("summary"):
            lines.append(f"> {info['summary']}")
        lines.append("")

        headings = info.get("headings", [])
        if headings:
            lines.append("### 标题大纲")
            lines.append("")
            for h in headings[:30]:
                indent = "  " * (h["level"] - 1)
                lines.append(f"{indent}- {h['text']} (L{h['line']})")
            if len(headings) > 30:
                lines.append(f"  ... 共 {len(headings)} 个标题")
            lines.append("")

        code_blocks = info.get("code_blocks", [])
        if code_blocks:
            lines.append("### 代码块")
            lines.append("")
            for cb in code_blocks:
                lines.append(f"- `{cb['lang']}` (L{cb['line']})")
                if cb.get("preview"):
                    preview_first_line = cb["preview"].splitlines()[0]
                    lines.append(f"  ```{preview_first_line[:80]}```")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def cmd_extract(args):
    """本地提取代码结构 + 文档索引，零 AI token 消耗。"""
    scope_paths = normalize_scope_paths(args.scope)
    if not scope_paths:
        print("[ERR] --scope 不能为空")
        return

    topic = args.topic.strip().replace(" ", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(args.output) if args.output else Path(f"docs/scan/{timestamp}-{topic}")
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(args.db) if args.db else output_dir / "scan.db"
    cache_path = output_dir / "_extract-cache.json"
    cached_file_results, cached_doc_results = _load_extract_cache(cache_path)
    hash_conn = init_db(str(db_path))

    file_results: dict[str, dict] = {}   # 代码文件
    doc_results: dict[str, dict] = {}    # MD 文档
    total_files = 0
    extracted_files = 0
    extracted_docs = 0
    skipped_files = 0

    def process_extract_target(file_path: Path):
        nonlocal total_files, extracted_files, extracted_docs, skipped_files

        ext = file_path.suffix.lower()
        total_files += 1
        if ext not in CODE_EXTENSIONS and ext not in DOC_EXTENSIONS:
            return

        rel_path = str(file_path).replace("\\", "/")
        current_hash = ""
        try:
            current_hash = compute_sha256(file_path)
        except OSError as exc:
            print(f"[WARN] 读取失败 {file_path}: {exc}", file=sys.stderr)
            return

        cache_bucket = cached_file_results if ext in CODE_EXTENSIONS else cached_doc_results
        if args.incremental and not is_file_changed(hash_conn, rel_path, current_hash):
            cached_info = cache_bucket.get(rel_path)
            if cached_info is not None:
                if ext in CODE_EXTENSIONS:
                    file_results[rel_path] = cached_info
                else:
                    doc_results[rel_path] = cached_info
                skipped_files += 1
                return

        if ext in CODE_EXTENSIONS:
            info = _extract_file(file_path)
            if info is None:
                return
            info["loc"] = count_code_lines(file_path)
            file_results[rel_path] = info
            extracted_files += 1
        else:
            doc_results[rel_path] = _extract_markdown(file_path)
            extracted_docs += 1

        update_file_hash(hash_conn, rel_path, current_hash)

    try:
        for raw_scope in scope_paths:
            scope_path = Path(raw_scope)
            if not scope_path.exists():
                print(f"[WARN] scope 路径不存在: {scope_path}", file=sys.stderr)
                continue

            if scope_path.is_file():
                process_extract_target(scope_path)
                continue

            for root, dir_names, file_names in os.walk(scope_path):
                current_root = Path(root)
                dir_names[:] = [
                    d for d in dir_names
                    if not _should_skip_extract_dir(current_root / d)
                ]

                for fname in file_names:
                    process_extract_target(current_root / fname)

        if not file_results and not doc_results:
            print("[WARN] 未找到可提取的代码文件或文档")
            return

        # ── 代码部分 ──────────────────────────────────────
        modules = _aggregate_modules(file_results, scope_paths) if file_results else []

        extract_data = _build_extract_data(modules, scope_paths, topic, file_results)
        json_path = output_dir / "extract-data.json"
        json_path.write_text(
            json.dumps(extract_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        map_text = _generate_codebase_map(modules, scope_paths, topic)
        map_path = output_dir / "CODEBASE_MAP.md"
        map_path.write_text(map_text, encoding="utf-8")

        docs_map = Path("docs/CODEBASE_MAP.md")
        docs_map.parent.mkdir(parents=True, exist_ok=True)
        docs_map.write_text(map_text, encoding="utf-8")

        # ── 文档部分 ──────────────────────────────────────
        docs_index_path = None
        if doc_results:
            docs_index_text = _generate_docs_index(doc_results, scope_paths, topic)
            docs_index_path = output_dir / "docs-index.md"
            docs_index_path.write_text(docs_index_text, encoding="utf-8")

        _save_extract_cache(cache_path, scope_paths, topic, file_results, doc_results)
        hash_conn.commit()

        # ── 汇总输出 ──────────────────────────────────────
        print("[OK] 本地结构提取完成（零 AI token）")
        print(f"  扫描文件总数: {total_files}")
        if args.incremental:
            print(f"  跳过 {skipped_files} 个未变更文件")
        if file_results:
            print(f"  代码文件提取: {extracted_files} 个")
            print(f"    模块数: {len(modules)}")
            print(f"    函数数: {sum(len(m['all_functions']) for m in modules)}")
            print(f"    类数:   {sum(len(m['all_classes']) for m in modules)}")
            print(f"  产物: {json_path}")
            print(f"  地图: {map_path}")
        if doc_results:
            total_headings = sum(len(d.get("headings", [])) for d in doc_results.values())
            total_code_blocks = sum(len(d.get("code_blocks", [])) for d in doc_results.values())
            print(f"  文档提取: {extracted_docs} 篇")
            print(f"    标题数: {total_headings}")
            print(f"    代码块: {total_code_blocks}")
            print(f"  文档索引: {docs_index_path}")
        print(f"  哈希库: {db_path}")
    finally:
        hash_conn.close()


def cmd_verify(args):
    """校验扫描目录的产物完整性。"""
    output_dir = Path(args.dir)
    mode = args.mode

    if not output_dir.exists() or not output_dir.is_dir():
        print(f"[ERR] 扫描目录不存在或不是目录: {output_dir}")
        sys.exit(2)

    required_files = REQUIRED_BY_MODE.get(mode, REQUIRED_BY_MODE["M1"])
    missing_files = [name for name in required_files if not (output_dir / name).exists()]
    if missing_files:
        print("[FAIL] 产物不完整，缺少以下文件：")
        for missing_file in missing_files:
            print(f"  - {missing_file}")
        sys.exit(1)

    if "scan.db" in required_files:
        db_path = output_dir / "scan.db"
        conn = None
        try:
            conn = sqlite3.connect(str(db_path))
            tables = get_existing_tables(conn)
            if "modules" not in tables:
                print("[ERR] scan.db 缺少 modules 表，数据可能已损坏")
                sys.exit(2)

            module_count = conn.execute("SELECT COUNT(*) FROM modules").fetchone()[0]
        except sqlite3.Error as exc:
            print(f"[ERR] 读取 scan.db 失败: {exc}")
            sys.exit(2)
        finally:
            if conn is not None:
                conn.close()

        if module_count == 0:
            print("[FAIL] scan.db 存在但 modules 表为空，数据可能未正确加载")
            sys.exit(1)

    print(f"[OK] {mode} 模式产物验证通过（{len(required_files)} 个文件）")
    sys.exit(0)


def cmd_export_to_claude_md(args):
    """从 scan.db 导出摘要到 CLAUDE.md 项目特定区域。"""
    db_path = Path(args.db)
    claude_md_path = Path(args.claude_md)
    max_items = args.max_items
    max_lines = args.max_lines

    if not db_path.exists():
        print(f"[ERR] 数据库不存在: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # 获取表列表，用于判断哪些表存在
    tables = {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}

    # 提取关键数据（根据存在的表动态查询）
    modules = []
    if "modules" in tables:
        modules = conn.execute(
            "SELECT id, path, responsibility FROM modules ORDER BY id LIMIT ?",
            (max_items,),
        ).fetchall()

    entry_points = []
    if "entry_points" in tables:
        entry_points = conn.execute(
            "SELECT entry_point, trigger, call_chain_top3 FROM entry_points ORDER BY entry_point LIMIT ?",
            (max_items,),
        ).fetchall()
    elif "functions" in tables:
        # 从 functions 表取公开函数作为入口点
        rows = conn.execute(
            "SELECT name, file_path, line_number FROM functions WHERE is_public=1 ORDER BY name LIMIT ?",
            (max_items,),
        ).fetchall()
        entry_points = [
            {
                "entry_point": f"{r['name']}()",
                "trigger": f"{r['file_path']}:{r['line_number']}",
                "call_chain_top3": None,
            }
            for r in rows
        ]

    constraints = []
    if "constraints" in tables:
        constraints = conn.execute(
            "SELECT source_doc, content, priority FROM constraints ORDER BY priority DESC LIMIT ?",
            (max_items,),
        ).fetchall()

    impact_high = []
    if "impact_items" in tables:
        impact_high = conn.execute(
            "SELECT change_point, risk_level FROM impact_items WHERE risk_level IN ('high', 'critical') ORDER BY risk_level DESC LIMIT ?",
            (max_items,),
        ).fetchall()

    # 获取扫描元信息（key-value 格式）
    scan_info = {}
    if "scan_meta" in tables:
        rows = conn.execute("SELECT key, value FROM scan_meta").fetchall()
        scan_info = {r["key"]: r["value"] for r in rows}

    conn.close()

    # 构建摘要内容
    lines: list[str] = []
    lines.append("## 扫描摘要（auto-generated by largebase-scan）")
    lines.append("")
    lines.append(f"> 扫描时间: {datetime.now().isoformat(timespec='minutes')}")
    lines.append(f"> 数据来源: `{db_path}`")
    lines.append("")

    # 入口点
    if entry_points:
        lines.append("### 入口点")
        for ep in entry_points:
            chain = ep["call_chain_top3"] or "未记录"
            lines.append(f"- `{ep['entry_point']}` ({ep['trigger']}) → {chain}")
        lines.append("")

    # 核心模块
    if modules:
        lines.append("### 核心模块")
        for m in modules:
            mod_id = m["id"] or "未命名"
            resp = m["responsibility"] or "未填写"
            lines.append(f"- `{mod_id}`: {resp}")
        lines.append("")

    # 关键约束
    if constraints:
        lines.append("### 关键约束")
        for c in constraints:
            src = c["source_doc"].split("/")[-1] if "/" in c["source_doc"] else c["source_doc"]
            lines.append(f"- [{src}] {c['content']}")
        lines.append("")

    # 高风险变更点
    if impact_high:
        lines.append("### 高风险变更点")
        for i in impact_high:
            lines.append(f"- `{i['change_point']}` (风险: {i['risk_level']})")
        lines.append("")

    # 截断到最大行数
    if len(lines) > max_lines:
        lines = lines[: max_lines - 1]
        lines.append("> ... 摘要已截断，完整数据请查询 scan.db")

    summary_text = "\n".join(lines)

    # 写入 CLAUDE.md
    existing_content = ""
    marker_start = "<!-- SCAN_SUMMARY_START -->"
    marker_end = "<!-- SCAN_SUMMARY_END -->"

    if claude_md_path.exists():
        existing_content = claude_md_path.read_text(encoding="utf-8")

    # 如果已有标记，替换；否则追加到文件末尾
    if marker_start in existing_content and marker_end in existing_content:
        before = existing_content.split(marker_start)[0]
        after = existing_content.split(marker_end)[1]
        new_content = f"{before}{marker_start}\n{summary_text}\n{marker_end}{after}"
    else:
        new_content = f"{existing_content.rstrip()}\n\n{marker_start}\n{summary_text}\n{marker_end}\n"

    claude_md_path.write_text(new_content, encoding="utf-8")
    print(f"[OK] 已更新 {claude_md_path} ({len(lines)} 行)")


def cmd_merge(args):
    """合并多个 scan-data.json（并行 Codex 后汇总用）。"""
    input_paths = [Path(p) for p in args.inputs]
    output_path = Path(args.output)

    # 检查输入
    missing = [str(p) for p in input_paths if not p.exists()]
    if missing:
        for m in missing:
            print(f"[ERR] 文件不存在: {m}")
        return

    merged = {
        "scan_meta": {},
        "modules": [],
        "functions": [],
        "data_structures": [],
        "data_flows": [],
        "constraints": [],
        "impact_items": [],
        "reference_docs": [],
    }

    seen_module_ids: set[str] = set()
    seen_function_ids: set[str] = set()
    seen_other_ids: dict[str, set[str]] = {
        "data_structures": set(),
        "data_flows": set(),
        "constraints": set(),
        "impact_items": set(),
        "reference_docs": set(),
    }

    source_files = []

    for idx, json_path in enumerate(input_paths):
        try:
            with json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[WARN] 读取失败 {json_path}: {e}", file=sys.stderr)
            continue

        source_files.append(str(json_path))

        # 合并 scan_meta（保留第一个，其余合并 scope）
        if not merged["scan_meta"]:
            merged["scan_meta"] = dict(data.get("scan_meta", {}))
        else:
            existing_scope = merged["scan_meta"].get("scan_scope", [])
            new_scope = data.get("scan_meta", {}).get("scan_scope", [])
            if isinstance(existing_scope, list) and isinstance(new_scope, list):
                merged["scan_meta"]["scan_scope"] = list(dict.fromkeys(existing_scope + new_scope))

        module_rows = get_module_rows(data)
        function_rows = get_function_rows(data)

        # 合并模块（按 name+path 去重）
        for mod in module_rows:
            mod_path = (mod.get("path") or "").replace("\\", "/")
            mod_name = mod.get("name") or Path(mod_path).name
            dedup_key = f"{mod_name}|{mod_path}"
            if dedup_key not in seen_module_ids:
                seen_module_ids.add(dedup_key)
                merged["modules"].append(mod)

        # 合并函数（按 name+file_path+line 去重）
        for func in function_rows:
            func_name = func.get("name", "")
            file_path = (func.get("file_path") or func.get("file_line") or "").replace("\\", "/")
            line = func.get("line_number") or func.get("line") or 0
            dedup_key = f"{func_name}|{file_path}|{line}"
            if dedup_key not in seen_function_ids:
                seen_function_ids.add(dedup_key)
                merged["functions"].append(func)

        # 合并其他表（按 id 去重，无 id 则全量追加）
        for table_key in seen_other_ids:
            get_fn = {
                "data_structures": get_datastructure_rows,
                "data_flows": get_dataflow_rows,
                "constraints": get_constraint_rows,
                "impact_items": get_impact_rows,
                "reference_docs": get_reference_doc_rows,
            }[table_key]
            for item in get_fn(data):
                item_id = item.get("id") or item.get("name") or ""
                dedup_key = f"{table_key}|{item_id}"
                if not item_id or dedup_key not in seen_other_ids[table_key]:
                    seen_other_ids[table_key].add(dedup_key)
                    merged[table_key].append(item)

    # 更新 meta
    merged["scan_meta"]["merged_from"] = source_files
    merged["scan_meta"]["merged_at"] = datetime.now().isoformat()
    merged["scan_meta"]["module_count"] = len(merged["modules"])
    merged["scan_meta"]["function_count"] = len(merged["functions"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] 合并完成: {len(source_files)} 个文件 → {output_path}")
    print(f"  模块: {len(merged['modules'])}")
    print(f"  函数: {len(merged['functions'])}")
    print(f"  约束: {len(merged['constraints'])}")
    print(f"  影响项: {len(merged['impact_items'])}")


def main():
    """CLI 入口。"""
    setup_stdio_encoding()
    parser = argparse.ArgumentParser(
        description="largebase-structured-scan: 结构化代码库扫描工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="初始化扫描目录和数据库")
    p_scan.add_argument("--mode", required=True, choices=list(SCAN_MODES.keys()), help="扫描模式")
    p_scan.add_argument("--scope", required=True, nargs="+", help="扫描范围（支持多个目录，空格分隔）")
    p_scan.add_argument("--topic", required=True, help="扫描主题")
    p_scan.add_argument("--refs", nargs="*", help="参考文档路径")

    p_load = sub.add_parser("load", help="从 scan-data.json 加载到 SQLite")
    p_load.add_argument("--load", required=True, help="JSON 文件路径")
    p_load.add_argument("--db", required=True, help="数据库路径")

    p_query = sub.add_parser("query", help="查询 SQLite 扫描结果")
    p_query.add_argument("--query", required=True, help="查询字符串")
    p_query.add_argument("--db", required=True, help="数据库路径")
    p_query.add_argument("--filter", help="特殊查询模式的过滤词")
    p_query.add_argument("--limit", type=int, default=20, help="结果条数上限")
    p_query.add_argument(
        "--type",
        default="all",
        choices=["all", "function", "module", "constraint", "impact", "dataflow"],
        help="查询类型",
    )

    p_measure = sub.add_parser("measure", help="统计代码库规模并输出 JSON")
    p_measure.add_argument("--scope", required=True, nargs="+", help="扫描范围路径（支持多个目录）")
    p_measure.add_argument("--output", help="可选，输出 JSON 文件路径（默认输出到 stdout）")

    p_extract = sub.add_parser("extract", help="本地提取代码结构（零 AI token）")
    p_extract.add_argument("--scope", required=True, nargs="+", help="扫描范围路径")
    p_extract.add_argument("--topic", required=True, help="扫描主题")
    p_extract.add_argument("--output", help="输出目录（默认 docs/scan/YYYY-MM-DD-topic/）")
    p_extract.add_argument("--incremental", action="store_true", help="跳过哈希未变的文件")
    p_extract.add_argument("--db", help="哈希数据库路径（默认输出目录下的 scan.db）")

    p_merge = sub.add_parser("merge", help="合并多个 scan-data.json（并行 Codex 结果汇总）")
    p_merge.add_argument("--inputs", required=True, nargs="+", help="要合并的 scan-data.json 路径列表")
    p_merge.add_argument("--output", required=True, help="合并后输出的 scan-data.json 路径")

    p_export = sub.add_parser("export-to-claude-md", help="从 scan.db 导出摘要到 CLAUDE.md")
    p_export.add_argument("--db", required=True, help="数据库路径")
    p_export.add_argument("--claude-md", default="CLAUDE.md", help="目标 CLAUDE.md 路径")
    p_export.add_argument("--max-items", type=int, default=5, help="每个摘要分组最多条目数")
    p_export.add_argument("--max-lines", type=int, default=80, help="摘要最大行数")

    p_verify = sub.add_parser("verify", help="校验扫描产物完整性")
    p_verify.add_argument("--dir", required=True, help="扫描输出目录")
    p_verify.add_argument("--mode", default="M1", choices=list(REQUIRED_BY_MODE.keys()), help="扫描模式")

    args = parser.parse_args()
    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "load":
        cmd_load(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "measure":
        cmd_measure(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == "export-to-claude-md":
        cmd_export_to_claude_md(args)
    elif args.command == "verify":
        cmd_verify(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
