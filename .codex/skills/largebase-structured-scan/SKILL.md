---
name: largebase-structured-scan
description: Use when 需要先对大型代码库或多参考文档项目做结构化扫描，再进入规划或开发阶段。触发信号：递归代码文件数较多、Markdown/参考文档较多、跨3个及以上模块、重构/迁移/整合、命中"先扫描、影响分析"等关键词、或用户显式要求先扫描。
---

# largebase-structured-scan

## Overview

先扫描、后开发。统一产出 `00-06` 扫描包 + 可选 `scan-data.json` + `scan.db`，
让后续流程基于结构化数据而不是全库盲搜。

---

## 模式选择

| 模式 | 使用时机 | 必须产物 |
|------|---------|---------| 
| M1 | 新功能接入，摸清目录与入口 | 00, 01, 06 |
| M2 | 涉及存储/索引/转换/同步 | 00, 01, 02, 05, 06 |
| M3 | 公共函数签名或模块契约变更 | 00, 01, 03, 05, 06 |
| M4 | 大规模重构或迁移 | 全部 00-06 + scan-data.json + scan.db |

---

## Workflow

**连续执行规则**：步骤之间无需用户确认，必须连续执行，仅在 Step 0 提示和硬门禁失败时停下。

---

### Step 0：可选增强 — Cartographer 检测

> 此步骤为**可选增强**，不阻塞扫描流程。

1. 检查 `docs/CODEBASE_MAP.md` 是否存在且 `Generated at` ≤ 7 天
2. **若可用**：提示用户 `"检测到 CODEBASE_MAP.md 可用，将作为参考文档 --refs 传入"`，直接进入 Step 1
3. **若不可用**：提示用户选择：
   ```
   未检测到 CODEBASE_MAP.md，请选择：
     A) 使用本地 extract 命令生成（零 AI 成本，推荐）
     B) 运行 Cartographer 生成（需已安装，AI 级语义分析）
     C) 跳过，直接进入扫描
   ```
4. 选 A → Step 1 后自动执行 Step 1.5
5. 选 B → 尝试执行 Cartographer，成功则用其产物，失败则回退到 A
6. 选 C → 直接进入 Step 1

---

### Step 1：初始化扫描目录与数据库

```bash
python .claude/skills/largebase-structured-scan/scan.py scan \
  --mode M4 \
  --scope src docs references \
  --topic refactor-core \
  --refs docs/CODEBASE_MAP.md docs/api.md
```

**硬门禁**：输出必须包含 `[OK] 扫描初始化完成`，否则停止。

**约束**：`--scope` 禁止使用 `.` 作为全仓范围，必须显式列出业务目录。

---

### Step 1.5：本地结构预提取（推荐，零 AI Token）

```bash
python .claude/skills/largebase-structured-scan/scan.py extract \
  --scope src docs references \
  --topic refactor-core
```

增量模式（已有 scan.db 时跳过未变更文件）：

```bash
python .claude/skills/largebase-structured-scan/scan.py extract \
  --scope src docs references \
  --topic refactor-core \
  --incremental \
  --db docs/scan/YYYY-MM-DD-refactor-core/scan.db
```

产出：
- `extract-data.json`：模块/函数/导入关系（兼容 `load` 命令）
- `CODEBASE_MAP.md`：Markdown 格式导航地图
- `docs/CODEBASE_MAP.md`：全局副本

此步骤零 AI token，为 Step 2 提供结构化输入，减少 Codex 扫描时的探索开销。

---

### Step 2：生成扫描数据

**策略选择**：

> `extract` 完成后，提示用户选择执行策略：
>
> ```
> 请选择扫描执行策略：
>   A) Codex 扫描（默认）— 调用 Codex MCP 生成 scan-data.json + 00-06 报告
>   B) Claude Code 直接扫描 — CC 读取 extract-data.json 和 CODEBASE_MAP.md，自行生成全部产物（无 MCP 调用）
>   C) 跳过扫描 — 已有足够信息，跳过此步骤
> ```
>
> 用户确认后继续执行对应策略。若用户未明确选择，默认 A（Codex）。

