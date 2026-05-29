# 成功 Prompt 模板

> 存储：经过验证的高质量 Codex/CC Prompt 模板。由 CC 在 Prompt 成功输出后沉淀。

## 文件命名

`[场景]-prompt.md`

示例：`codex-refactor-prompt.md`、`codex-bugfix-prompt.md`

## 条目格式

```markdown
# [场景] Prompt 模板

## 适用场景
[什么时候用这个模板]

## 模板内容
\`\`\`
[实际的 Prompt 文本]
\`\`\`

## 验证记录
- [日期] 第 1 次使用 — 结果：[好/需调整]
- [日期] 第 2 次使用 — 结果：[好/需调整]
- [日期] 第 3 次使用 — 结果：[好] → 标记 [STABLE]
```

## 稳定性标记

- 新模板：无标记，需 3 次验证
- 验证 3 次均成功：标题加 `[STABLE]` 前缀
- 2 次失败：移到 `lessons/` 记录失败原因

## 写入触发

- Codex 输出质量高、无需大改时 → 保存模板
- 同类任务第 2 次出现时 → 检查是否有现成模板

## 来源

参见 `claude-workflow-constants.md`「Prompt 沉淀规则」。

## 检索方式

```
Grep { pattern: "关键词", path: ".claude/memory/prompts/" }
```
