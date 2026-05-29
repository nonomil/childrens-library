#!/usr/bin/env python3
"""Memory System - Markdown → SQLite FTS5/BM25 搜索引擎。
用法: python memory.py index|search|status|add|cleanup ...
CLI 参数保持与旧版兼容。
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = "memory"
DEFAULT_DB_NAME = "memory.sqlite"
CHUNK_MAX_CHARS = 1600
CHUNK_OVERLAP_CHARS = 320
DEFAULT_TOP_K = 6
DEFAULT_MIN_SCORE = -20.0
TOKENIZER = "trigram"
SCHEMA_VERSION = "fts5-bm25-v1"
CONTEXT_RADIUS = 1


def init_db(db_path: str) -> sqlite3.Connection:
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    version = conn.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
    if not version or version["value"] != SCHEMA_VERSION:
        conn.executescript("DROP TABLE IF EXISTS chunks_fts; DROP TABLE IF EXISTS chunks; DROP TABLE IF EXISTS files;")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS files (
          path TEXT PRIMARY KEY, hash TEXT NOT NULL, mtime_ns INTEGER NOT NULL,
          size INTEGER NOT NULL, indexed_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chunks (
          id TEXT PRIMARY KEY, path TEXT NOT NULL, chunk_index INTEGER NOT NULL,
          start_line INTEGER NOT NULL, end_line INTEGER NOT NULL,
          hash TEXT NOT NULL, text TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_chunks_path_index ON chunks(path, chunk_index);
        """
    )
    try:
        conn.execute(
            f"CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5("
            f"text, content='chunks', content_rowid='rowid', tokenize='{TOKENIZER}')"
        )
    except sqlite3.OperationalError as exc:
        raise SystemExit("错误: 当前 SQLite 不支持 FTS5 trigram tokenizer") from exc
    conn.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
        [("schema_version", SCHEMA_VERSION), ("search_engine", "fts5+bm25"), ("tokenizer", TOKENIZER)],
    )
    conn.commit()
    return conn


def chunk_markdown(text: str) -> list[dict]:
    lines = text.split("\n")
    chunks, current_lines = [], []
    current_start = 1
    current_chars = 0
    for line_no, line in enumerate(lines, 1):
        is_heading = re.match(r"^#{1,6}\s", line)
        if is_heading and current_lines:
            chunk_text = "\n".join(current_lines).strip()
            if chunk_text:
                chunks.append({"start_line": current_start, "end_line": line_no - 1, "text": chunk_text})
            current_lines, current_start, current_chars = [], line_no, 0
        current_lines.append(line)
        current_chars += len(line) + 1
        if current_chars >= CHUNK_MAX_CHARS and not is_heading:
            chunk_text = "\n".join(current_lines).strip()
            if chunk_text:
                chunks.append({"start_line": current_start, "end_line": line_no, "text": chunk_text})
            overlap_lines, overlap_chars = [], 0
            for overlap_line in reversed(current_lines):
                overlap_chars += len(overlap_line) + 1
                if overlap_chars > CHUNK_OVERLAP_CHARS:
                    break
                overlap_lines.insert(0, overlap_line)
            current_lines = overlap_lines
            current_start = line_no - len(overlap_lines) + 1
            current_chars = sum(len(item) + 1 for item in overlap_lines)
    if current_lines:
        chunk_text = "\n".join(current_lines).strip()
        if chunk_text:
            chunks.append({"start_line": current_start, "end_line": len(lines), "text": chunk_text})
    return chunks


