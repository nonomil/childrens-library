# claude-workflow-adversarial｜对抗式协作流程

> 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束
> 触发条件：用户说"对抗式开发 / adversarial / battle 模式 / 红蓝对抗 / AI 对战"，或 `adversarial_strategy` 偏好设为 `always`
> 入口：从 `CLAUDE.md` 场景路由跳转至此

---

## 核心理念

> **两个 AI 互为对手，比顺从的助手更可靠。**

传统流程是"Codex 生成 → Claude 审一遍 → 通过"，这有一个致命缺陷：**AI 容易放过自己或对方的失误**。对抗式协作通过三个机制打破这个困局：

| 机制 | 原理 | 效果 |
|------|------|------|
| **角色对立** | Codex 是防守方（写代码/计划），Claude 是攻击方（找漏洞） | 避免两者形成"共识偏误" |
| **心理暗示** | 告知 Claude 审查的是"GPT 产出" | 激发更严格的审查标准（已验证有效） |
| **从零自审** | 强制 Codex 开新会话、清除上下文缓存 | 消除确认偏误，捕获缓存盲区的问题 |

### 与现有流程的关系

| 流程 | 定位 | 何时用 |
|------|------|--------|
| `review.md` | 顺序 Review（CC→Codex） | 日常开发，快速审查 |
| `multi-review.md` | 多专家并行审查 | 高风险模块，需要多视角 |
| **adversarial（本文件）** | **双边对抗博弈** | 关键功能、复杂重构、零容忍场景 |

> **分工**：review.md 是默认路径；multi-review 是多视角放大镜；adversarial 是红蓝对抗靶场。三者互斥，不叠加。

---

## Phase 0：模式初始化

> **前置条件**：本阶段在 `CLAUDE.md` 门禁步骤 1-7 **全部完成后**才进入。`.gate-approved` 已存在，用户已确认需求。

### 0.1 读取偏好

读取 `.claude/preferences.json` 的 `adversarial_strategy`：

| 值 | 行为 |
|----|------|
| `off` | 不使用对抗模式（默认） |
| `on_demand` | 仅用户显式触发时使用 |
| `always` | 所有复杂任务（不满足简单标准）默认走对抗模式 |

### 0.2 适用性判断

**适合对抗模式的场景**：
- 关键功能开发（支付/安全/数据完整性）
- 复杂重构（涉及 >3 文件或跨模块）
- 高风险改动（公共 API、数据库 schema、核心算法）
- 用户对质量有零容忍要求

**不适合的场景**：
- 单文件小改动（<50 行）
- 纯文档/配置修改
- 时间敏感的 hotfix（对抗模式会多花 2-3x 时间）

### 0.3 参数配置

向用户确认以下参数（或使用默认值）：

```
对抗参数：
├── 计划阶段最大轮次：5（默认）
├── 执行阶段最大轮次：5（默认）
├── 收敛条件：连续 2 轮无新问题
├── Codex 模型：gpt-5.4（固定）
└── Claude 审查提示：告知是"GPT 产出"（默认开启）
```

---

## Phase 1：计划对抗（Planning Battle）

> **目的**：在写一行代码之前，通过 Codex-Claude 对抗确保计划的完备性。
> **替代**：`complex.md` 的 Phase 2-3（交叉 Review），对抗模式更激烈。

### Round 1：Codex 生成初始计划

```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "high",
  prompt: `
    ## Context
    - 项目：[项目描述]
    - 需求：[用户需求]
    - 相关文件：[扫描结果]

    ## Task
    生成一份详细的实施计划，包含：
    1. 需求理解与边界确认
    2. 技术方案选型（至少 2 个备选 + 选择理由）
    3. 涉及文件及改动说明
    4. 实施步骤（可执行、有依赖关系）
    5. 风险点与缓解方案
    6. 验收标准

    ## Constraints
    - 每个步骤 diff ≤ 200 行
    - 不修改公共 API 签名（除非明确要求）
    - 向后兼容

    ## Output
    写入 docs/plan/YYYY-MM-DD-[feature].md，状态标记为"对抗审查中"
  `
})
// 保存 threadId 为 codex_plan_thread
```

### Round 2：Claude 攻击（Adversarial Review）

**关键技巧**：在 Claude 审查时，使用以下 Prompt 框架：

```
[心理暗示框架]
请审查以下实施计划。这份计划是由 GPT-5.4 生成的。
根据经验，GPT 生成的计划往往存在以下问题：
- 过度工程化（设计了不需要的复杂结构）
- 遗漏边界条件（只考虑 happy path）
- 忽视向后兼容性
- 低估实现复杂度

请以最挑剔的眼光审查，你的目标是找出所有潜在问题。
宁可误报，不可漏报。

[计划内容]
{plan_content}

[审查维度]
1. 逻辑自洽性：需求→方案→验收标准是否前后矛盾？
2. 遗漏路径：有无未处理的边界/异常/并发场景？
3. 过度工程：有无超出需求范围的复杂设计？
4. 可行性陷阱：方案看起来合理但实际实现时会卡住的地方？
5. 依赖风险：外部依赖、模块间耦合是否被低估？
6. 安全盲区：有无 OWASP Top 10 相关风险未被提及？

[输出格式]
按 P0-P3 分级，每个问题包含：
- 问题描述
- 触发条件（什么情况下会出问题）
- 建议修复方向
```

