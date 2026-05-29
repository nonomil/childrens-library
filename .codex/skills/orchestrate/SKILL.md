---
name: orchestrate
description: 启动完整的多 agent 协作流水线，从需求到交付全自动
---

# 总调度技能

## 重要原则

- `pipeline/*` 是共享账本，不是自动消息总线
- 真正触发 Codex 的动作来自 `codex-plugin-cc`（插件路径）或 `mcp__codex__codex`（MCP 路径）
- 调用路径由 CLAUDE.md 强制门禁 Step 3 确定，本技能不再重复询问

## 触发方式

以下任一条件激活：

- 用户提出需要完整流水线处理的需求
- 用户说"按协作流执行" / "跑流水线" / "orchestrate"
- `pipeline/state.json` 中 `phase` 为 `idle` 且有新需求

## 执行步骤

### Step 1：初始化

1. 读取 `pipeline/state.json`，如不存在则调用 `pipeline-init` 技能
2. 将状态设为 `phase: planning`
3. 将用户需求写入 `requirement`

### Step 2：规划

调用 `.claude/skills/plan/SKILL.md`：

- 分析需求
- 拆解任务
- 写入 `pipeline/plan.md`
- 把任务对象同步写入 `pipeline/state.json.tasks`
- 任务初始状态统一写成 `planned`

规划完成后，更新：

- `phase: reviewing_plan`
- `plan_ready: true`

### Step 3：计划审查

根据当前会话的 Codex 调用路径执行：

**插件路径**：
```text
/codex:adversarial-review --background focus on pipeline/plan.md, rollback safety, race conditions, and testability
```

**MCP 路径**：
```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "high",
  prompt: "请审查 ./pipeline/plan.md，从实现可行性、回滚安全、测试策略角度指出问题。返回 [CODEX_REVIEW] 或 [CODEX_APPROVE]。"
})
```

收集反馈后：

- 若有 REVIEW，修改计划并重新送审，最多 3 轮
- 两轮以上仍无法收敛，通知用户人工介入
- 审查通过后，把 `owner = CODEX` 的任务状态从 `planned` 改为 `pending`
- 同步更新 `pending_tasks`
- 更新 `phase: executing`

### Step 4：实现分发

**插件路径**：
```text
/codex:rescue implement the CODEX tasks from pipeline/plan.md with the smallest safe patch, then summarize changed files and tests
```

**MCP 路径**：
```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "medium",
  prompt: "请执行 ./pipeline/plan.md 中标记给 CODEX 的任务，完成后返回 [DONE] + 变更摘要 + 测试结果。"
})
```

收到执行结果后：

- 将相应任务标记为 `in_progress` 或 `completed`
- 若失败且需要人工介入，标记为 `blocked`

### Step 5：代码审核

更新 `phase: reviewing_code`，调用 `.claude/skills/review/SKILL.md`。

审核不通过：

- 写入 `pipeline/review_log.md`
- 发回 Codex 修改
- 最多 2 轮

审核通过：

- 把对应任务标记为 `completed`
- 从 `pending_tasks` 中移除
- 加入 `completed_tasks`

### Step 6：测试

更新 `phase: testing`。

**插件路径**：
```text
/codex:rescue run the relevant test suite, fix only necessary failures, and return [TEST_RESULT] with a short summary
```

**MCP 路径**：
```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "low",
  prompt: "运行项目测试套件，修复必要失败用例，返回 [TEST_RESULT] + 摘要。"
})
```

### Step 7：报告

更新 `phase: reporting`，调用 `.claude/skills/report/SKILL.md` 生成最终报告。

### Step 8：完成

更新 `phase: done`，通知用户流程结束，并给出报告路径和关键结论。
