# 计划文件必须放到项目 docs/plan/ 目录

**Why:** Claude Code 内置 EnterPlanMode 会把计划写到 `.claude/plans/`（全局路径），但项目约定计划放在 `docs/plan/PLAN.md` + `docs/plan/tasks/Txxx-主题/`。放错位置会导致：计划分散在全局目录找不到、下次会话读不到历史计划、多项目计划混在一起。

**How to apply:** 收到需求需要做计划时，始终写到 `docs/plan/` 目录，不使用 Claude Code 内置 EnterPlanMode 的默认路径。如果用户触发了内置 plan mode，在退出时将内容迁移到 `docs/plan/` 并删除 `.claude/plans/` 中的副本。
