from pathlib import Path
import argparse
import sys

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from scan_shared import *
from scan_db_queries import *
from scan_extract_core import *
from scan_extract_core import _aggregate_modules
from scan_sidecar_paths import *
from scan_sidecar_views import *
from scan_rich_contract import *
from scan_commands import *
from scan_doc_gen import cmd_generate_docs


def main():
    """CLI 入口。"""
    setup_stdio_encoding()
    parser = argparse.ArgumentParser(
        description="largebase-structured-scan: 结构化代码库扫描工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="初始化扫描目录和数据库")
    p_scan.add_argument("--mode", required=True, choices=sorted(SCAN_MODES.keys()))
    p_scan.add_argument("--scope", required=True, nargs="+", help="扫描范围路径（支持多个）")
    p_scan.add_argument("--topic", required=True, help="扫描主题，用于输出目录命名")
    p_scan.add_argument("--refs", nargs="*", default=[], help="参考文档路径列表")
    p_scan.add_argument("--output", default="", help="输出目录，默认 docs/scan/<date>-<topic>")
    p_scan.set_defaults(func=cmd_scan)

    p_load = sub.add_parser("load", help="从 scan-data.json 加载到 SQLite")
    p_load.add_argument("--load", required=True, help="scan-data.json 路径")
    p_load.add_argument("--db", required=True, help="SQLite 数据库路径")
    p_load.set_defaults(func=cmd_load)

    p_query = sub.add_parser("query", help="查询 SQLite 中的结构化数据")
    p_query.add_argument("--query", required=True, help="查询关键字或预置模式")
    p_query.add_argument("--type", default="all", choices=["all", "modules", "functions", "dataflows", "constraints", "impacts", "docs"], help="查询类型")
    p_query.add_argument("--db", required=True, help="SQLite 数据库路径")
    p_query.add_argument("--limit", type=int, default=20, help="返回条数上限")
    p_query.set_defaults(func=cmd_query)

    p_measure = sub.add_parser("measure", help="统计 scope 的代码/文档体量")
    p_measure.add_argument("--scope", required=True, nargs="+", help="要统计的路径列表")
    p_measure.add_argument("--output", required=True, help="输出 JSON 路径")
    p_measure.set_defaults(func=cmd_measure)

    p_extract = sub.add_parser("extract", help="本地提取代码结构，零 AI token")
    p_extract.add_argument("--scope", required=True, nargs="+", help="提取范围路径（支持多个）")
    p_extract.add_argument("--topic", required=True, help="提取主题")
    p_extract.add_argument("--output", default="", help="输出目录，默认 docs/scan/<date>-<topic>")
    p_extract.add_argument("--db", default="", help="用于增量缓存的 SQLite 路径，默认输出目录下 scan.db")
    p_extract.add_argument("--incremental", action="store_true", help="启用增量提取，跳过未变更文件")
    p_extract.set_defaults(func=cmd_extract)

    p_verify = sub.add_parser("verify", help="检查目录产物是否满足当前模式要求")
    p_verify.add_argument("--mode", required=True, choices=sorted(SCAN_MODES.keys()))
    p_verify.add_argument("--dir", required=True, help="扫描结果目录")
    p_verify.set_defaults(func=cmd_verify)

    p_export = sub.add_parser("export-to-claude-md", help="将 scan.db 摘要写入 CLAUDE.md")
    p_export.add_argument("--db", required=True, help="SQLite 数据库路径")
    p_export.add_argument("--claude-md", required=True, help="目标 CLAUDE.md 路径")
    p_export.add_argument("--max-lines", type=int, default=80, help="摘要最大行数")
    p_export.set_defaults(func=cmd_export_to_claude_md)

    p_merge = sub.add_parser("merge", help="合并多个 scan-data.json（并行 Codex 结果汇总）")
    p_merge.add_argument("--inputs", required=True, nargs="+", help="要合并的 scan-data.json 路径列表")
    p_merge.add_argument("--output", required=True, help="合并后输出的 scan-data.json 路径")
    p_merge.set_defaults(func=cmd_merge)

    p_gendoc = sub.add_parser("generate-docs", help="从 scan-data.json 代码生成 01-06 结构化文档模板")
    p_gendoc.add_argument("--scan-data", required=True, help="scan-data.json 路径")
    p_gendoc.add_argument("--output", default="", help="输出目录，默认 scan-data.json 同级目录")
    p_gendoc.add_argument("--docs", nargs="*", default=None, help="要生成的文档编号列表，如 01 02 03；默认全部")
    p_gendoc.set_defaults(func=cmd_generate_docs)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
