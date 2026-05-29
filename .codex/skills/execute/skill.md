---
name: execute
description: 执行 Claude Code 下发的实现任务
---

# Codex 执行技能

## 触发方式
- 由 Claude Code 通过插件（`/codex:rescue`）或 MCP（`mcp__codex__codex`）下发任务
- 或 Codex 读取 `pipeline/state.json.tasks` / `pipeline/plan.md` 中标记给自己的任务

## 执行流程

1. 优先读取 `pipeline/state.json.tasks`，找到 `owner = CODEX` 且 `status = pending` 的任务
2. 若状态文件未同步，再回退读取 `pipeline/plan.md`
3. 按 plan.md 中的实现要点执行
4. 完成后返回结构化结果：

```
[DONE] task_id: T00X
摘要：实现了 xxx 功能
变更文件：
  - src/api/user.ts（新增）
  - src/index.ts（修改）
测试：pass
风险：无
```

## 执行约束

- 只修改 Scope 指定目录下的文件
- 不删除文件，不修改 pipeline/ 目录
- 所有文本文件 UTF-8 编码
- 遵循项目 AGENTS.md 中的编码规范
- 不自行改写 `pipeline/state.json`，只返回结果给 Claude Code 归档
- 单次任务 diff ≤ 200 行（超过必须拆分）
