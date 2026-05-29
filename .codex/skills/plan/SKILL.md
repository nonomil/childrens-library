---
name: plan
description: 基于需求制定详细可执行的技术计划
---

# 规划技能

## 触发方式
- 由 `orchestrate` 调度流程调用
- 或用户说"生成计划" / "拆任务" / "写 plan"

## 输入
- `pipeline/state.json` 中的 `requirement` 字段
- 用户直接提供的需求描述

## 执行流程

1. 分析需求，拆解为独立可执行的任务单元
2. 为每个任务标注负责 agent：`[CLAUDE]` / `[CODEX]`
3. 标注任务依赖关系（哪个必须在哪个之前完成）
4. 估算每个任务的复杂度：LOW / MEDIUM / HIGH
5. 写入 `pipeline/plan.md`
6. 同步更新 `pipeline/state.json.tasks`
7. 每个任务对象至少写入：`id`、`title`、`owner`、`status`、`depends_on`、`complexity`
8. 规划阶段任务状态统一设为 `planned`
9. 更新 `pipeline/state.json`：`phase: reviewing_plan`，`plan_ready: true`，`plan_version + 1`

## 任务拆解原则

- 每个任务粒度：一个 agent 一次能完成的独立单元
- 依赖关系必须显式标注
- 复杂度评估基于：文件数、diff 行数、跨模块程度
- 高风险任务（权限、支付、迁移）标注 P0
- 单次任务 diff ≤ 200 行（硬约束，超过必须拆分）

## 输出格式

每个任务必须包含：
- 任务 ID（T001, T002...）
- 负责 agent
- 输入（依赖的前置任务输出或文件）
- 输出（产物描述）
- 验收标准（可测试的具体条件）
- 复杂度（LOW / MEDIUM / HIGH）

## state.json 任务对象示例

```json
{
  "id": "T001",
  "title": "实现用户 CRUD API",
  "owner": "CODEX",
  "status": "planned",
  "depends_on": [],
  "complexity": "MEDIUM"
}
```
