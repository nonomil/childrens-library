# 工具安装速查

## 必装

### Claude Code (CC)

```bash
npm install -g @anthropic-ai/claude-code
claude --version
claude auth login
```

## 可选工具

### Codex CLI (CX) — 代码审查 + 任务救援

```bash
# 安装
npm install -g @openai/codex
codex login

# MCP 方式接入 CC
claude mcp add codex -s user -- codex mcp-server

# 插件方式接入 CC
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup

# 使用
/codex:review              # 标准审查（只读）
/codex:adversarial-review   # 对抗性审查
/codex:rescue              # 任务救援
```

### Trellis — 项目管理（PLAN.md + tasks/ 的替代方案）

```bash
npm install -g @mindfoldhq/trellis@latest
trellis init --claude-code --codex -u yourname

# 目录结构
# .trellis/
# ├── spec/          # 项目规范
# ├── tasks/         # 任务 PRD
# ├── workspace/     # Journal + 决策记录
# └── workflow.md
```

### autoresearch — 自动研究循环

```bash
# karpathy/autoresearch（基础 ML 优化循环）
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch && uv sync

# 或使用 Claude skill 版本
# 参考 .claude/skills/autoresearch/（如已安装）
```

### grill-me — 已内置

grill-me 原则已集成到门禁系统（gate.md）：
- 先查代码再问人
- 每次追问附带推荐答案
