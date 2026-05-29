# -*- coding: utf-8 -*-
"""
Interactive Code Graph Viewer — Local HTTP Server
Reads .code-review-graph/graph.db, serves API + static HTML.
Usage: python server.py [--port PORT] [--db PATH]
"""
import argparse
import json
import os
import sqlite3
import subprocess
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=3334)
parser.add_argument("--db", type=str, default=None, help="Path to graph.db")
args = parser.parse_args()

PORT = args.port
DB_PATH = os.path.abspath(args.db) if args.db else os.path.join(os.path.dirname(__file__), "..", "graph.db")
HTML_PATH = os.path.join(os.path.dirname(__file__), "viewer.html")
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _fix_path(s):
    """Replace backslashes with forward slashes for JSON safety."""
    if not s:
        return s
    return s.replace(chr(92), "/")


def node_to_dict(row):
    """Convert a sqlite3.Row to a dict with short file_path."""
    d = dict(row)
    # Normalize all path fields to forward slashes for JSON safety
    for key in ("file_path", "qualified_name"):
        d[key] = _fix_path(d.get(key, ""))
    # Make file_path relative to repo root
    fp = d.get("file_path", "")
    fp_abs = _fix_path(REPO_ROOT)
    if fp and fp.startswith(fp_abs):
        d["rel_path"] = fp[len(fp_abs) + 1:]  # strip leading slash
    else:
        d["rel_path"] = fp
    return d


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Quieter logging
        pass

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False, indent=None).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, path):
        with open(path, "r", encoding="utf-8") as f:
            body = f.read().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # Serve viewer HTML
        if path == "/" or path == "/viewer.html":
            self._html(HTML_PATH)
            return

        # API: open file in VS Code
        if path == "/open":
            filepath = params.get("file", [None])[0]
            line = params.get("line", ["1"])[0]
            if not filepath:
                self._json({"error": "missing file param"}, 400)
                return
            # Resolve relative path
            if not os.path.isabs(filepath):
                filepath = os.path.join(REPO_ROOT, filepath)
            try:
                subprocess.Popen(
                    ["code", "--goto", f"{filepath}:{line}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self._json({"ok": True, "file": filepath, "line": line})
            except FileNotFoundError:
                self._json({"error": "code command not found"}, 500)
            return

        conn = get_db()
        try:
            # API: communities (modules)
            if path == "/api/communities":
                cur = conn.execute(
                    "SELECT c.id, c.name, c.size, c.dominant_language, c.description "
                    "FROM communities c ORDER BY c.size DESC"
                )
                rows = [dict(r) for r in cur.fetchall()]
                self._json(rows)
                return

            # API: nodes, optionally filtered by community or search
            if path == "/api/nodes":
                community_id = params.get("community", [None])[0]
                search = params.get("q", [None])[0]
                kind = params.get("kind", [None])[0]

                sql = (
                    "SELECT n.id, n.kind, n.name, n.qualified_name, n.file_path, "
                    "n.line_start, n.line_end, n.parent_name, n.community_id, "
                    "n.signature, n.is_test, c.name as community_name "
                    "FROM nodes n LEFT JOIN communities c ON n.community_id = c.id "
                    "WHERE n.kind != 'File'"
                )
                args = []
                if community_id:
                    sql += " AND n.community_id = ?"
                    args.append(community_id)
                if kind:
                    sql += " AND n.kind = ?"
                    args.append(kind)
                if search:
                    sql += " AND (n.name LIKE ? OR n.qualified_name LIKE ?)"
                    args.extend([f"%{search}%", f"%{search}%"])

                sql += " ORDER BY n.file_path, n.line_start LIMIT 500"
                cur = conn.execute(sql, args)
                rows = [node_to_dict(r) for r in cur.fetchall()]
                self._json(rows)
                return

            # API: edges for a specific node
            if path == "/api/edges":
                node_id = params.get("node", [None])[0]
                if not node_id:
                    self._json({"error": "missing node param"}, 400)
                    return

                # Get edges where this node is source or target
                sql = (
                    "SELECT e.kind, e.source_qualified, e.target_qualified, "
                    "s.id as source_id, s.name as source_name, s.file_path as source_file, "
                    "s.line_start as source_line, s.kind as source_kind, "
                    "t.id as target_id, t.name as target_name, t.file_path as target_file, "
                    "t.line_start as target_line, t.kind as target_kind "
                    "FROM edges e "
                    "JOIN nodes s ON e.source_qualified = s.qualified_name "
                    "JOIN nodes t ON e.target_qualified = t.qualified_name "
                    "WHERE s.id = ? OR t.id = ?"
                )
                cur = conn.execute(sql, [node_id, node_id])
                rows = []
                for r in cur.fetchall():
                    d = dict(r)
                    for key in ["source_file", "target_file", "source_qualified", "target_qualified"]:
                        d[key] = _fix_path(d.get(key, ""))
                    # Make source/target file relative
                    fp_abs = _fix_path(REPO_ROOT)
                    for key in ["source_file", "target_file"]:
                        fp = d.get(key, "")
                        if fp and fp.startswith(fp_abs):
                            d[key] = fp[len(fp_abs) + 1:]
                    rows.append(d)
                self._json(rows)
                return

            # API: graph data for D3 visualization
            if path == "/api/graph":
                graph_conn = sqlite3.connect(DB_PATH)
                graph_conn.row_factory = sqlite3.Row

                communities = params.get("communities", [None])[0]
                sql_nodes = (
                    "SELECT n.id, n.kind, n.name, n.qualified_name, n.file_path, "
                    "n.line_start, n.line_end, n.parent_name, n.community_id, "
                    "c.name as community_name "
                    "FROM nodes n LEFT JOIN communities c ON n.community_id = c.id "
                    "WHERE n.kind != 'File' LIMIT 2000"
                )
                cur = graph_conn.execute(sql_nodes)
                nodes = [node_to_dict(r) for r in cur.fetchall()]

                try:
                    sql_edges = (
                        "SELECT s.id, t.id, e.kind "
                        "FROM edges e "
                        "JOIN nodes s ON e.source_qualified = s.qualified_name "
                        "JOIN nodes t ON e.target_qualified = t.qualified_name "
                        "WHERE e.kind = 'CALLS' AND s.kind != 'File' AND t.kind != 'File'"
                    )
                    cur = graph_conn.execute(sql_edges)
                    links = [{"source": r[0], "target": r[1], "type": r[2]} for r in cur.fetchall()]
                except Exception as ex:
                    links = []
                    graph_conn.close()

                self._json({"nodes": nodes, "links": links})
                return

                self._json({"nodes": nodes, "links": links})
                return

            # API: tree structure (file → functions/classes grouped by directory)
            if path == "/api/tree":
                cur = conn.execute(
                    "SELECT n.id, n.kind, n.name, n.file_path, n.line_start, n.line_end, "
                    "n.parent_name, n.community_id, c.name as community_name, n.signature "
                    "FROM nodes n LEFT JOIN communities c ON n.community_id = c.id "
                    "WHERE n.kind IN ('Function', 'Class', 'Test') "
                    "ORDER BY n.file_path, n.line_start"
                )
                rows = [node_to_dict(r) for r in cur.fetchall()]

                # Group: dir → file → nodes
                tree = {}
                for r in rows:
                    rp = r.get("rel_path", "")
                    if not rp:
                        continue
                    parts = rp.split("/")
                    if len(parts) >= 2:
                        project = parts[0]
                        file_dir = "/".join(parts[:-1])
                        file_name = parts[-1]
                    else:
                        project = "root"
                        file_dir = ""
                        file_name = parts[0] if parts else ""

                    if project not in tree:
                        tree[project] = {}
                    if file_dir not in tree[project]:
                        tree[project][file_dir] = {}
                    if file_name not in tree[project][file_dir]:
                        tree[project][file_dir][file_name] = []
                    tree[project][file_dir][file_name].append({
                        "id": r["id"],
                        "name": r["name"],
                        "kind": r["kind"],
                        "line_start": r.get("line_start"),
                        "line_end": r.get("line_end"),
                        "parent_name": r.get("parent_name"),
                        "community_id": r.get("community_id"),
                        "community_name": r.get("community_name"),
                        "signature": r.get("signature"),
                        "rel_path": r.get("rel_path"),
                    })

                self._json(tree)
                return

            self._json({"error": "not found"}, 404)

        finally:
            conn.close()


if __name__ == "__main__":
    # Pre-flight check
    import sqlite3 as _sq
    _c = _sq.connect(DB_PATH)
    _r = _c.execute("SELECT COUNT(*) FROM edges e JOIN nodes s ON e.source_qualified = s.qualified_name JOIN nodes t ON e.target_qualified = t.qualified_name WHERE e.kind = 'CALLS'").fetchone()
    print(f"Pre-flight: {os.path.abspath(DB_PATH)} has {_r[0]} CALLS edges with matching nodes")
    _c.close()

    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Code Graph Viewer running at http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
