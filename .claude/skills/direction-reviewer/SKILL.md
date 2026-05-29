---
name: direction-reviewer
description: 工件驱动的方向漂移审查。基于 git diff、PLAN 变更、任务契约对比客观工件，检测 scope 漂移和方向偏离。不依赖对话信号，不继承主线程上下文。
layer: on-demand
tags: [drift-detection, direction-review, artifact-based, observer]
domain: governance
---

# 方向审查技能（工件驱动）

> 核心原理：不看对话说了什么，看**工件实际发生了什么**。git diff 和任务契约是客观的，不受对话中偏差前提的影响。
> 设计依据：agentsys artifact-first drift + claude-caliper "never let coding agent review its own code"

## 与旧版的区别

| 维度 | 旧版（对话信号驱动） | 新版（工件驱动） |
|------|---------------------|-----------------|
| 输入 | 数"继续"次数、读对话情绪 | 读 git diff、PLAN diff、任务契约 |
| 触发 | PostToolUse 高频 Hook | 阶段门禁自然节点 |
| 输出 | ✅/⚠️ 二态 | PASS/REBASELINE/BLOCK 三态 |
| 误报率 | 高（"继续"可能只是正常确认） | 低（只看客观事实） |

## 触发条件（三选一即触发）

1. **阶段门禁触发**：doing → in_review（自然工作流节点，无需额外 Hook）
2. **手动触发**：用户说"方向审查"/"检查方向"/"drift check"
3. **语义触发（兜底）**：CC 自己判断"继续做下去大概率走偏" → 单独触发

## 审查流程

### Step 1：读取任务契约（Baseline）

读取以下文件，建立审查基线：

```
docs/plan/PLAN.md                          — 任务总表（当前版本）
docs/plan/tasks/{task_id}/steps.md         — 任务步骤
docs/plan/tasks/{task_id}/acceptance.md    — 验收标准
docs/plan/tasks/{task_id}/.meta.yaml       — 任务元数据 + 基线哈希
.claude/state/MANIFEST.yaml                — 当前会话焦点
```

提取核心信息：
- **原始目标**（一句话，来自 PLAN.md 任务行）
- **预期范围**：allowed_paths（允许修改的文件/目录列表）
- **基线哈希**（如有）：approved_plan_hash / approved_acceptance_hash / allowed_paths_hash
- **task_id**：防止跨任务污染

### Step 2：收集客观工件

按优先级收集当前状态的实际工件：

1. `git diff --stat` — 改动统计
2. `git diff --name-only` — 已修改文件列表
3. 与 allowed_paths 对比：修改了哪些不在预期范围内的文件
4. PLAN.md diff（如基线存在）：对比任务描述是否被修改过

### Step 3：确定性预检（Scriptable Check）

按顺序检查，先验条件不满足时不做后续判断：

```
1. 无 task_id 或无任务目录 → contract_missing（需 LLM 评估严重性）
2. 无 .meta.yaml 或无 baseline 哈希 → legacy 任务，跳过哈希检查，进 Step 4
3. baseline 哈希不匹配 → contract_conflict → BLOCK
4. modified_files 有超出 allowed_paths 且无 task_id 关联 → 需 LLM 判断
5. modified_files 全部在 allowed_paths 内 且 契约存在且哈希一致 → PASS
```

确定性预检覆盖 ~70% 的正常场景，只有不确定时才调用 LLM。

### Step 4：LLM 深度审查（仅预检不确定时触发）

用三问框架审查：

**Q1. 初始目标是什么？**
一句话概括，只看任务契约。

**Q2. 实际工件发生了什么？**
基于 git diff 和 allowed_paths 对比，客观描述。

**Q3. 三态判定？**

| 状态 | 含义 | 后续动作 |
|------|------|---------|
| **PASS** | 工件与契约对齐 | 直接继续 |
| **REBASELINE** | scope 有合理增长，但需要更新契约 | **暂停编码**，更新契约后重新审查 |
| **BLOCK** | 方向偏离或契约被篡改 | 展示给用户，等确认后再继续 |

### Step 5：输出格式

严格按以下格式，不要多说：

```
【方向审查】
任务：{task_id} {任务名}
初始目标：<一句话>
实际工件：{文件数/行数/超出 allowed_paths 的文件}
判断：PASS / REBASELINE / BLOCK
reason_code：{见下方编码}
```

**REBASELINE 或 BLOCK 时追加（总字数 ≤80 字）：**
```
偏离说明：<客观描述>
建议：<1-2 个选项>
```

### reason_code 编码与三态映射

