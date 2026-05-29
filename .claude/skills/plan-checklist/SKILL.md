---
name: plan-checklist
description: 将讨论结论沉淀为可执行的计划文档，采用 PLAN.md 总表 + 子文件夹打钩步骤结构
layer: ondemand
tags: [plan, checklist]
domain: planning
---

# 计划检查清单

把"口头讨论过的方向"固定成可执行文档，避免每次重新解释边界、优先级和已完成状态。

## 何时使用

- 用户说"重新梳理计划""给我总计划和分计划""生成可打钩文档"
- 准备新开 worktree，但需要先冻结范围和步骤
- 旧计划已经失真，需要基于最近对话重新整理

## 三层输出结构

```
docs/plan/
├── PLAN.md                              ← 更新总表（追加/修改任务行）
├── {编号}-{任务说明}/                     ← 创建子文件夹
│   ├── steps.md                         ← 打钩步骤清单
│   ├── acceptance.md                    ← 验收标准
│   └── .meta.yaml                       ← 元数据
```

## 执行流程

1. **读取现状**：读取 `docs/plan/PLAN.md`，确定当前最大编号
2. **整理讨论结论**：从当前对话中提取已确认的目标、范围、约束
3. **拆解任务**：每个任务创建独立子文件夹
4. **写入 steps.md**：打钩步骤清单
5. **写入 acceptance.md**：验收标准 + 约束
6. **写入 .meta.yaml**：任务元数据
7. **更新 PLAN.md 总表**：追加任务行

## 子文件夹模板

### steps.md

```markdown
# {编号} — {任务名称}

> Agent: {agent名} | 复杂度: {LOW/MEDIUM/HIGH} | 依赖: {前置任务ID或无}

## 执行步骤

- [ ] 1. {步骤描述}
- [ ] 2. {步骤描述}
- [ ] 3. {步骤描述}

## 完成标准

- [ ] 所有步骤打钩
- [ ] 验收标准全部满足
- [ ] diff ≤ 200 行
```

### acceptance.md

```markdown
# {编号} — 验收标准

## 功能验收
- [ ] {具体可测试条件}

## 质量验收
- [ ] 无 API 签名变更
- [ ] 新增逻辑有对应测试

## 机器验证（auto-verify）
> Review 通过后自动运行，失败时提示用户选择：AI 修复 / 人工处理 / 跳过

- [ ] `pytest` / `npm test` — 单元测试通过
- [ ] `tsc --noEmit` / `mypy .` — 类型检查通过
- [ ] `ruff check` / `eslint` — 代码规范检查通过
- [ ] `git diff --stat | tail -1` — diff ≤ 200 行

## 约束
- 文件范围：{允许修改的文件}
- diff 上限：200 行
- 不触碰：{排除的文件/模块}
```

### .meta.yaml

```yaml
task_id: "{编号}"
name: "{任务名称}"
agent: "{agent标识}"
branch: null
status: "pending"
depends_on: []
complexity: "MEDIUM"
created: "{YYYY-MM-DD}"
updated: "{YYYY-MM-DD}"
git_commits: []
```

## 打钩规则

- 只把**已经有证据**的事项打成 `[x]`
- 文档创建本身可以打钩
- 未开始实现的代码任务保持 `[ ]`
- 状态变化时**必须同时更新**：
  1. 子文件夹 `steps.md` 中的 checkbox
  2. `PLAN.md` 总表中对应行的状态列
  3. `.meta.yaml` 中的 status 字段

## 与 PLAN.md 的同步

| 事件 | steps.md | PLAN.md | .meta.yaml |
|------|----------|---------|-----------|
| 任务创建 | 全部 `[ ]` | 状态=⏳ | status: pending |
| 开始执行 | 第一步 `[x]` | 状态=🔄 | status: in_progress |
| 完成任务 | 全部 `[x]` | 状态=✅ | status: done |
| 遇到阻塞 | 标注阻塞原因 | 状态=🚫 | status: blocked |

## 不要做的事

- 不要只写一份泛泛的长文
- 不要把旧计划整段复制过来不修状态
- 不要把"还没做的代码工作"提前打钩
- 不要跳过 PLAN.md 总表更新（子文件夹和总表必须同步）
