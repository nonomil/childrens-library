---
name: pipeline-init
description: Use when 需要初始化或校准当前 Codex 控制面，确认 docs/plan、.claude/state/MANIFEST.yaml 和 scripts/taskctl.py 都能作为真实入口工作。
layer: ondemand
tags: [pipeline, init, taskctl]
domain: planning
---

# 控制面初始化技能

这里的“初始化”指的是当前 Codex 控制面初始化，不是旧 `pipeline/*` 状态账本。当前真相源是 `docs/plan/PLAN.md`、`docs/plan/tasks/`、`docs/plan/MERGE_QUEUE.yaml`，`.claude/state/MANIFEST.yaml` 只负责会话级焦点缓存。

## 触发方式

- 模板刚复制到新项目，需要先校准控制面入口
- `docs/plan/` 已存在，但状态总览、任务表或 merge queue 还没同步
- 当前需求要开新任务，但还没有跑过最小初始化检查

## 先看什么

1. `AGENTS.md`
2. `docs/plan/PLAN.md`
3. `docs/plan/MERGE_QUEUE.yaml`
4. `.claude/state/MANIFEST.yaml`
5. `python scripts/taskctl.py --help`

## 初始化流程

### 1. 确认关键文件齐全

至少确认这些路径存在并可读：

- `docs/plan/PLAN.md`
- `docs/plan/tasks/README.md`
- `docs/plan/MERGE_QUEUE.yaml`
- `.claude/state/MANIFEST.yaml`
- `scripts/taskctl.py`

如果缺的是导出模板本身应携带的脚手架，先补文件；不要自己退回旧的 pipeline 状态账本。

### 2. 先同步控制面状态

```bash
python scripts/taskctl.py sync
```

`sync` 的作用是刷新 `PLAN.md` 里的状态总览、任务表和 merge queue 视图，不负责替你推断需求。

### 3. 给新需求做路由判断

如果接下来要创建第一批任务，先跑 `route`：

```bash
python scripts/taskctl.py route \
  --path docs/plan \
  --doc-target docs/plan/PLAN.md#plan-task-table \
  --requires-stack
```

### 4. 创建最小任务骨架

已经明确参数时，用 `create`：

```bash
python scripts/taskctl.py create \
  --title "初始化任务" \
  --owner codex-main \
  --mode patch \
  --branch feat/bootstrap \
  --topic bootstrap \
  --path docs/plan
```

如果希望承接 `route` 建议，则改用 `create-from-route`。

## 初始化完成的判定标准

- `docs/plan/PLAN.md` 已同步到最新状态
- `docs/plan/MERGE_QUEUE.yaml` 可读且结构正常
- `.claude/state/MANIFEST.yaml` 存在，且被明确视为会话缓存而非总真相源
- 后续任务已知道应该走 `create` 还是 `create-from-route`

## 不要这样做

- 不要再创建或依赖旧的 pipeline 状态账本
- 不要把初始化理解成旧插件 setup 检测
- 不要跳过 `sync`，直接手工改 `PLAN.md` 汇总块
- 不要继续把兼容层 taskctl 路径当对外默认入口
