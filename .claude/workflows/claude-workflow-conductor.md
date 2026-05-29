# claude-workflow-conductor｜Task 级增量执行流程

> 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束
> 触发条件：`claude-workflow-complex.md` Phase 6，用户明确说“开始开发”
> 入口：从复杂流程进入执行阶段时跳转至此

---

## 目标

Conductor 的职责不是重新规划，而是把已经冻结的 Plan 拆成一个个 task，按控制面状态机稳定推进，避免：

- 一次把过多任务塞进同一上下文。
- 多个 agent 同时改同一片区域。
- review、merge、handoff 脱离 `PLAN.md` 和任务目录。

它强调“单任务闭环”，而不是“大对话一把梭”。

---

## 前置条件

进入本流程前，至少满足：

1. 用户已明确说“开始开发”。
2. 相关 Plan 已定稿。
3. `docs/plan/PLAN.md`、`docs/plan/tasks/`、`MERGE_QUEUE.yaml` 已准备好。
4. `.claude/state/.gate-approved` 已存在。

如果这些条件不满足，应回到 Gate 或复杂流程，而不是直接进入实现。

---

## 单任务执行循环

### Phase 1：读取当前控制面

必读：

- `docs/plan/PLAN.md`
- 当前任务目录下的 `task.md`、`steps.md`、`acceptance.md`、`review.md`、`handoff.md`
- `.claude/state/MANIFEST.yaml`

### Phase 2：预检与放行

优先用：

```bash
python scripts/taskctl.py preflight --task <TASK_ID>
python scripts/taskctl.py proceed --task <TASK_ID>
```

只有 preflight 通过后，任务才进入 `doing`。

### Phase 3：按 `allowed_paths` 实施

实施时必须遵守：

- 只改当前任务允许的路径。
- 大文档按 section 小块编辑。
- 不顺手改不相关代码。
- 当前 task 完成前，不切去别的 task 继续堆上下文。

### Phase 4：验证与审查

完成实现后：

1. 跑最小必要测试或验证命令。
2. 更新 `review.md`、`handoff.md` 等交付文档。
3. 按控制面推进到 `in_review / approved / queued`。

### Phase 5：排队与合并

需要进入 merge 阶段时，继续由：

- `MERGE_QUEUE.yaml`
- `queue_guard.py`
- `taskctl.py enqueue / merge`

共同维护顺序。

---

## Context 约束

Conductor 模式下优先遵循“短上下文、强交接”原则：

- 一个 session 尽量只推进一个 task。
- 通过 `handoff.md`、`review.md`、`PLAN.md` 传递状态。
- 不依赖整段长对话历史作为唯一上下文来源。

这与 `claude-workflow-governance.md` 中的上下文治理规则保持一致。

---

## 什么时候停止

以下任一情况应暂停当前 task：

- preflight 不通过。
- 命中 `allowed_paths` 冲突或 `file_leases` 冲突。
- 用户改了需求边界，需要回到 Plan 或 Gate。
- review 出现 blocker，当前 task 不能继续推进。

---

## 与其他流程的关系

| 流程 | 关系 |
|------|------|
| `claude-workflow-complex.md` | Complex 负责定稿方案，Conductor 负责逐 task 执行 |
| `gate.md` | Gate 负责放行；Conductor 不替代 gate |
| `taskctl.py` | Conductor 的执行依赖控制面状态机 |
| `claude-workflow-multi-review.md` | 高风险 task 可在执行后进入多专家评审 |

---

## 完成标准

- 当前 task 已通过 preflight 并按状态机推进。
- 变更仅发生在允许路径内。
- 测试 / 验证 / review 证据已回写任务目录。
- 需要 merge 时已进入 queue，而不是口头宣称“完成”。
