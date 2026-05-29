# -*- coding: utf-8 -*-
"""Generate viewer_data.js from Graphify graph.json.

Outputs a JS file that sets global variables for viewer_template.html.
Usage:
    python generate_viewer.py [--input graph.json] [--output viewer_data.js]
"""
import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

COMMUNITY_COLORS = [
    "#89b4fa", "#a6e3a1", "#cba6f7", "#f9e2af", "#f38ba8",
    "#94e2d5", "#fab387", "#74c7ec", "#f5c2e7", "#b4befe",
    "#a6adc8", "#f2cdcd", "#89dceb", "#8bd5ca", "#dbc4d8",
    "#cdd6f4", "#eba0ac", "#f5e0dc", "#96cdfb", "#b4befe",
    "#cba6f7", "#f9e2af", "#a6e3a1", "#89b4fa", "#f38ba8",
    "#94e2d5",
]


def load_graph(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_path(p: str) -> str:
    if not p:
        return ""
    return p.replace("\\", "/")


def make_rel_path(abs_path: str) -> str:
    try:
        rel = str(Path(abs_path).resolve().relative_to(REPO_ROOT))
        return rel.replace("\\", "/")
    except (ValueError, TypeError):
        return normalize_path(abs_path)


def parse_line(loc: str) -> int:
    if not loc:
        return 1
    digits = "".join(ch for ch in str(loc) if ch.isdigit())
    if not digits:
        return 1
    return max(1, int(digits))


def build_vscode_uri(file_path: str, line: int) -> str:
    normalized_path = normalize_path(file_path)
    encoded_path = quote(normalized_path, safe="/:")
    return f"vscode://file/{encoded_path}:{line}"


def build_nested_tree(nodes: list[dict]) -> dict:
    """Build nested tree: {_children: {name: ...}, _files: {name: [ids]}}."""
    root: dict = {"_children": {}, "_files": {}}
    for n in nodes:
        sf = n.get("source_file", "")
        if not sf:
            continue
        rel = make_rel_path(sf)
        parts = rel.split("/")
        current = root
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # filename
                current["_files"].setdefault(part, []).append(n["id"])
            else:
                # directory
                if part not in current["_children"]:
                    current["_children"][part] = {"_children": {}, "_files": {}}
                current = current["_children"][part]
    return root


def build_node_lookup(nodes: list[dict]) -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for n in nodes:
        lookup[n["id"]] = n
    return lookup


def build_edge_index(links: list[dict]) -> tuple[dict, dict]:
    out_edges: dict[str, list] = {}
    in_edges: dict[str, list] = {}
    for e in links:
        src, tgt = e.get("source", ""), e.get("target", "")
        if src:
            out_edges.setdefault(src, []).append(e)
        if tgt:
            in_edges.setdefault(tgt, []).append(e)
    return out_edges, in_edges


def prepare_vis_data(nodes: list[dict], links: list[dict]) -> tuple[list, list, dict]:
    conn_count: dict[str, int] = {}
    for e in links:
        for key in ("source", "target"):
            nid = e.get(key, "")
            conn_count[nid] = conn_count.get(nid, 0) + 1

    vis_nodes = []
    community_map: dict[int, dict] = {}

    for n in nodes:
        nid = n["id"]
        comm = n.get("community", 0) or 0
        color = COMMUNITY_COLORS[comm % len(COMMUNITY_COLORS)]
        count = conn_count.get(nid, 0)
        size = min(30, max(8, 8 + count * 1.5))

        vis_nodes.append({
            "id": nid, "label": n.get("label", nid),
            "color": color, "size": size, "community": comm,
        })

        if comm not in community_map:
            community_map[comm] = {"color": color, "count": 0, "node_ids": []}
        community_map[comm]["count"] += 1
        community_map[comm]["node_ids"].append(nid)

    vis_edges = []
    for e in links:
        src, tgt = e.get("source", ""), e.get("target", "")
        if not src or not tgt:
            continue
        vis_edges.append({
            "from": src, "to": tgt,
            "relation": e.get("relation", ""),
            "confidence": e.get("confidence", "EXTRACTED"),
            "confidence_score": e.get("confidence_score", 1.0),
        })

    return vis_nodes, vis_edges, community_map


def build_targets_and_paths(node_lookup: dict) -> tuple[dict, dict, dict]:
    targets: dict[str, dict] = {}
    uris: dict[str, str] = {}
    rel_paths: dict[str, str] = {}
    for nid, n in node_lookup.items():
        sf = n.get("source_file", "")
        if sf:
            line = parse_line(n.get("source_location", ""))
            fp = normalize_path(sf)
            rel_path = make_rel_path(sf)
            targets[nid] = {
                "path": fp,
                "line": line,
                "relPath": rel_path,
            }
            uris[nid] = build_vscode_uri(fp, line)
            rel_paths[nid] = rel_path
    return targets, uris, rel_paths


def find_latest_graph_json(repo_root: Path) -> str:
    """自动扫描 docs/代码库-知识图谱/*-LLM图谱/graph.json，返回最新的一个。"""
    base = repo_root / "docs" / "代码库-知识图谱"
    if base.is_dir():
        candidates = sorted(base.glob("*-LLM图谱/graph.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if candidates:
            return str(candidates[0])
    # Fallback: 旧目录
    for fallback in ["graphify-out/graph.json"]:
        fp = repo_root / fallback
        if fp.is_file():
            return str(fp)
    return str(base / "graph.json")


def main():
    default_input = find_latest_graph_json(REPO_ROOT)
    default_output = str(Path(__file__).resolve().parent / "viewer_data.js")

    input_path = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_path = sys.argv[2] if len(sys.argv) > 2 else default_output

    print(f"Reading: {input_path}")
    graph = load_graph(input_path)
    nodes = graph.get("nodes", [])
    links = graph.get("links", [])
    print(f"Parsing {len(nodes)} nodes, {len(links)} edges...")

    tree = build_nested_tree(nodes)
    node_lookup = build_node_lookup(nodes)
    out_edges, in_edges = build_edge_index(links)
    vis_nodes, vis_edges, community_map = prepare_vis_data(nodes, links)
    targets, uris, rel_paths = build_targets_and_paths(node_lookup)

    communities = set(n.get("community") for n in nodes if n.get("community") is not None)
    extracted = sum(1 for e in links if e.get("confidence") == "EXTRACTED")
    inferred = sum(1 for e in links if e.get("confidence") == "INFERRED")
    stats = {
        "node_count": len(nodes), "edge_count": len(links),
        "community_count": len(communities),
        "extracted_count": extracted, "inferred_count": inferred,
    }
    print(f"Stats: {stats}")

    # Write viewer_data.js — a single JS file that sets global variables
    data = {
        "TREE": tree,
        "NODES": node_lookup,
        "OUT": out_edges,
        "IN": in_edges,
        "TARGETS": targets,
        "URIS": uris,
        "RELS": rel_paths,
        "STATS": stats,
        "VNODES": vis_nodes,
        "VEDGES": vis_edges,
        "COMMS": community_map,
    }

    js_lines = []
    for key, value in data.items():
        json_str = json.dumps(value, ensure_ascii=False)
        js_lines.append(f"const {key} = {json_str};")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(js_lines))

    size_kb = os.path.getsize(output_path) // 1024
    print(f"Generated: {output_path} ({size_kb} KB)")
    print(f"Now open viewer_template.html in browser (via HTTP server)")


if __name__ == "__main__":
    main()