#### 策略 A：单 Codex（默认）

1. 检查 `mcp__codex__codex` 工具是否可用
2. 调用 Codex，使用 `references/prompt-pack.md` 模板
3. 必填参数：`model: "gpt-5.4"`, `sandbox: "danger-full-access"`, `approval-policy: "on-failure"`
4. 若 Step 1.5 的 `extract-data.json` 存在，在 Prompt 中引用其模块清单和函数列表
5. 输出 `scan-data.json` 和 `00-06` 文档

**失败后** → 策略 B

#### 策略 B：CC 直接扫描

1. 读取 `extract-data.json`（或 `CODEBASE_MAP.md`）提取模块信息
2. 按模板逐个生成 `00-06` 文件
3. 基于 extract-data 生成 `scan-data.json`

#### 策略 C：并行多 Codex（模块数 ≥ 5，大型代码库加速）

按 `extract-data.json` 的模块清单拆分 scope，CC **同时**调起多个 Codex：

```text
模块清单：[src/core, src/api, src/ui, services/auth, services/payment, docs]
    ↓ CC 按模块拆分（每个 Codex 负责 1-2 个模块）
Codex-1: --scope src/core            → scan-data-core.json
Codex-2: --scope src/api src/ui      → scan-data-api.json
Codex-3: --scope services/auth ...  → scan-data-svc.json
Codex-4: --scope docs               → scan-data-docs.json
    ↓ 等待全部完成后：
scan.py merge --inputs scan-data-core.json scan-data-api.json scan-data-svc.json scan-data-docs.json \
              --output scan-data.json
```

**注意**：
- 策略 C 不要求 Codex 完全同时启动，CC 可以顺序触发；等全部完成后再 merge
- merge 命令自动去重（按 name+path+line 三键），重叠扫描不产生重复数据
- merge 后执行 `load` 写入 `scan.db`，流程与策略 A 完全相同

**硬门禁**（强制验证）：

```bash
python .claude/skills/largebase-structured-scan/scan.py verify \
  --dir docs/scan/YYYY-MM-DD-[topic] \
  --mode M4
```

退出码非 0 时：终止流程，输出 `[FAIL]` 信息，不得继续进入 Step 3。

**doc-gen 校验门禁**（Step 2 结束前必须执行）：

01-06 文档生成后，必须按 `doc-gen` skill 的校验清单逐项检查：

```
图表数量
[ ] 01 ≥ 3 张图（含 ≥1 SVG 分层架构图 + ≥1 SVG 文件树）
[ ] 02 ≥ 3 张图（含 ≥1 SVG 存储层图）
[ ] 03 ≥ 2 张图（含 ≥1 SVG API 分组卡片）
[ ] 04 ≥ 2 张图（含 ≥1 SVG 约束矩阵）
[ ] 05 ≥ 3 张图（含 ≥1 SVG 影响热力图）
[ ] 06 ≥ 3 张图（含 ≥1 SVG 四象限 + ≥1 SVG 条形图）

doc-gen 通用规则
[ ] 每份文档有标题 + 一句话说明（≤ 30 字）
[ ] 有目录
[ ] 有概览图节
[ ] Mermaid 节点 ID 不含中文
[ ] SVG 设了 viewBox，源码无空白行
[ ] 无完整函数体（> 15 行代码块）
[ ] 每段 ≤ 5 行
```

不通过则返工修改，不得进入 Step 3。详见 `.claude/skills/doc-gen/SKILL.md` 和 `references/doc-format-spec.md` §六。

---

### Step 3：Schema 校验 + 写入 SQLite

```bash
python .claude/skills/largebase-structured-scan/scan.py load \
  --load docs/scan/YYYY-MM-DD-refactor-core/scan-data.json \
  --db docs/scan/YYYY-MM-DD-refactor-core/scan.db
```

