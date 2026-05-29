---
name: test
description: 运行项目测试套件并修复失败用例
layer: domain
tags: [python, test]
domain: python
---

# Codex 测试技能

## 触发方式
- 由 Claude Code 通过插件（`/codex:rescue`）或 MCP（`mcp__codex__codex`）请求测试
- 或 Codex 在实现完成后自动运行

## 执行流程

1. 确认项目的测试命令（从 AGENTS.md 或配置文件读取）
2. 运行测试套件
3. 如有失败用例，分析原因并修复
4. 重新运行测试确认修复有效
5. 返回结构化结果：

```
[TEST_RESULT]
passed: 8
failed: 0
coverage: 85%
notes: 所有测试通过，新增 3 个测试用例
```

## 轮次控制

- 最多修复 2 轮
- 第 2 轮仍有失败 → 记录失败用例，返回结果给 Claude Code
- Claude Code 收到失败结果后将任务标记为 `blocked`，通知用户介入
