---
name: commit
description: Use when 完成任务需提交、查看历史、创建检查点或回退。涵盖提交、检查点、历史查看、还原等 Git 操作。
layer: always
tags: [git, commit, checkpoint, history, restore]
---

# commit

## 执行步骤

1. 在 `docs/development/` 下定位当前任务文档（优先最近修改的 `*-steps.md`）。
2. 将已完成步骤从 `- [ ]` 更新为 `- [x]`。
3. 运行 `git status --short` 和 `git diff --stat` 确认改动范围。
4. 生成 Conventional Commits 提交信息（`feat/fix/refactor/docs/test/chore`）。
5. 执行 `git add -A` 与 `git commit -m "<message>"`。

## 约束

- 不执行 `git push`，除非用户明确要求。
- 若存在范围外改动、冲突或测试失败，先停下并报告。

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
| 完成功能/修复 bug/用户说"完成了" | 提交（执行步骤 1-5） |
| 开始复杂修改/用户说"先保存一下" | checkpoint |
| 用户问"之前改了什么" | history |
| 用户说"回到之前"/"还原" | restore |

## 注意事项
- 只提交代码文件，不提交 .env、密钥等敏感文件
- checkpoint 用于临时保存，commit 用于正式提交
