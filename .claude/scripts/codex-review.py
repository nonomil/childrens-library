#!/usr/bin/env python3
"""codex-review.py — Windows-compatible Codex review wrapper

Background: /codex:review has disable-model-invocation: true,
          AI cannot invoke via Skill tool. This script calls codex-companion.mjs directly.

Usage:
  python .claude/scripts/codex-review.py              # normal review
  python .claude/scripts/codex-review.py adversarial  # adversarial review
"""

from __future__ import annotations

import glob
import os
import subprocess
import sys

REVIEW_MODE = sys.argv[1] if len(sys.argv) > 1 else "review"

# ── 1. Locate Codex plugin scripts directory ──
plugin_candidates = [
    os.path.expanduser("~/.claude/plugins/cache/openai-codex/codex"),
    "C:/Users/Administrator/.claude/plugins/cache/openai-codex/codex",
]

plugin_base = None
for path in plugin_candidates:
    if os.path.isdir(path):
        plugin_base = path
        break

if not plugin_base:
    print("[ERROR] Codex plugin dir not found. Tried:", file=sys.stderr)
    for p in plugin_candidates:
        print(f"  {p}", file=sys.stderr)
    print("[FALLBACK] Use MCP path B (mcp__codex__codex)", file=sys.stderr)
    sys.exit(1)

# Find latest version directory
scripts_dirs = sorted(glob.glob(os.path.join(plugin_base, "*", "scripts")))
if not scripts_dirs:
    print("[ERROR] codex-companion.mjs not found in any version dir", file=sys.stderr)
    print("[FALLBACK] Use MCP path B (mcp__codex__codex)", file=sys.stderr)
    sys.exit(1)

companion = os.path.join(scripts_dirs[-1], "codex-companion.mjs")
if not os.path.isfile(companion):
    print(f"[ERROR] Script not found: {companion}", file=sys.stderr)
    print("[FALLBACK] Use MCP path B (mcp__codex__codex)", file=sys.stderr)
    sys.exit(1)

# ── 2. Execute review ──
print(f"[codex-review] Script: {companion}")
print(f"[codex-review] Mode: {REVIEW_MODE}")

if REVIEW_MODE == "adversarial":
    cmd = ["node", companion, "review", "--adversarial", "--wait"]
else:
    cmd = ["node", companion, "review", "--wait"]

result = subprocess.run(
    cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
)

# ── 3. Output result ──
if result.stdout:
    print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)

# ── 4. Exit with same code ──
sys.exit(result.returncode)