| code | 含义 | 默认三态 |
|------|------|---------|
| `aligned` | 工件与契约完全对齐 | PASS |
| `legit_scope_growth` | scope 增长但合理（如发现依赖问题需同步修改） | REBASELINE |
| `off_target` | 修改内容与任务目标不相关 | BLOCK |
| `contract_missing` | 任务契约不存在或未冻结 | REBASELINE（提示补充契约） |
| `contract_conflict` | 契约被中途修改（hash 不匹配） | BLOCK |
| `cross_task_scope_violation` | 修改了其他任务的文件（并行场景） | BLOCK |
| `legacy_no_baseline` | 旧任务无基线哈希，无法做契约对比 | PASS（仅做 allowed_paths 检查） |

### Fallback 矩阵

| 场景 | 处理方式 | reason_code |
|------|---------|-------------|
| 无 task_id | 需 LLM 评估是否偏离 | `contract_missing` |
| 无任务目录（tasks/{id}/ 不存在） | 需 LLM 评估是否偏离 | `contract_missing` |
| 无 .meta.yaml | 跳过哈希检查，仅检查 allowed_paths | `legacy_no_baseline` |
| 无 baseline 哈希（.meta.yaml 无 baseline 段） | 同上，跳过哈希检查 | `legacy_no_baseline` |
| 无 allowed_paths | 用 PLAN.md 任务行的文件描述推断范围 | `contract_missing`（需 LLM） |
| modified_files 超出 allowed_paths 且无 task_id 关联 | 需 LLM 判断是合法增长还是偏离 | → `legit_scope_growth` 或 `off_target` |
| 基线哈希不匹配 | 契约被篡改 | `contract_conflict` → BLOCK |
| 跨任务文件命中 | 修改了其他任务的文件 | `cross_task_scope_violation` → BLOCK |

### 承诺映射（P2 增强）

> 设计灵感：BinkRon Debate 的回溯校验——每次 scope 裁剪映射到核心承诺。

**触发时机**：在标准审查流程 Step 3 之后自动追加。

**承诺来源**：读取 `.claude/state/debate-commitments.yaml`（Debate 机制产出）。若无此文件，从 Plan 文档验收标准中提取核心承诺。

**映射流程**：
1. 读取 commitments 列表
2. 将当前 git diff 涉及的 scope 逐条映射到每个 commitment
3. 判断覆盖状态：✅ 完整覆盖 / ⚠️ 部分覆盖 / ❌ 未覆盖

**新增 reason_code**：

| code | 含义 | 默认三态 |
|------|------|---------|
| `commitment_eroded` | must 级承诺未被当前 scope 覆盖 | BLOCK |
| `commitment_partial` | should 级承诺部分覆盖 | REBASELINE |
| `commitment_aligned` | 所有承诺被覆盖 | PASS |

**reason_code 优先级合并规则**（解决 reason_code 和 commitment_* 的冲突）：

```
最终状态 = max(标准 reason_code, 承诺映射结果) 按以下优先级取最高：
  BLOCK:   contract_conflict > commitment_eroded > cross_task_scope_violation > off_target
  REBASELINE: contract_missing > commitment_partial > legit_scope_growth
  PASS:    commitment_aligned > legacy_no_baseline > aligned
```

规则：BLOCK > REBASELINE > PASS。同一三态内，具体 code 按上表从左到右优先。
不允许出现 `reason_code=aligned` + `commitment_eroded` 的矛盾输出。

**承诺文件生产者**：
- **唯一生产者**：Debate 机制（`claude-workflow-debate.md` Layer 1 收敛后写入）
- **Gate 只读确认**：`gate.md` 读取并冻结，不覆盖
- **无 Debate 时**：从 Plan 文档验收标准中提取，由 Gate 写入

**输出追加**（在标准输出格式的 reason_code 之后）：

```
承诺校验：{commitment_aligned / commitment_partial / commitment_eroded}
  C001: ✅ 覆盖 → [说明]
  C002: ⚠️ 部分覆盖 → [说明]
```

## 基线冻结机制

任务门禁确认时（gate approval），冻结以下哈希到 `.meta.yaml`：

```yaml
baseline:
  approved_plan_hash: "{PLAN.md 当前任务行的 SHA256 前 8 位}"
  approved_acceptance_hash: "{acceptance.md 的 SHA256 前 8 位}"
  allowed_paths_hash: "{allowed_paths 列表的 SHA256 前 8 位}"
  frozen_at: "{ISO datetime}"
```

审查时对比：如果哈希不匹配 → `contract_conflict`。

## 使用约束

- **只读**：不修改任何文件，不提供实现方案
- **独立**：不继承主对话的上下文和假设
- **简短**：PASS 时 ≤4 行，REBASELINE/BLOCK 时 ≤7 行
- **不循环**：审查结果交给用户决定，不做二次审查
- **task_id 隔离**：只审查当前任务范围内的工件，不跨任务
