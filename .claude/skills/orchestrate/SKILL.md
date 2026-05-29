---
name: orchestrate
description: Use when 需要按当前 Codex 控制面编排完整流程，把需求从 route/create 一直推进到 execute/review/test/report/merge。
layer: ondemand
tags: [orchestrate, taskctl, codex]
domain: planning
---

# 总调度技能

当前 Codex 主流程不再围绕旧 `pipeline/*` 状态文件展开，而是围绕 `docs/plan/PLAN.md`、`docs/plan/tasks/`、`docs/plan/MERGE_QUEUE.yaml` 与 `scripts/taskctl.py` 编排。这个技能负责把一次需求收口成可执行任务，并串起规划、实现、评审、测试、交付和入队合并。

## 触发方式

- 用户说“按完整流程推进”“从需求一路排到 merge”“orchestrate”
- 当前需求还没有任务骨架，但已经确定要按 Codex 控制面完整落地
- 需要同时协调规划、执行、评审和合并顺序

## 先看什么

1. `AGENTS.md`
2. `docs/plan/PLAN.md`
3. `docs/plan/tasks/README.md`
4. `docs/plan/MERGE_QUEUE.yaml`
5. `python scripts/taskctl.py --help`

## 编排流程

### 1. 先校准控制面

- 如果仓库还没完成控制面初始化，先调用 `$pipeline-init`
- 如果当前需求还没有任务目录，先跑 `route`，不要跳过模式判断

```bash
python scripts/taskctl.py route \
  --path src/example \
  --doc-target docs/project-overview.md#project-structure-tree \
  --requires-worktree
```

### 2. 把需求落成任务骨架

优先用 `create-from-route` 直接承接路由结果：

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

如果输入已经足够明确，也可以改用 `create`。

### 3. 调度实现与状态推进

- 规划阶段用 `$plan` 补齐 `task.md`、`steps.md`、`acceptance.md`、`handoff.md`
- 实现阶段用 `$execute`，并遵守 `preflight -> proceed -> submit`
- 复杂任务需要拆多路评审时，用 `$review` 先做 `review-split`

### 4. 汇总评审与测试

- 多路 reviewer 完成后，用 `review-aggregate` 回写目标任务 `review.md`
- 再调用 `$test` 补齐验证证据、失败回归和交付前检查

```bash
python scripts/taskctl.py review-aggregate \
  --review-task T201 \
  --review-task T202 \
  --target-task T123
```

### 5. 形成交付结论并推进合并

- 调用 `$report` 汇总 `handoff.md`、`review.md`、验证结果和残余风险
- 评审通过后再推进状态：`approve -> enqueue -> merge`

```bash
python scripts/taskctl.py approve --task T123
python scripts/taskctl.py enqueue --task T123
python scripts/taskctl.py merge --task T123
```

## 编排时必须盯住的点

- 当前任务是否真的落在 `allowed_paths`
- 是否需要 `doc_targets`
- 是否命中 `advanced` 升级条件
- merge queue 是否需要顺序集成
- reviewer 结论是否已经收敛到目标任务的 `review.md`

## 不要这样做

- 不要再读写旧的 pipeline 状态账本
- 不要依赖旧插件命令、旧 MCP 调用入口或角色协议当主流程调度器
- 不要跳过 `route` / `create-from-route`，直接口头分派任务
- 不要在没有 `review.md` 与验证证据的情况下直接入队或合并
