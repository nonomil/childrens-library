---
name: commit
description: Use when 完成任务需提交、查看历史、创建检查点或回退。涵盖提交、检查点、历史查看、还原等 Git 操作。
layer: always
tags: [git, commit, checkpoint, history, restore]
domain: git
---

# commit

## ⛔ MANDATORY GATES (read before proceeding)

> 执行前必须 echo-back 本块。未输出 = 未开始。

| # | 门禁点 | 位置 | 通过条件 |
|---|--------|------|----------|
| G1 | 构建产物排除 | 步骤 4 | *.pyc/__pycache__ 等不在 staging 区 |
| G2 | Breaking Change 检测 | 步骤 5 | 若有则追加 BREAKING CHANGE footer |
| G3 | git status + diff 检查 | 步骤 3 | 确认改动范围 ≤200 行 |

## 执行步骤

1. 在 `docs/development/` 下定位当前任务文档（优先最近修改的 `*-steps.md`）。
2. 将已完成步骤从 `- [ ]` 更新为 `- [x]`。
3. 运行 `git status --short` 和 `git diff --stat` 确认改动范围。
4. **构建产物清理**（artifact cleanup）— 在 staging 前执行：
   - 扫描未跟踪和已修改文件中的构建产物：`*.pyc`、`__pycache__/`、`*.o`、`*.obj`、`*.exe`、`*.dll`、`.DS_Store`、`node_modules/`
   - 若发现匹配文件：警告用户，列出发现项，**绝不自动添加这些文件到暂存区**
   - 用 `git add` 逐文件添加源代码文件，而非 `git add -A`（避免意外收入构建产物）
5. **Breaking Change 检测** — 分析 diff 内容：
   - 检查：函数签名变更、公开 API 删除、返回类型变更、文件重命名
   - 若检测到：在 commit message 末尾追加 `BREAKING CHANGE:` footer 说明影响
   - 若本次改动同时包含 breaking 和 non-breaking 变更：建议拆分为独立 commits
6. **多逻辑提交检测** — 评估改动内聚性：
   - 若 diff 涉及 >3 个不相关关注点（如：功能 A + 功能 B + 配置修改 + 文档更新），建议拆分
   - 向用户展示变更分组（按模块/功能/类型归类），让用户决定是否拆分提交
7. 生成 Conventional Commits 提交信息（`feat/fix/refactor/docs/test/chore`）。
8. 执行 `git add`（步骤 4 确定的文件列表）与 `git commit -m "<message>"`。

## 约束

- 不执行 `git push`，除非用户明确要求。
- 若存在范围外改动、冲突或测试失败，先停下并报告。
- **构建产物绝不进入暂存区**：`*.pyc`、`__pycache__/`、`*.o`、`*.obj`、`*.exe`、`*.dll`、`.DS_Store`、`node_modules/` 等构建产物一律排除，发现时警告用户。
- **breaking change 必须标注**：检测到函数签名删除/变更、公开 API 移除、返回类型变更、文件重命名时，commit message 必须包含 `BREAKING CHANGE:` footer。
- **混合改动建议拆分**：同时包含 breaking 和 non-breaking 变更时，建议拆分为独立 commits；涉及 >3 个不相关关注点时，展示分组建议由用户决定。

## 子命令

### checkpoint - 保存临时状态
**触发**：开始复杂任务前、暂停工作、尝试风险操作前
1. `git add -A && git commit -m "WIP: [当前任务描述]" --no-verify`
2. 告知用户：检查点已创建 + 哈希值

### history [文件/关键词] - 查看历史
**触发**：需要了解之前改了什么、不理解某段代码来源
1. `git log --oneline -20` 或 `git log --oneline -10 -- <file>`
2. 如需详情：`git show <hash>`
3. 总结相关修改历史

### restore <hash> [file] - 还原版本
**触发**：多次修改仍失败、用户要求回退、改坏了
1. 确认还原目标（整个提交还是某个文件）
2. `git checkout <hash> -- <file>` 或 `git revert <hash>`
3. 告知用户：已还原

## 智能判断

根据对话上下文判断应该执行哪个操作：

| 场景 | 动作 |
|------|------|
| 完成功能/修复 bug/用户说"完成了" | 提交（执行步骤 1-8） |
| 开始复杂修改/用户说"先保存一下" | checkpoint |
| 用户问"之前改了什么" | history |
| 用户说"回到之前"/"还原" | restore |

## 注意事项
- 只提交代码文件，不提交 .env、密钥等敏感文件
- 不提交构建产物：`*.pyc`、`__pycache__/`、`*.o`、`*.obj`、`*.exe`、`*.dll`、`.DS_Store`、`node_modules/`
- checkpoint 用于临时保存，commit 用于正式提交
- 建议项目根目录维护 `.gitignore` 覆盖上述构建产物模式，作为双重防护