def file_hash(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def list_md_files(memory_dir: str) -> list[str]:
    root = Path(memory_dir).resolve()
    seen, files = set(), []
    candidates = [root.parent / "MEMORY.md"]
    if root.exists():
        candidates.extend(sorted(root.rglob("*.md")))
    for path in candidates:
        if path.exists():
            resolved = str(path.resolve())
            if resolved not in seen:
                seen.add(resolved)
                files.append(resolved)
    return files


def resolve_db_path(memory_dir: str, db_path: str | None) -> str: return os.path.abspath(db_path) if db_path else os.path.join(memory_dir, DEFAULT_DB_NAME)


def rebuild_fts(conn: sqlite3.Connection) -> None: conn.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")


def upsert_file(conn: sqlite3.Connection, filepath: str) -> int:
    content = Path(filepath).read_text(encoding="utf-8")
    chunks = chunk_markdown(content)
    stat = os.stat(filepath)
    conn.execute("DELETE FROM chunks WHERE path = ?", (filepath,))
    for chunk_index, chunk in enumerate(chunks):
        conn.execute(
            "INSERT INTO chunks(id, path, chunk_index, start_line, end_line, hash, text) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (
                f"{filepath}:{chunk['start_line']}-{chunk['end_line']}",
                filepath,
                chunk_index,
                chunk["start_line"],
                chunk["end_line"],
                text_hash(chunk["text"]),
                chunk["text"],
            ),
        )
    conn.execute(
        "INSERT OR REPLACE INTO files(path, hash, mtime_ns, size, indexed_at) VALUES(?, ?, ?, ?, ?)",
        (filepath, file_hash(filepath), stat.st_mtime_ns, stat.st_size, datetime.now().isoformat(timespec="seconds")),
    )
    return len(chunks)


def sync_index(conn: sqlite3.Connection, memory_dir: str, verbose: bool = False) -> dict:
    current_files = list_md_files(memory_dir)
    indexed_rows = {row["path"]: row for row in conn.execute("SELECT path, mtime_ns, size FROM files")}
    current_stats = {path: (os.stat(path).st_mtime_ns, os.stat(path).st_size) for path in current_files}
    changed_files, skipped_files = [], 0
    for path in current_files:
        row = indexed_rows.get(path)
        if row and (row["mtime_ns"], row["size"]) == current_stats[path]:
            skipped_files += 1
        else:
            changed_files.append(path)
    removed_files = sorted(set(indexed_rows) - set(current_stats))
    indexed_chunks = 0
    with conn:
        for path in removed_files:
            conn.execute("DELETE FROM chunks WHERE path = ?", (path,))
            conn.execute("DELETE FROM files WHERE path = ?", (path,))
            if verbose:
                print(f"  已移除: {Path(path).name}")
        for path in changed_files:
            chunk_count = upsert_file(conn, path)
            indexed_chunks += chunk_count
            if verbose:
                print(f"  已索引: {Path(path).name} ({chunk_count} 块)")
        if changed_files or removed_files:
            rebuild_fts(conn)
    return {
        "total_files": len(current_files),
        "indexed_files": len(changed_files),
        "indexed_chunks": indexed_chunks,
        "removed_files": len(removed_files),
        "skipped_files": skipped_files,
        "changed": bool(changed_files or removed_files),
    }


def build_match_queries(query: str) -> list[str]:
    stripped = query.strip(); escaped = stripped.replace('"', '""')
    return [stripped] if escaped == stripped else [stripped, f'"{escaped}"']


def rows_to_results(rows: list[sqlite3.Row], source: str) -> list[dict]:
    return [
        {
            "id": row["id"],
            "path": row["path"],
            "chunk_index": row["chunk_index"],
            "start_line": row["start_line"],
            "end_line": row["end_line"],
            "text": row["text"],
            "score": float(row["score"]),
            "source": source,
        }
        for row in rows
    ]


def fts_search(conn: sqlite3.Connection, query: str, top_k: int) -> list[dict]:
    if len(query.strip()) < 3:
        return []
    sql = (
        "SELECT chunks.id, chunks.path, chunks.chunk_index, chunks.start_line, chunks.end_line, "
        "chunks.text, bm25(chunks_fts) AS score FROM chunks_fts "
        "JOIN chunks ON chunks.rowid = chunks_fts.rowid WHERE chunks_fts MATCH ? "
        "ORDER BY score, chunks.path, chunks.chunk_index LIMIT ?"
    )
    for candidate in build_match_queries(query):
        try:
            rows = conn.execute(sql, (candidate, max(top_k * 3, top_k))).fetchall()
        except sqlite3.OperationalError:
            rows = []
        if rows:
            return rows_to_results(rows, "fts")
    return []


def like_search(conn: sqlite3.Connection, query: str, top_k: int) -> list[dict]:
    normalized = query.strip().lower()
    if not normalized:
        return []
    rows = conn.execute(
        """
        SELECT id, path, chunk_index, start_line, end_line, text,
        -CAST((length(lower(text)) - length(replace(lower(text), ?, ''))) AS REAL) / ? AS score,
        instr(lower(text), ?) AS first_hit
        FROM chunks
        WHERE lower(text) LIKE '%' || ? || '%'
        ORDER BY score, first_hit, length(text), path, chunk_index
        LIMIT ?
        """,
        (normalized, max(len(normalized), 1), normalized, normalized, max(top_k * 3, top_k)),
    ).fetchall()
    return rows_to_results(rows, "like")


