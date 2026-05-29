---
name: plan
description: Use when 需要把当前需求收口为 Codex 可执行的任务控制面，明确 docs/plan/PLAN.md、任务目录、allowed_paths、doc_targets 和 taskctl 路由。
layer: ondemand
tags: [plan, taskctl, codex]
domain: planning
---

# 规划技能

Codex 当前的计划真相源不是 `pipeline/`，而是 `docs/plan/PLAN.md`、`docs/plan/tasks/` 和 `docs/plan/MERGE_QUEUE.yaml`。规划时先冻结范围、依赖、执行模式和 `allowed_paths`，再创建任务骨架。

## 触发方式

- 用户说“生成计划”“拆任务”“建立控制面”“创建任务骨架”
- 当前还没有任务目录，或现有任务的 `allowed_paths` / `doc_targets` / 执行模式不清楚
- 需要判断这次改动到底走 `patch`、`stack` 还是 `worktree`

## 先看什么

1. `AGENTS.md`
2. `docs/plan/README.md`
3. `docs/plan/PLAN.md`
4. `docs/plan/tasks/README.md`
5. `python scripts/taskctl.py --help`

## 当前真相源

- `docs/plan/PLAN.md`：任务总表、状态汇总、共享文件和依赖
- `docs/plan/tasks/<task>/`：单任务的 `task.md`、`steps.md`、`acceptance.md`、`handoff.md`、`review.md`、`.meta.yaml`
- `docs/plan/MERGE_QUEUE.yaml`：最终 merge 顺序
- `scripts/taskctl.py`：控制面 CLI 入口（转发到真实 taskctl 模块）

## 执行流程

### 1. 先做路由判断

范围、文档锚点或执行模式不清楚时，先跑 `route`，不要靠拍脑袋决定：

```bash
python scripts/taskctl.py route \
  --path src/example \
  --doc-target docs/project-overview.md#project-structure-tree \
  --requires-worktree
```

重点确认：

- 改动范围是否真的能落进 `allowed_paths`
- 是否需要 `doc_targets`
- 是否命中 `advanced` 升级条件
- 当前任务更适合 `patch`、`stack` 还是 `worktree`

### 2. 创建任务骨架

优先用 `create-from-route`，把路由建议直接落进任务目录：

```bash
python scripts/taskctl.py create-from-route \
  --title "示例任务" \
  --owner codex-main \
  --branch feat/example \
  --topic example \
  --path src/example \
  --doc-target docs/project-overview.md#project-structure-tree \
  --requires-worktree
```

如果你已经明确知道任务参数，也可以直接 `create`：

```bash
python scripts/taskctl.py create \
  --title "示例任务" \
  --owner codex-main \
  --mode patch \
  --branch feat/example \
  --topic example \
  --path src/example
```

### 3. 补齐任务正文

创建完成后，继续完善任务目录：

- `task.md`：目标、上下文、范围、风险、边界
- `steps.md`：按可执行顺序拆成打钩步骤
- `acceptance.md`：验收标准、测试要求、禁止触碰路径
- `handoff.md`：实现过程中的注意事项和后续接力信息

如果只是需要把讨论结论补成更细的打钩清单，可以继续配合 `$plan-checklist` 使用。

### 4. 判断是否升级到 advanced

命中下面任一情况，就不要停留在普通任务：

- `3+` 个 agent 并行
- 同一文件会被多个任务重叠改动
- 同一文档需要不同 section 并行
- 文档与代码联动，且 review / merge 顺序敏感

这时应补 `lane_key`、`approval_target`、`file_leases`：

```bash
python scripts/taskctl.py upgrade-advanced \
  --task T001 \
  --approval-gate coordinator \
  --approval-review reviewer \
  --approval-merge merge-owner
```

### 5. 开工前预检

计划写完不等于可以直接开工。真正进入实现前，先做预检：

```bash
python scripts/taskctl.py preflight --task T001
python scripts/taskctl.py proceed --task T001
```

`preflight` 负责检查：

- `allowed_paths` 是否和活跃任务冲突
- 当前任务是否需要升级为 `advanced`
- 文档目标、`lane_key`、审批链是否缺字段

## 规划阶段必须产出的信息

- 任务 ID、标题、owner、执行模式
- 精确的 `allowed_paths`
- 是否存在 `doc_targets`
- 依赖任务和 merge 顺序
- 是否要升级到 `advanced`
- 对应的测试或验证命令

## 不要这样做

- 不要再把旧 `pipeline` 状态文件或旧计划文档当当前计划真相源
- 不要跳过 `allowed_paths`，也不要写成大而泛的整个仓库路径
- 不要先开工再倒补任务目录
- 不要把长期 roadmap 塞回 `docs/plan/`；长期方向放 `docs/plans/`
