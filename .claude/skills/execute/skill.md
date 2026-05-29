---
name: execute
description: Use when 需要按当前 Codex 控制面执行已有任务，围绕 docs/plan/tasks、allowed_paths、taskctl preflight/proceed 和本地验证命令推进实现。
layer: ondemand
tags: [execute, codex, taskctl]
domain: pipeline
---

# Codex 执行技能

执行任务时，当前真相源是 `docs/plan/tasks/<task>/` 和 `docs/plan/PLAN.md`。先通过 `preflight` / `proceed` 进入 `doing`，再在 `allowed_paths` 内实现、验证、回写交接信息，最后 `submit`。

## 触发方式

- 已经存在任务目录，需要开始实现
- 用户给出明确的 `task_id`，要求 Codex 接手执行
- 需要把某个任务从 `todo` 推进到 `doing`、再推进到 `in_review`

## 先看什么

1. `AGENTS.md`
2. `docs/plan/PLAN.md`
3. 目标任务目录下的 `task.md`、`steps.md`、`acceptance.md`、`handoff.md`、`.meta.yaml`
4. `python scripts/taskctl.py preflight -h`
5. `python scripts/taskctl.py proceed -h`

## 执行流程

### 1. 先读取任务契约

实现前先确认：

- 当前任务 ID、owner、状态
- `allowed_paths`
- `doc_targets`
- 验收标准和测试命令
- 是否已经有上游 reviewer 或 merge 依赖

如果连任务目录都没有，先回到 `$plan` 创建控制面，不要直接开工。

### 2. 开工前先做预检

```bash
python scripts/taskctl.py preflight --task T001
python scripts/taskctl.py proceed --task T001
```

`preflight` 没通过时，优先修正：

- `allowed_paths` 过宽或缺失
- 活跃任务路径冲突
- 应该升级 `advanced` 但元数据没补齐

### 3. 在 allowed_paths 内实现

实现期间只改：

- `allowed_paths` 允许的源码 / 文档路径
- 当前任务目录下的 `steps.md`、`handoff.md`、必要时 `review.md`

同时保持：

- 小步可验证
- 所有文本文件显式 UTF-8
- 每次重要变化都能对应到 `steps.md` 的某一步

### 4. 边做边回写任务文档

- `steps.md`：完成一项就打钩
- `handoff.md`：记录当前进展、验证命令、遗留风险、接力说明
- `review.md`：只在当前任务需要自检摘要或汇总 review 结果时更新

### 5. 跑本地验证

至少执行与任务直接相关的验证：

- 单元测试 / 集成测试
- 类型检查 / lint
- 针对当前任务的最小手工验证命令

若 `acceptance.md` 已给出命令，以 `acceptance.md` 为准。

### 6. 提交到 review 前状态

验证完成后：

```bash
python scripts/taskctl.py submit --task T001
```

这表示任务已进入待评审状态，而不是已经可以合并。

## 推荐的最小执行节奏

1. `preflight`
2. `proceed`
3. 实现最小变更
4. 运行验证
5. 更新 `steps.md` / `handoff.md`
6. `submit`

## 不要这样做

- 不要再读写旧 `pipeline` 状态文件或旧计划文档
- 不要依赖旧插件命令或旧 MCP 执行入口当实现主线
- 不要绕过 `preflight` 直接把任务改成 `doing`
- 不要修改超出 `allowed_paths` 的文件
- 不要把“代码写完”当成“任务完成”；没有验证和交接就不能 `submit`
