# claude-workflow-debate｜需求辩证讨论流程

> 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束
> 触发条件：复杂任务命中 `debate_strategy=on_demand/always`，或用户显式说“debate / 需求讨论 / 辩证讨论”
> 入口：从 `CLAUDE.md` 或 `claude-workflow-complex.md` Phase 0.5 跳转至此

---

## 目标

在进入正式 Plan 之前，把复杂需求中的目标、边界、隐含约束和分歧点先讲透，避免“方案看起来完整，但核心承诺没冻结”。

本流程解决的不是“写代码”，而是三类前置问题：

1. 目标是否真的明确。
2. 各个候选方向的取舍有没有说清。
3. 哪些是 must，哪些只是 should / nice to have。

---

## 什么时候应该进入 Debate

适用场景：

- 需求跨模块、跨角色、跨文档来源，口头描述容易失真。
- 用户给了方向，但边界、优先级或非目标还不清楚。
- 同时存在两个以上合理方案，需要先对撞再收敛。
- 复杂任务准备进入 `claude-workflow-complex.md`，且不希望 Plan 带着歧义继续往下滚。

不适用：

- 简单单文件小改动。
- 纯文档润色。
- 已经有明确冻结的需求与验收标准。

---

## Debate 输出物

最少需要得到这 3 类结果：

| 输出 | 用途 |
|------|------|
| 需求共识摘要 | 给后续 Plan 生成当输入 |
| 分歧与取舍表 | 记录为什么选 A 不选 B |
| 承诺冻结清单 | 交给 Gate 或 Plan 继续沿用 |

其中承诺冻结建议至少区分：

- `must`：后续 scope 裁剪时不能架空。
- `should`：可降级，但要记录理由。
- `nice_to_have`：可延期，不影响本轮闭环。

---

## 执行步骤

### Phase 1：目标与边界澄清

1. 复述用户真正想解决的问题。
2. 分离“要什么”和“不要什么”。
3. 把范围、限制、优先级拆开确认。

### Phase 2：候选方案对撞

1. 至少列 2 个方案。
2. 逐项比较实现成本、风险、兼容性和维护成本。
3. 明确当前推荐方案和放弃其它方案的理由。

### Phase 3：冻结核心承诺

1. 把不能被后续执行阶段稀释的承诺列成清单。
2. 明确验收口径与非目标。
3. 若后续进入 Gate，允许 Gate 从本清单继续写入 `debate-commitments.yaml`。

### Phase 4：移交复杂流程

完成 Debate 后，不直接开工，而是把结果交给：

- `claude-workflow-complex.md` Phase 1 生成正式 Plan。
- `docs/plan/` 或相关需求文档作为后续真相源。

---

## 与其他流程的关系

| 流程 | 关系 |
|------|------|
| `gate.md` | Gate 负责放行；Debate 负责先把需求讲透 |
| `claude-workflow-complex.md` | Debate 是复杂流程的前置澄清阶段 |
| `taskctl.py` | Debate 不直接建任务，任务仍由控制面创建 |
| `claude-workflow-conductor.md` | Conducter 只处理执行；Debate 只处理需求收敛 |

---

## 完成标准

- 已明确目标、边界、约束和优先级。
- 已列出并比较候选方案。
- 已冻结 must / should / nice_to_have。
- 已把结果移交给正式 Plan，而不是停留在口头结论。
