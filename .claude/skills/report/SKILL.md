---
name: report
description: Use when 需要汇总当前任务或一组任务的交付结论，基于 docs/plan、handoff.md、review.md 和状态机命令形成可交接报告。
layer: ondemand
tags: [report, handoff, taskctl]
domain: docs
---

# 交付报告技能

当前 Codex 控制面没有单独的旧 pipeline 测试报告文件作为总账本。报告要直接建立在 `docs/plan/PLAN.md`、任务目录的 `handoff.md`、`review.md` 和验证证据之上，并明确接下来是继续修、进入批准，还是入队合并。

## 触发方式

- 用户说“汇总当前任务”“生成交付报告”“给出最终结论”
- 一个任务已经完成实现、评审和测试，需要形成收口结论
- 一组相关任务需要一起判断是否 `approve / enqueue / merge`

## 先看什么

1. `docs/plan/PLAN.md`
2. 目标任务目录下的 `handoff.md`
3. 目标任务目录下的 `review.md`
4. 目标任务目录下的 `acceptance.md`
5. `python scripts/taskctl.py approve -h`

## 报告流程

### 1. 汇总任务事实

至少确认：

- `docs/plan/PLAN.md` 中的当前状态
- `handoff.md` 记录的实现摘要、验证命令、剩余风险
- `review.md` 中的结论是 `approved`、`changes_requested` 还是 `blocked`
- `acceptance.md` 里的要求是否都已被覆盖

### 2. 形成报告结构

建议输出 4 段：

1. 执行摘要：做了什么、范围在哪
2. 验证证据：跑了哪些命令、结果如何
3. 风险与阻塞：还有哪些待确认项
4. 下一步建议：继续修复 / 可以批准 / 可以入队 / 可以合并

默认把摘要回写到 `handoff.md`；如果 reviewer 需要直接看结论，也同步到 `review.md`。

### 3. 按结论推进状态

评审已经通过时，再推进：

```bash
python scripts/taskctl.py approve --task T001
python scripts/taskctl.py enqueue --task T001
python scripts/taskctl.py merge --task T001
```

如果还有阻塞，不要为了“生成报告”硬推进状态。

## 适合写进报告的内容

- 任务目标与实际变更范围
- 关键文件或目录
- 运行过的验证命令与结果
- 仍需人工确认的地方
- 合并前后的注意事项

## 不要这样做

- 不要再生成或依赖旧的 pipeline 审核日志文件
- 不要再生成或依赖旧的 pipeline 测试报告文件
- 不要把旧的 pipeline 状态账本当报告来源
- 不要引用额外排版技能作为报告前置条件
- 不要继续把兼容层 taskctl 路径写成默认状态推进入口
