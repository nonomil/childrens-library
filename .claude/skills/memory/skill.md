---
name: memory
description: 跨会话记忆系统（主记忆）。用 CC 原生工具（Read/Write/Grep）管理 Markdown 记忆文件。在需要回忆历史决策、查找过往经验时触发。
layer: always
tags: [memory, context, recall]
domain: memory
---

# 记忆技能（CC 原生工具版）

## 架构

```
.claude/memory/                ← 记忆根目录（Markdown 文件，进 git，团队共享）
├── lessons/                        ← 踩坑经验（按主题拆分）
│   ├── codex.md                        Codex 调用经验
│   └── workflow.md                     工作流教训
├── context/                        ← Changelog AI 轨（与 docs/changes/ 同名）
│   └── 序号-日期-hash-标题.md           结构化变更记忆
├── decisions/                      ← 架构决策
├── constraints/                    ← 项目约束发现
├── patterns/                       ← 可复用实现模式
├── prompts/                        ← 成功 Prompt 模板
├── user-prefs.md                   ← 用户偏好
├── debug-history.md                ← Bug 根因记录（按需创建）
├── architecture-decisions.md       ← 架构决策摘要（按需创建）
└── [按需创建].md                   ← 其他主题
```

**三层架构定位**：
- Layer 1 个人层：`~/.claude/projects/<hash>/MEMORY.md`（个人行为约束，不进 git）
- **Layer 2 项目记忆**：`.claude/memory/`（本目录，CC 自动读写，团队共享）
- Layer 3 规范层：`.claude/rules/`（人工维护，CC 不自动修改）

**无外部依赖**：不用 MCP 服务器，不用 LLM API，CC 直接用 Read/Write/Grep 操作。

## 操作方式

### 搜索记忆

用 Grep 搜索关键词，CC 自己判断相关性（比向量检索更智能）：

```
Grep({ pattern: "[关键词]", path: ".claude/memory/" })
```

找到文件后用 Read 读取内容，CC 理解语义后提取相关信息。

### 写入记忆

直接用 Write/Edit 追加到对应主题文件：

```markdown
## [标题]

- **日期**: YYYY-MM-DD
- **场景**: [什么情况下发生的]
- **内容**: [详细描述]
- **教训**: [下次怎么避免/复用]

---
```

### 查看记忆状态

用 Glob 列出所有记忆文件，用 Read 抽样查看内容。

## 触发时机（自动，无需用户指令）

### 必须触发

1. **新任务开始时**（门禁 Step 4.5）— Grep 搜索相关记忆
   - 搜索关键词：当前任务的核心概念
   - 目的：避免重复犯错，复用过往方案

2. **Bug 修复完成后**（debug workflow Phase 5）— 追加到 `debug-history.md`
   - 格式：`## Bug修复: [描述]` + 根因 + 方案 + 预防

3. **任务完成收尾时** — 追加到对应主题文件
   - 关键决策 → `architecture-decisions.md`
   - Codex 经验 → `codex-lessons.md`
   - 其他 → 自动创建新文件

### 建议触发

4. **用户提到"之前/上次/历史"** — 立即搜索记忆，不凭记忆回答
5. **用户纠正 AI 错误时** — 写入记忆（写入 `.claude/memory/lessons/`（对应主题文件））

## 自动触发模式（Trigger-Based Activation）

> 基于用户输入模式自动激活记忆检索，无需显式指令。

### 触发词 → 动作映射

| 触发模式 | 示例 | 自动动作 | 搜索范围 |
|----------|------|---------|---------|
| 历史引用 | "之前"、"上次"、"之前那个"、"以前" | 搜索记忆后再回答，**禁止凭对话记忆回答** | `.claude/memory/` 全域 |
| 经验回忆 | "记得"、"历史"、"经验"、"教训"、"遇到过" | 全量记忆召回（Grep 多关键词） | `.claude/memory/` 全域 + `critical-lessons.md` |
| 新任务开始 | 门禁 Step 4.5 | 搜索当前任务核心概念的教训 | `.claude/memory/lessons/` 优先 |
| Bug/错误出现 | 错误信息、traceback、test failure | 搜索 `debug-history.md` + `lessons/` | `debug-history.md`, `lessons/` |
| 偏好相关 | "我不喜欢"、"帮我设置"、"你之前怎么做的" | 读取 `user-prefs.md` | `user-prefs.md` |
| 架构决策 | "为什么这样设计"、"当时的方案" | 搜索 `architecture-decisions.md` + `decisions/` | `decisions/`, `context/` |

### 实现方式

触发时不直接回答，先执行 Grep 搜索：

```
// 伪代码
if (用户输入 matches /之前|上次|以前|历史/) {
  Grep({ pattern: extract_keywords(用户输入), path: ".claude/memory/" })
  → 如果找到相关条目：引用并标注来源文件
  → 如果未找到：明确说明"未找到历史记录"，不编造
}
```