- `load` 会先校验 JSON schema，失败时输出缺失字段列表并终止
- 校验通过后写入所有表，`scan_meta` 写入 `load_validated=true`

---

### Step 4：查询扫描结果

**通用模糊搜索**：

```bash
python .claude/skills/largebase-structured-scan/scan.py query \
  --query <keyword> --type all \
  --db docs/scan/YYYY-MM-DD-refactor-core/scan.db
```

查询类型：`all` / `function` / `module` / `constraint` / `impact` / `dataflow`

**结构化查询模式**（`--query` 支持特殊值）：

```bash
# 影响分析：查某个路径下的公开函数 + 影响矩阵
python scan.py query --query impact --filter "file_manager" --db scan.db

# 调用链：查谁调用了某个函数
python scan.py query --query callers --filter "merge_images" --db scan.db

# 高风险点汇总（无需 --filter）
python scan.py query --query risks --db scan.db

# 模块依赖关系
python scan.py query --query module-deps --filter "merger" --db scan.db
```

通用参数：`--limit N`（结果条数上限，默认 20）

---

### Step 5：导出摘要到 CLAUDE.md（默认执行）

```bash
python .claude/skills/largebase-structured-scan/scan.py export-to-claude-md \
  --db docs/scan/YYYY-MM-DD-refactor-core/scan.db \
  --claude-md CLAUDE.md
```

- 将核心模块、关键约束和高风险影响点写入 CLAUDE.md 的标记区块
- 重复执行会覆盖同一标记块，不会追加重复内容
- **此步骤默认执行**，确保后续会话零成本获取扫描上下文

---

### Step 5.5：生成项目综述（M2/M4 推荐）

基于扫描产出的模块清单、架构图和数据流，使用 `doc-gen` skill 的 **explain** 模式生成项目综述文档。

```bash
# 输出到项目 docs/ 根目录
docs/project-overview.md
```

**生成规则**：

1. 读取 `01-architecture.md` 的模块清单和 `02-dataflow.md` 的数据流作为输入
2. 至少 2 张 Mermaid 图 + 1 张 SVG 图
3. 面向**首次接触项目的人类读者**，不假设任何前置知识
4. 重复执行覆盖同一文件

**⚠️ 质量硬约束**（不满足则返工）：

- 第一段必须用**大白话**说清"这个项目是什么、解决什么问题"（不出现技术术语）
- 每个核心概念必须用**类比或比喻**先给直觉理解，再给技术细节
- 必须有"快速上手"或"如何使用"节，告诉读者拿到项目后第一步做什么
- 必须有"为什么这样设计"节，解释关键设计决策的**动机**（不是描述设计本身）
- 目录结构节必须标注每个目录的**一句话用途**，不能只列路径
- **禁止**：纯技术参数罗列、无上下文的函数签名表、无解释的架构图

**结构模板**（严格按此顺序）：

```markdown
# [项目名] — 项目综述

> 一句话概括项目核心价值（≤ 30 字，人话）

## 这是什么？

[2-3 段大白话，回答：这个项目做什么？解决什么痛点？给谁用？]
[类比：用日常生活中的比喻解释项目的核心价值]

## 为什么需要它？

[描述没有这个项目时的痛点/问题，用场景讲故事]
[列出 3-5 个具体问题场景]

## 它怎么工作？（30 秒版）

[一张简化的架构/流程图]
[5-8 步的文字描述，每步一句话，说清楚数据/控制从哪来到哪去]

## 快速上手

### 前置条件
[需要什么环境、工具、知识]

### 5 分钟体验
[具体操作步骤：clone → 安装 → 运行 → 看到结果]
[每步都是可执行的命令或操作]

### 项目结构速览
[目录树 + 每个目录一句话用途]
[标注"核心"/"配置"/"文档"等分类]

## 核心概念（深入版）

[每个概念一节，格式：]
### [概念名]
- 一句话直觉解释（类比）
- 技术细节（1-2 段）
- 在项目中的具体体现（指向文件/模块）

## 关键设计决策

[表格：决策 | 选择了什么 | 为什么这样选 | 放弃了什么]
[至少 3 个设计决策]

## 常见场景指南

[3-5 个"我想做 X，应该看哪里/怎么做"的问答]
[每个场景指向具体的文件或工作流]

## 术语表

[只收录本文档中出现的术语]
[术语 | 日常解释 | 技术定义]
```

