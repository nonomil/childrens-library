# Claude Code + Codex 协作框架

> 一个轻量级 AI 编码 Harness，用 Markdown + Python 脚本构建，零外部依赖。

## 这是什么

本项目是一个 **AI 辅助开发的工程化框架**，基于 Claude Code（CC）+ Codex MCP 的双模型协作模式：

- **CC = 大脑**：规划、搜索、决策、代码审查
- **Codex = 双手**：代码生成、重构、Bug 修复

核心思想来自 Harness Engineering（工具链工程）：通过工程手段配置 AI 行为环境，而非单纯依赖提示词。

## 架构概览

```
CLAUDE.md（路由入口）
├── .claude/rules/          ← 自动加载的门禁规则
│   ├── gate.md               强制需求讨论流程
│   ├── project.md            项目架构约束
│   └── workflows.md          开发循环规范
├── .claude/workflows/      ← 按需加载的场景工作流
│   ├── claude-workflow-constants.md    全局常量与参数
│   ├── claude-workflow-debug.md        调试流程
│   ├── claude-workflow-review.md       代码审查
│   ├── claude-workflow-parallel.md     并行开发
│   ├── claude-workflow-complex.md      复杂任务
│   └── ...more
├── .claude/scripts/        ← Hook 自动化脚本
│   ├── auto_checkpoint_commit.py       提交检查点
│   ├── append_changelog_draft.py       Changelog 自动生成
│   └── block_delete.py                 删除防护
├── .claude/preferences.json ← 用户偏好配置
├── .claude/memory/          ← 跨会话记忆系统
│   ├── lessons/            历史教训
│   ├── context/            AI 上下文文档
│   └── ...
└── image-merger/            ← 示例应用（Python 图片合并）
```

## 核心特性

### 1. 渐进式加载

不一次性加载所有配置。CLAUDE.md 作为路由表，根据场景按需加载对应工作流文档。ETH Zurich 研究证实：**冗长的指令文件反而降低 AI 输出质量**。

### 2. 门禁流程

任何代码改动前必须经过需求讨论 → 复述确认 → 用户确认，防止 AI 自行其是。

### 3. 用户偏好系统

通过 `.claude/preferences.json` 一键控制行为：

| 偏好 | 选项 | 说明 |
|------|------|------|
| **profile** | `standard` / `minimal` | minimal = 关闭所有自动化，纯对话 |
| **git_strategy** | `auto_commit` / `ask` / `skip` | 提交行为 |
| **codex_invocation** | `cc_auto_decides` / `always` / `ask` / `skip` | Codex 调用策略 |
| **review_strategy** | `cc_only` / `auto_gate` / `codex_required` | 审查策略 |

### 4. 安全防护

- Hook 脚本拦截危险操作（删除文件、force push 等）
- diff ≤ 200 行硬约束，超过必须拆分
- 高风险文件（API 签名、数据库 schema、安全模块）命中即升级复杂模式

### 5. 跨会话记忆

每次任务的经验教训写入 `.claude/memory/lessons/`，下次任务自动读取规避。支持 FBM 语义检索。

## 与重型 Harness 框架的对比

| 维度 | 本项目 | 重型框架（HumanLayer 等） |
|------|--------|--------------------------|
| **配置量** | ~800 行 Markdown | 数千行 YAML/JSON |
| **依赖** | 零（纯 Markdown + Python） | 多个 npm/pip 包 |
| **启动** | 5 分钟 | 1-2 小时 |
| **灵活性** | preferences.json 一键切换 | 修改多处配置 |
| **适用** | 个人 / 小团队 | 企业 / CI |

本项目已覆盖 Harness Engineering 11 个核心维度中的 7 个，剩余 3 个（back-pressure hook、独立 evaluator、context reset）可在 2 小时内补齐。详见 [harness-research-analysis.md](docs/项目介绍与对比Harness工程/harness-research-analysis.md)。

## 快速开始

### 前置条件

- Claude Code CLI
- Codex MCP 服务
- Python 3.10+

### 使用方式

1. 将本项目作为模板复制到你的项目根目录
2. 修改 `CLAUDE.md` 中的项目特定信息
3. 根据需要调整 `.claude/preferences.json`
4. 开始使用 Claude Code — 框架会自动加载

### 初始化偏好

在 Claude Code 对话中输入"初始化偏好"，会交互式引导你配置 3 个偏好维度。

## 示例应用

`image-merger/` 目录包含一个 Python 图片合并工具，作为框架使用的演示：

- **技术栈**：Python 3.10+ / Pillow / tkinter / SQLite
- **入口**：`image-merger/src/main.py`（CLI）、`image-merger/src/gui.py`（GUI）
- **功能**：图片合并、批量处理、自然排序文件扫描

## 文档索引

| 文档 | 说明 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 路由入口，项目级指令 |
| [Harness 调研分析](docs/项目介绍与对比Harness工程/harness-research-analysis.md) | 与重型框架的详细对比 |
| [框架快速上手指南](docs/Claude%20Code%20框架快速上手指南.md) | 使用教程 |
| [Guide 页面](docs/guide/) | 详细功能说明 |
| [Changelog](docs/changes/) | 变更记录 |

## 设计哲学

> "Bad programmers worry about the code. Good programmers worry about data structures." — Linus Torvalds

- **简单优于复杂**：能 3 行解决的不写 10 行
- **实用优于完美**：90 分的功能 > 0 分的完美设计
- **向后兼容**：任何改动不能破坏现有工作流
- **渐进式**：先跑通再优化，三轮迭代（可用 → 质量 → 打磨）

## License

MIT