def attach_context(conn: sqlite3.Connection, result: dict) -> dict:
    rows = conn.execute(
        "SELECT start_line, end_line, text FROM chunks WHERE path = ? AND chunk_index BETWEEN ? AND ? ORDER BY chunk_index",
        (result["path"], max(result["chunk_index"] - CONTEXT_RADIUS, 0), result["chunk_index"] + CONTEXT_RADIUS),
    ).fetchall()
    context = "\n\n".join(row["text"] for row in rows) if rows else result["text"]
    result["context_start_line"] = rows[0]["start_line"] if rows else result["start_line"]
    result["context_end_line"] = rows[-1]["end_line"] if rows else result["end_line"]
    result["context"] = context
    result["snippet"] = context[:700]
    return result


def search_chunks(conn: sqlite3.Connection, query: str, top_k: int, min_score: float) -> list[dict]:
    results = like_search(conn, query, top_k) if len(query.strip()) < 3 else fts_search(conn, query, top_k)
    if not results:
        results = like_search(conn, query, top_k)
    matched = []
    for item in results:
        if item["score"] < min_score:
            continue
        matched.append(attach_context(conn, item))
        if len(matched) >= top_k:
            break
    return matched


def cmd_index(args) -> None:
    memory_dir = os.path.abspath(args.dir)
    db_path = resolve_db_path(memory_dir, args.db)
    conn = init_db(db_path)
    stats = sync_index(conn, memory_dir, verbose=True)
    conn.close()
    if not stats["total_files"]:
        print(f"没有找到 .md 文件 (目录: {memory_dir})")
    print(
        f"\n完成: 索引 {stats['indexed_files']} 个文件 ({stats['indexed_chunks']} 块)，"
        f"移除 {stats['removed_files']} 个文件，跳过 {stats['skipped_files']} 个未变化文件"
    )
    print(f"数据库: {db_path}")


def cmd_search(args) -> None:
    memory_dir = os.path.abspath(args.dir)
    db_path = resolve_db_path(memory_dir, args.db)
    conn = init_db(db_path)
    sync_index(conn, memory_dir, verbose=False)
    results = search_chunks(conn, args.query, args.top, args.min_score)
    conn.close()
    if not results:
        print("[]" if args.json else "没有找到相关结果")
        return
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "path": item["path"],
                        "start_line": item["start_line"],
                        "end_line": item["end_line"],
                        "score": round(item["score"], 4),
                        "snippet": item["snippet"],
                        "context_start_line": item["context_start_line"],
                        "context_end_line": item["context_end_line"],
                        "context": item["context"],
                        "source": item["source"],
                    }
                    for item in results
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    for index, item in enumerate(results, 1):
        snippet = item["snippet"][:220].replace("\n", " ")
        print(
            f"\n[{index}] {Path(item['path']).name}:{item['start_line']}-{item['end_line']}  "
            f"(上下文: {item['context_start_line']}-{item['context_end_line']}, 分数: {item['score']:.4f})"
        )
        print(f"    {snippet}...")


def cmd_status(args) -> None:
    memory_dir = os.path.abspath(args.dir)
    db_path = resolve_db_path(memory_dir, args.db)
    conn = init_db(db_path)
    file_count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    engine = conn.execute("SELECT value FROM meta WHERE key='search_engine'").fetchone()
    tokenizer = conn.execute("SELECT value FROM meta WHERE key='tokenizer'").fetchone()
    db_size = Path(db_path).stat().st_size if Path(db_path).exists() else 0
    print(f"数据库:    {db_path}")
    print(f"大小:      {db_size / 1024 / 1024:.2f} MB")
    print(f"文件数:    {file_count}")
    print(f"分块数:    {chunk_count}")
    print(f"搜索引擎:  {engine['value'] if engine else 'N/A'}")
    print(f"分词器:    {tokenizer['value'] if tokenizer else 'N/A'}")
    if args.verbose:
        print("\n--- 已索引文件 ---")
        for row in conn.execute("SELECT path, size, indexed_at FROM files ORDER BY path"):
            print(f"  {Path(row['path']).name} ({row['size']} bytes, {row['indexed_at']})")
    conn.close()