**与 01-architecture.md 的区别**：

- `01-architecture.md`：扫描产物，面向 AI/开发者，侧重模块依赖和文件结构
- `project-overview.md`：综述文档，面向人类，侧重"是什么、为什么、怎么用"

**与 README.md 的区别**：

- `README.md`：项目首页，侧重安装和快速启动（面向决定是否使用的人）
- `project-overview.md`：项目综述，侧重理解全貌（面向已经 clone 下来、想深入理解的人）

---

### Step 6：输出合同校验并路由

校验规则：`references/output-contract.md`

路由：
- 任务数 `=1` → `claude-workflow-complex.md`（可跳过其 Phase 0）
- 任务数 `>=2` → `claude-workflow-parallel.md`
- 缺陷修复主导 → `claude-workflow-debug.md`
- **lessons 联动**（可选但推荐）：扫描过程中发现的架构陷阱、文档冲突等经验写入 `.claude/memory/lessons/`

---

## Output Contract

```text
docs/scan/YYYY-MM-DD-[topic]/
├── 00-scan-meta.json           必须
├── 01-architecture.md          必须
├── 02-dataflow.md              M2/M4 必须
├── 03-api-surface.md           M3/M4 必须
├── 04-reference-constraints.md M2/M3/M4 必须
├── 05-impact-matrix.md         M2/M3/M4 必须
├── 06-exec-brief.md            必须
├── extract-data.json           本地提取（推荐）
├── scan-data.json              M4 必须，其他可选
├── scan.db                     M2/M3/M4 必须
└── project-overview.md         M2/M4 推荐（explain 模式综述）
```

---

## Guardrails

- 不执行业务代码，不修改源码文件
- 扫描结论必须能追溯到文件/函数/行号或文档来源
- 扫描后优先查询 `scan.db` 或 `extract-data.json`，避免重复全库搜索
- `load` 失败时不得跳过校验直接使用不完整数据
- `--scope` 禁止包含 `.git`、`node_modules`、`.venv`、`docs/scan` 等非业务目录
- **硬门禁**：Step 2 结束后必须运行 `verify` 子命令，退出码非 0 时不得继续
- **增量扫描**：已有 `scan.db` 时优先使用 `--incremental` 跳过未变更文件

---

## Document Format Specification

所有 01-06 扫描报告遵循通用 `doc-gen` skill 的排版规范，并额外遵守扫描专用规则：

- **每份文档必须有目录 + 概览图**
- **图表数量下限**：01→3, 02→3, 03→2, 04→2, 05→3, 06→3
- **各文档必须的图类型**：详见 `references/doc-format-spec.md` §六

> 通用排版规范见 `doc-gen` skill（图表选型、Mermaid/SVG 规则、代码块、文字写作）
> 扫描专用补充见 `references/doc-format-spec.md`

---

## References

- **`doc-gen` skill** — 通用文档排版规范（所有文档生成场景共用）
- `references/doc-format-spec.md` — 扫描报告专用补充（各文档必须图类型、图表数量下限、校验清单）
- `references/prompt-pack.md` — Codex Prompt 模板（已内嵌排版规则摘要）
- `references/output-contract.md` — 产物验收标准 + 排版校验清单
- `templates/codex-prompt-M1.txt` ~ `M4.txt` — 各模式 Prompt 模板
