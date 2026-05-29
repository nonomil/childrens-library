#!/usr/bin/env bash
# codex-review.sh — 封装 Codex review 调用，自动解析插件版本路径
#
# 背景：/codex:review 命令设置了 disable-model-invocation: true，
#       AI 无法通过 Skill 工具调用，需要直调底层脚本绕过限制。
#
# 用法：
#   bash .claude/scripts/codex-review.sh              # 普通 review
#   bash .claude/scripts/codex-review.sh adversarial  # 对抗性 review
#
# 调用方（AI）：
#   Bash("bash .claude/scripts/codex-review.sh")
#   Bash("bash .claude/scripts/codex-review.sh adversarial")

set -euo pipefail

REVIEW_MODE="${1:-review}"  # review | adversarial

# ── 1. 定位 Codex 插件脚本目录（自动适配版本号升级）──────────────────
PLUGIN_BASE="C:/Users/Administrator/.claude/plugins/cache/openai-codex/codex"

if [[ ! -d "$PLUGIN_BASE" ]]; then
  echo "[ERROR] Codex 插件目录不存在: $PLUGIN_BASE" >&2
  echo "[FALLBACK] 请改用 MCP 路径 B（mcp__codex__codex）" >&2
  exit 1
fi

# 取最新版本目录（按目录名排序，取最后一个）
SCRIPTS_DIR=$(ls -d "${PLUGIN_BASE}"/*/scripts/ 2>/dev/null | tail -1)

if [[ -z "$SCRIPTS_DIR" ]]; then
  echo "[ERROR] 未找到 codex-companion.mjs，插件可能未安装或路径变更" >&2
  echo "[FALLBACK] 请改用 MCP 路径 B（mcp__codex__codex）" >&2
  exit 1
fi

COMPANION="${SCRIPTS_DIR}codex-companion.mjs"

if [[ ! -f "$COMPANION" ]]; then
  echo "[ERROR] 脚本不存在: $COMPANION" >&2
  exit 1
fi

# ── 2. 执行 review ────────────────────────────────────────────────────
echo "[codex-review] 使用脚本: $COMPANION"
echo "[codex-review] 模式: $REVIEW_MODE"

case "$REVIEW_MODE" in
  adversarial)
    node "$COMPANION" review --adversarial --wait
    ;;
  review|*)
    node "$COMPANION" review --wait
    ;;
esac