**硬约束**：触发后必须先输出搜索结果摘要，再回答用户问题。禁止跳过搜索直接回答。

### 记忆文件归档约定

| 文件名 | 用途 |
|--------|------|
| `debug-history.md` | Bug 根因记录 |
| `architecture-decisions.md` | 架构决策和原因 |
| `codex-lessons.md` | Codex 调用的经验教训 |
| `performance-tuning.md` | 性能优化记录 |
| `integration-notes.md` | 第三方工具集成经验 |
| `[按需创建].md` | 其他主题，按 title 自动命名 |

## 记忆生命周期

> 简化版：不追踪 uses/last_ref 元数据。通过 index.md 的“最后更新”列和人工审计管理记忆时效性。

### 时效性判断
- 检查 index.md 的“最后更新”列，超过 60 天未更新的条目在审计时标记为 
- 超过 90 天且未被引用的条目在审计时建议清理

### 审计触发
- 用户说“审计记忆”/“清理记忆”
- index.md 总条目 ≥ 50 或单文件 ≥ 300 行时主动提醒

## 审计机制

### 触发时机

- 用户说"审计记忆" / "清理记忆"
- 每月一次（由 CC 在对话开头检查记忆目录创建日期时提醒）

### 审计步骤

1. **Glob** 列出 `.claude/memory/` 下所有文件
2. **Read** 每个文件，检查：
   - 超过 3 个月的低置信度条目（可删除）
   - 互相矛盾的条目（需标注）
   - 明显过时的内容（如已不存在的文件路径、已解决的环境问题）
3. 输出建议列表，**等待用户确认后再修改**
4. 绝不自动删除任何条目

## 优先级分层（Priority Tiers）

> 记忆按重要性分三层加载，避免无关记忆消耗 context 窗口。

### 分层定义

| 优先级 | 名称 | 目录/文件 | 加载时机 | 加载方式 |
|--------|------|----------|---------|---------|
| **P0** | 始终加载 | `critical-lessons.md`（已硬加载到 rules/） | 每次会话自动 | 系统自动注入，无需操作 |
| **P1** | 任务相关 | `lessons/`, `decisions/`, `constraints/` | 新任务开始时 | Grep 搜索任务关键词，仅读取匹配条目 |
| **P2** | 背景参考 | `patterns/`, `context/`, `prompts/` | 用户明确要求时 | 用户说"查看模式/历史上下文/prompt"才读取 |

### 加载策略

**P0 — 始终加载（零成本）**
- `critical-lessons.md` 已在 `.claude/rules/` 中，每次会话自动注入到 system prompt
- CC 无需额外操作，这些教训自动生效

**P1 — 任务相关（按需搜索）**
- 新任务开始（门禁 Step 4.5）时：
  1. 提取当前任务的核心概念关键词（2-3 个）
  2. `Grep({ pattern: "关键词1|关键词2", path: ".claude/memory/lessons/" })`
  3. `Grep({ pattern: "关键词1|关键词2", path: ".claude/memory/decisions/" })`
  4. 仅 Read 匹配到的文件，不盲目全读
- Bug 修复时额外搜索 `constraints/`

**P2 — 背景参考（显式触发）**
- 仅在以下情况搜索 P2 目录：
  - 用户说"查看历史模式"/"查看过往方案"/"有什么可复用的"
  - 用户提到具体文件名或路径（如"之前 patterns/ 里那个..."）
  - 审计记忆时（全量读取）
- 不在常规任务中自动搜索 P2，节省 context 窗口

### 优先级与触发模式的配合

```
新任务开始 → P0(自动) + P1(关键词搜索) → 足够
用户说"之前/上次" → P1 + P2 全域搜索 → 找到后回答
用户说"记得/经验" → P0 + P1 + P2 全量 → 完整回忆
日常对话 → P0(自动) → 不额外加载
```

## 体积控制

写入前检查目标文件行数（Read 后数行）：

- **< 300 行**：正常追加
- **≥ 300 行**：列出最旧的 3 条低置信度条目，提示用户确认是否清理后再追加
- **≥ 500 行**：强烈建议拆分文件（按子主题拆为多个文件）

## 用户偏好

用户偏好记忆存放于 `.claude/memory/user-prefs.md`，由 CC 在对话中自动积累：
- 沟通风格偏好
- 技术偏好
- 工作习惯
- 安全红线

每次发现新偏好时追加，开头注明最后更新日期。

## 初始化

首次使用时，确保目录存在：
```bash
mkdir -p .claude/memory/decisions .claude/memory/constraints .claude/memory/patterns .claude/memory/lessons .claude/memory/context .claude/memory/prompts
```
