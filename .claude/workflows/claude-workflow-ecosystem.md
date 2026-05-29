# claude-workflow-ecosystem.md — 工具生态与可选增强

> 本文档只在“安装什么插件 / Skill / Hook 更合适”这类场景按需加载，不作为所有 workflow 的默认常驻上下文。

---

## 1. 多模型工具角色矩阵

| 工具 | 角色 | 擅长 | 何时用 |
|------|------|------|--------|
| Antigravity + Opus + Plan Mode | 需求分析师 + 架构师 | 深度需求澄清、架构决策、发现歧义 | 最初 Plan 生成 |
| Claude Code (CC) + Plan Mode | 日常规划者 | 单任务分析、文件搜索、改动预览 | 日常开发每个任务前 |
| Codex (gpt-5.4) | 高级工程师 | 计划落地、代码生成、长时间连续执行 | 代码生成、工程审查、自动化执行 |
| Claude Sonnet (Kiro/Antigravity) | 快速编码 | 中等复杂度任务、快速迭代 | 并行开发支线 |
| Trae + gpt-5.4 | 省 Token 编码 | 简单任务、成本敏感场景 | 并行开发支线 |

---

## 2. Skills 生态

### 2.1 Skill 目录结构

每个 skill 是一个目录，核心入口是 `SKILL.md`，可包含脚本、模板、示例。

```text
.claude/skills/
└── my-skill/
    ├── SKILL.md
    ├── templates/
    ├── examples/
    └── scripts/
```

Codex 侧镜像目录：

```text
.codex/skills/
```

### 2.2 激活机制

- 启动时只加载 skill 的名称和描述
- 只有判断匹配当前任务时才加载完整内容
- 多个 skill 可同时激活组合使用

### 2.3 安装方式

| 方式 | 命令示例 | 特点 |
|------|---------|------|
| `/plugin`（推荐） | `/plugin add owner/marketplace` | Claude Code 内安装，重启生效 |
| `npx skills` | `npx skills add owner/repo --skill name -a claude-code -g` | 跨 agent 通用，支持 `update` / `list` |
| `npx add-skill` | `npx add-skill owner/repo --skill name` | 轻量、零额外依赖 |

### 2.4 superpowers 建议

优先考虑这些高价值 skill：
- `superpowers:brainstorming`
- `superpowers:writing-plans`
- `superpowers:dispatching-parallel-agents`
- `superpowers:requesting-code-review`
- `superpowers:verification-before-completion`

---

## 3. Cartographer / 安全防护增强

### 3.1 Cartographer

- vendored marketplace 只是分发方式，不等于“自动识别”
- 必须在 `.claude/settings.json` 中显式声明：
  - `extraKnownMarketplaces`
  - `enabledPlugins`
- 模板默认策略：官方插件优先，`extract` 回退
- 建议先跑：

```bash
python .claude/scripts/cartographer_smoke.py \
  --write-report docs/scan/cartographer-smoke-report.md
```

- 若要做真实端到端验证，再配合 `.claude/templates/cartographer-e2e-checklist.md`

### 3.2 安全防护工具

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| `dcg` | Rust 实现，AST 级危险命令识别 | 强安全拦截 |
| `claude-code-damage-control` | Python/YAML，可自定义 patterns | 规则定制 |
| `claudekit` | 自动 checkpoint + 质量 hooks | 会话收口 |
| GitButler | 并行 worktree / virtual branches | 重并行协作 |

---

## 4. Hooks 配置合并规则

| 文件位置 | 生效范围 | 是否提交 git |
|---------|---------|-------------|
| `~/.claude/settings.json` | 全局，所有项目 | 否 |
| `.claude/settings.json` | 当前项目，共享 | 是 |
| `.claude/settings.local.json` | 当前项目，本机覆写 | 否 |

规则：
- 同类 hook 会合并执行
- 安全防护建议放全局
- 项目质量检查放项目级

---

## 5. 推荐叠加顺序

### 最小配置

1. 项目级 `.claude/settings.json`
2. Gate / git safety / merge scope hooks
3. Cartographer 插件或 `extract` 回退

### 进阶叠加

- 可定制安全 patterns：`claude-code-damage-control`
- 自动 checkpoint：`claudekit`
- TDD / 调试 / 规划标准化：`superpowers`
- 多 worktree / merge queue：GitButler、CODEOWNERS、外部协调层

---

## 版本历史

- 2026-02-27：从 constants 拆出工具生态和安全防护扩展
- 2026-04-07：补充 Cartographer“必须显式启用，不会因 vendored 自动识别”的说明
