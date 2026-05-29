---
name: review
description: Use when 需要按当前 Codex 控制面对任务做评审，使用 docs/plan/tasks、review.md 和 taskctl 的 review-split / review-aggregate 流程收口结论。
layer: always
tags: [review, taskctl, codex]
domain: review
---

# 审核技能

当前 Codex 主线的评审真相源落在任务目录的 `review.md`，并由 `taskctl review-split` / `review-aggregate` 负责拆分和汇总。不要再把旧 pipeline 评审日志或旧的 PASS/FAIL 文本协议当正式入口。

## 触发方式

- 用户说“审查当前任务”“做 code review”“汇总多路 reviewer 结论”
- 某个任务已经完成实现，需要进入 `in_review`
- 文档、算法或混合型任务需要按固定视角拆成多路评审

## 先看什么

1. `docs/plan/PLAN.md`
2. 目标任务目录下的 `task.md`、`acceptance.md`、`handoff.md`、`review.md`
3. `python scripts/taskctl.py review-split -h`
4. `python scripts/taskctl.py review-aggregate -h`

## 当前真相源

- `docs/plan/tasks/<task>/review.md`：目标任务最终评审结论
- reviewer 子任务目录中的 `review.md`：单视角评审记录
- `docs/plan/PLAN.md`：任务状态与 owner
- `scripts/taskctl.py`：固定视角拆分、聚合与状态推进

## 评审流程

### 1. 先锁定目标任务

评审前必须明确：

- 当前评的是哪个 `task_id`
- 输入材料有哪些源码、文档或测试文件
- 这次 review 属于 `code`、`algorithm`、`document` 还是 `mixed`

### 2. 需要多路评审时先拆任务

当任务复杂、证据面广、或需要不同视角独立给结论时，先拆 reviewer 任务：

```bash
python scripts/taskctl.py review-split \
  --title "T123 评审" \
  --topic t123-review \
  --review-kind code \
  --source-path src/example.py \
  --source-path tests/test_example.py
```

拆分后每个 reviewer 任务只改自己的 `review.md`、`handoff.md` 等交付文档，不直接改业务源码。

### 3. 单路 reviewer 的输出要求

每条发现都要包含：

- 严重度：`blocker` / `major` / `minor` / `question`
- 证据：具体文件、命令、日志、测试、文档引用
- 结论：已验证事实 or 推断
- 建议动作：修复、补测试、补文档或人工确认

没有问题时，也要写清：

- 本次审过的范围
- 仍然存在的残余风险
- 哪些结论只是“当前未发现问题”，不是“理论上绝对无风险”

### 4. 汇总多路 reviewer 结果

至少两路 reviewer 完成后，再聚合：

```bash
python scripts/taskctl.py review-aggregate \
  --review-task T201 \
  --review-task T202 \
  --review-task T203 \
  --target-task T123
```

聚合结果会写回目标任务目录的 `review.md`，并给出统一结论：

- `approved`
- `changes_requested`
- `blocked`

### 5. 推进状态

- 需要修复：保持目标任务在 `in_review`，补充修改要求
- 评审通过：再执行 `approve`
- 仍有外部阻塞：改成 `blocked`

## 推荐检查维度

- 正确性：是否真的满足 `task.md` 和 `acceptance.md`
- 回归风险：关键路径和长尾场景是否有证据
- 架构边界：是否破坏模块职责或 `allowed_paths`
- 文档一致性：命令、路径、示例和入口是否漂移
- 证据闭环：测试、日志、截图、引用是否足够支撑结论

## 不要这样做

- 不要再把旧 pipeline 评审日志当正式评审落点
- 不要再输出旧的 PASS/FAIL 文本协议
- 不要 reviewer 一边审一边直接改业务源码
- 不要只写主观判断，不附文件、命令或日志证据