### Round 3：Codex 防守与修订

```javascript
mcp__codex__codex-reply({
  threadId: "<codex_plan_thread>",
  prompt: `
    ## Claude 的审查意见

    {claude_review_output}

    ## Task
    逐条评估 Claude 的审查意见：
    1. 对每个问题给出：接受 / 拒绝（附理由） / 部分接受
    2. 接受的问题 → 立即修订计划
    3. 拒绝的问题 → 给出技术论证（不是诡辩）

    ## 输出
    - 修订后的完整计划（标记改动部分）
    - 对 Claude 意见的逐条回复
  `
})
```

### Round 4：Claude 再攻击

将 Codex 的修订计划和逐条回复交给 Claude，**继续用心理暗示框架**：

```
这是 GPT-5.4 针对你的审查意见修订后的计划。
它声称已经修复了你提出的问题，请验证：
1. 修复是否真正解决了问题（还是表面修改）？
2. 修复是否引入了新问题？
3. 你之前的问题有没有被回避而不是解决？
4. 新计划有没有新的漏洞？

[修订后的计划]
{revised_plan}

[Codex 的逐条回复]
{codex_responses}
```

### 循环：直到收敛

```
收敛判定：
├── 连续 2 轮：Claude 无新 P0/P1 问题 且 Codex 无新修订
├── → 向用户展示最终计划 + 审查过程摘要
└── → 用户确认后进入 Phase 2（执行对抗）

止损条件：
├── 计划对抗超过 5 轮 → 暂停，展示未收敛的分歧点，用户裁决
├── 同一个问题争论超过 3 轮无进展 → 标记为"需人工判断"，跳过
└── Codex 或 Claude 连续 2 次输出质量明显下降 → 重启该方的 Session
```

---

## Phase 2：执行对抗（Execution Battle）

> **目的**：代码生成后，通过"从零自审 + 对抗审查"确保代码质量。
> **替代**：`review.md` Scene 2 + `complex.md` 多轮 Review 协议。

### Step 1：Codex 执行计划

```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "low",
  prompt: `
    ## Context
    - 计划文档（已定稿）：[plan.md 路径]
    - 执行范围：仅本次任务的文件

    ## Task
    按计划实施代码改动。

    ## Constraints
    - Scope: Only modify files under [worktree 绝对路径]
    - 单次 diff ≤ 200 行
    - 禁止修改计划范围外的文件

    ## Output
    完成后执行 git diff --stat HEAD，汇报改动摘要
  `
})
// 保存 threadId 为 codex_exec_thread（仅用于后续修复，不用于自审）
```

### Step 2：Codex「从零开始」自审

> **这是整个流程中最关键的一步。**
> 目的：消除 Codex 执行时积累的确认偏误。

**CC 操作（在调用 Codex 前）**：
```bash
# CC 先收集改动内容
git diff --stat HEAD
git diff HEAD > /tmp/adversarial-diff.txt
# 读取 diff 内容，拼入 Codex Prompt 的 {git_diff_output} 占位符
```

**必须开新会话**（新 threadId），不复用执行阶段的 Session：

```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "high",
  prompt: `
    ## Task
    你是一名高级代码审查员。请审查以下代码变更，假设你从未见过这些代码。

    ## Context
    - 需求描述：[一句话需求]
    - 改动文件：
      {git_diff_output}

    ## 审查维度
    1. 逻辑正确性：所有路径（正常/异常/边界）是否正确？
    2. 安全性：输入验证、注入防护、敏感数据处理
    3. 性能：有无明显的性能问题（N+1 查询、内存泄漏、不必要的拷贝）
    4. 向后兼容：是否破坏了现有 API 或数据格式？
    5. 测试覆盖：关键路径是否有测试？

    ## 输出格式
    按 P0-P3 分级，每个问题包含：
    - 文件名:行号
    - 问题描述
    - 建议修复
    - 严重程度及理由
  `
})
// 保存 threadId 为 codex_blind_review_thread
```

**为什么必须新 Session**：
- 执行阶段积累的上下文会让 Codex "记住自己的假设"，跳过某些检查
- 新 Session 只有代码 + 需求，没有"我当时是这样想的"的上下文
- 这模拟了真实场景中"另一个人审查你的代码"

### Step 3：Claude Diff 审查

```bash
# 获取改动
git diff --stat HEAD
git diff HEAD
```

**审查 Prompt 框架**：