def cmd_add(args) -> None:
    memory_dir = os.path.abspath(args.dir)
    Path(memory_dir).mkdir(parents=True, exist_ok=True)
    filename = (args.file if args.file.endswith(".md") else f"{args.file}.md") if args.file else f"{datetime.now():%Y-%m-%d-%H%M}.md"
    filepath = Path(memory_dir) / filename
    mode = "a" if filepath.exists() else "w"
    with filepath.open(mode, encoding="utf-8") as handle:
        if mode == "a":
            handle.write("\n\n")
        handle.write(args.content)
        handle.write("\n")
    print(f"已写入: {filepath}")
    conn = init_db(resolve_db_path(memory_dir, args.db))
    with conn:
        chunk_count = upsert_file(conn, str(filepath.resolve()))
        rebuild_fts(conn)
    conn.close()
    print(f"已索引: {chunk_count} 块")


def cmd_cleanup(args) -> None:
    memory_dir = os.path.abspath(args.dir)
    memory_root = Path(memory_dir)
    if not memory_root.exists():
        print(f"目录不存在: {memory_dir}")
        return
    cutoff = datetime.now() - timedelta(days=args.days)
    stale_files = [path for path in sorted(memory_root.rglob("*.md")) if datetime.fromtimestamp(path.stat().st_mtime) < cutoff]
    if not stale_files:
        print(f"没有超过 {args.days} 天的文件")
        return
    print(f"将删除 {len(stale_files)} 个文件:")
    for path in stale_files:
        print(f"  {path.name} (修改于 {datetime.fromtimestamp(path.stat().st_mtime):%Y-%m-%d})")
    if not args.force and input("\n确认删除? [y/N] ").lower() != "y":
        print("已取消")
        return
    for path in stale_files:
        path.unlink()
        print(f"  已删除: {path.name}")
    db_path = resolve_db_path(memory_dir, args.db)
    if Path(db_path).exists():
        print("\n重新同步索引...")
        conn = init_db(db_path)
        sync_index(conn, memory_dir, verbose=False)
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Memory System - Markdown FTS5/BM25 搜索", formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")
    p_index = sub.add_parser("index", help="索引 .md 文件")
    p_index.add_argument("--dir", default=DEFAULT_MEMORY_DIR, help="记忆目录 (默认: memory/)")
    p_index.add_argument("--db", default=None, help="数据库路径")
    p_search = sub.add_parser("search", help="搜索记忆")
    p_search.add_argument("query", help="搜索查询")
    p_search.add_argument("--top", type=int, default=DEFAULT_TOP_K, help="返回结果数")
    p_search.add_argument("--min-score", type=float, default=DEFAULT_MIN_SCORE, help="BM25 最小分数")
    p_search.add_argument("--db", default=None, help="数据库路径")
    p_search.add_argument("--json", action="store_true", help="JSON 输出")
    p_search.add_argument("--dir", default=DEFAULT_MEMORY_DIR, help="记忆目录")
    p_status = sub.add_parser("status", help="查看索引状态")
    p_status.add_argument("--db", default=None, help="数据库路径")
    p_status.add_argument("--dir", default=DEFAULT_MEMORY_DIR, help="记忆目录")
    p_status.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    p_add = sub.add_parser("add", help="添加记忆")
    p_add.add_argument("content", help="记忆内容")
    p_add.add_argument("--file", "-f", default=None, help="目标文件名")
    p_add.add_argument("--dir", default=DEFAULT_MEMORY_DIR, help="记忆目录")
    p_add.add_argument("--db", default=None, help="数据库路径")
    p_cleanup = sub.add_parser("cleanup", help="清理旧记忆")
    p_cleanup.add_argument("--days", type=int, default=90, help="清理超过 N 天的文件")
    p_cleanup.add_argument("--dir", default=DEFAULT_MEMORY_DIR, help="记忆目录")
    p_cleanup.add_argument("--db", default=None, help="数据库路径")
    p_cleanup.add_argument("--force", "-f", action="store_true", help="不确认直接删除")
    args = parser.parse_args()
    if args.command == "index":
        cmd_index(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "cleanup":
        cmd_cleanup(args)
    else:
        parser.print_help()


if __name__ == "__main__": main()
