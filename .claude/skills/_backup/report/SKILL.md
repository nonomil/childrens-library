---
name: report
description: 汇总所有测试结果和审核记录，生成最终报告
---

# 报告生成技能

## 排版规范

> 报告输出遵循 `doc-gen` skill 的结构化文档规范（图表优先、分层表达、可导航）。
> 触发 `doc-gen` 后自动应用其排版规则，本文件只定义报告特有的数据结构和内容。

## 触发方式
- 由 `orchestrate` 调度流程调用
- 或用户说"生成测试报告" / "汇总结果" / "生成报告"

## 数据来源

- `pipeline/state.json`（完整流程状态）
- `pipeline/review_log.md`（所有审核记录）
- Codex 返回的 [TEST_RESULT] 数据
- `pipeline/state.json.tasks`（任务级状态）

## 报告结构（写入 pipeline/test_report.md）

### 1. 执行摘要

- 总任务数
- 成功数
- 需人工介入数
- 测试通过率
- 整体结论：PASS / FAIL / PARTIAL

### 2. 各任务状态

| 任务 ID | 名称 | 负责 | 状态 | 审核轮次 | 备注 |
|---------|------|------|------|---------|------|
| T001 | ... | CODEX | completed | 1 | ... |

### 3. 审核记录摘要

从 `pipeline/review_log.md` 提取关键决策和修改。

### 4. 测试结果

```text
[TEST_RESULT]
passed: X
failed: Y
coverage: Z%
notes: ...
```

### 5. 风险与建议

基于整体情况的优化建议。

### 6. 结论

- **PASS**：所有任务完成 + 测试全通过
- **FAIL**：有 blocked 任务或测试失败
- **PARTIAL**：部分通过但有可接受风险

## 最终操作

- 写入 `pipeline/test_report.md`
- 更新 `pipeline/state.json` → `phase: done`
- 通知用户流程结束