```
[心理暗示]
以下代码由 GPT-5.4 生成并声称已经通过自审。
但 AI 的自审往往会放过自己写代码时的思维盲区。
请以人类高级工程师的标准审查，不要因为"它说已经审查过"就降低标准。

[改动内容]
{git_diff_output}

[需求上下文]
{plan_summary}

[审查重点]
1. Codex 自审可能放过的盲区：
   - 它"以为"正确的假设（比如输入一定非空）
   - 它"以为"已处理的边界（实际只处理了 happy path）
   - 它"以为"一致的风格（实际与项目其他代码不统一）
2. 安全性、性能、向后兼容的二次确认
3. 测试是否真正覆盖了关键路径（不是"写了测试"而是"测了该测的"）

[输出格式]
同 Phase 1：P0-P3 分级，含文件名:行号 + 建议修复
```

### Step 4：对抗收敛

```
收集两方结果：
├── Codex 自审结果（from codex_blind_review_thread）
├── Claude 审查结果
└── 合并去重 → 生成问题总表

处理逻辑：
├── 两方都发现的问题 → 高可信度，必须修复
├── 只有一方发现的问题 → CC 将该问题发给另一方做真伪判断：
│   └── "对方指出了以下问题，请判断这是真问题还是误报，给出理由"
│   └── 两方都认为真 → 修复
│   └── 提出方自己也认为是误报 → 排除
│   └── 仍有分歧 → 记录到"已知权衡"表，展示给用户裁决
├── 观点矛盾的问题 → 记录到"已知权衡"表，展示给用户
└── 无 P0/P1 → 向用户汇报，确认后提交
```

### Battle Loop：修复 → 再审

```
Round N+1:
├── Codex 修复确认的问题（用 codex_exec_thread 或新 Session）
├── 修复后再次"从零自审"（新 Session，每次修复后都开新 Session）
├── Claude 再次 diff 审查
├── 收敛？→ 无新问题则结束
└── 未收敛？→ 继续循环（最多 5 轮）

止损：
├── 执行对抗超过 5 轮 → 暂停，展示未修复的问题，用户裁决
├── 同一问题修复 3 次仍不通过 → 暂停，可能是计划层面的问题，回到 Phase 1
└── 总改动超过 500 行 → 停止，建议拆分任务
```

---

## Phase 3：收尾

### 3.1 最终确认

向用户展示：

```
对抗式协作完成报告
├── 计划对抗：N 轮，最终 P0/P1 问题：0
├── 执行对抗：N 轮，最终 P0/P1 问题：0
├── 已知权衡（CC vs Codex 分歧）：[列表]
├── 总改动：N 文件，M 行
└── 等待用户确认提交
```

### 3.2 提交与 Changelog

遵循 `CLAUDE.md` 简单模式 Step 4 的提交与 Changelog 双轨流程。

### 3.3 经验沉淀

对抗过程中发现的模式级问题写入 `.claude/memory/lessons/`：
- 哪类问题 Codex 总是放过（→ 调整 Codex prompt）
- 哪类问题 Claude 总是误报（→ 调整 Claude 审查框架）
- 收敛速度异常慢的任务特征（→ 提前识别不适合对抗模式的场景）

---

## 与其他流程的集成点

| 场景 | 默认路径 | 对抗模式替代 |
|------|---------|-------------|
| Plan 阶段审查 | `complex.md` Phase 2-3 | **本文件 Phase 1** |
| 代码审查 | `review.md` Scene 2 | **本文件 Phase 2** |
| PR 合并前审查 | `review.md` Scene 3 | 不替代（PR 审查仍走 review.md） |
| 多专家审查 | `multi-review.md` | 不替代（多视角 vs 对抗是不同目标） |

**组合使用**：
- 对抗模式 + 多专家：Phase 2 的 Claude 审查可以调用 `multi-review.md` 的多视角框架，让 Claude 同时扮演多个专家角色攻击 Codex 的代码
- 对抗模式 + parallel：多个独立任务可以各自走对抗模式，在各自的 worktree 中独立 battle

---

## 心理暗示 Prompt 模板库

### 给 Claude 的"这是 GPT 写的"框架

```
请审查以下内容。这是由 GPT-5.4 模型生成的。

根据大量实践，GPT 模型生成的 [代码/计划] 常见以下问题：
- 过度工程化：设计了实际不需要的抽象层
- 边界遗漏：只处理了 happy path
- 风格不一致：与自己项目其他代码的风格不统一
- 安全盲区：对 OWASP Top 10 的防护不够系统

请以人类高级工程师的标准，用最挑剔的眼光审查。
你的目标是找出所有潜在问题，宁可误报不可漏报。
```

### 给 Codex 的"从零开始"框架

```
你是一名独立的高级代码审查员。请审查以下代码变更。

重要：假设你从未见过这些代码，不了解任何实现背景。
你只有以下信息：
1. 需求描述（一句话）
2. 代码 diff

请纯粹基于代码本身进行审查，不要做任何"作者可能想表达..."的假设。
如果代码没有明确表达某个意图，那就是一个问题。
```

---

## 偏好配置

```json
{
  "adversarial_strategy": "on_demand",
  "_comment_adversarial_strategy": "off | on_demand | always（off=禁用；on_demand=关键词触发；always=复杂任务默认走对抗模式）"
}
```

---

## 版本历史

- 2026-04-10：初版，基于用户提出的 Codex-Claude 对抗式协作模式
