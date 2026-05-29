# 外部工具安装教训

## install 命令覆盖 hooks（2026-04-09）

**事件**：code-review-graph `install --platform claude-code` 整体替换了 `.claude/settings.json` 的 hooks 字段，原有 13 个 hooks（gate_guard、git_safety_check、auto_checkpoint_commit 等）全部丢失。

**根因**：外部工具的 install 命令按自己的格式重写 hooks，不做合并。这不是 bug 而是设计——它们不知道你的项目已有 hooks。

**规则**：
1. 安装任何外部工具前，先 `git diff HEAD -- .claude/settings.json` 确认当前状态
2. 安装后，立即 `git diff` 检查是否覆盖了原有 hooks
3. 如果覆盖了，手动合并：保留原有 hooks + 追加新工具的 hooks
4. 合并后用 `git diff` 二次确认只有增量变更

**适用范围**：所有会修改 `.claude/settings.json` 的 `install` 命令（code-review-graph、未来类似工具）
