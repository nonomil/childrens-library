---
name: scan-cc-codex-choice
description: largebase-structured-scan 流程缺少 CC/Codex 选择提示，导致 CC 直接调用 Codex 而未询问用户
type: feedback
---

扫描阶段（Phase B/C/D/E 生成 00-06 文档）应受 `codex_invocation` 偏好控制，但 `claude-workflow-largebase.md` 没有这个选择入口。

**Why:** 用户配置了 `cc_auto_decides`，CC 自作主张调了 Codex 做文档分析，但生成 Markdown 文档本质是非代码工作，应该 CC 自己做。用户期望被问一句。

**How to apply:** 在 `claude-workflow-largebase.md` Step 3（代码结构扫描）前增加一个门禁：
- 提示用户选择：A) CC 直接分析生成文档 B) 调用 Codex 生成
- 受 `codex_invocation` 偏好控制：`skip`→CC做，`always`→Codex做，`ask`→询问，`cc_auto_decides`→生成 Markdown 文档算非代码工作→CC 做
- 同时更新 `.claude/skills/largebase-structured-scan/SKILL.md` 的 Step 3 描述
