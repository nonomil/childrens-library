扫描当前对话历史，执行：
1. 找出所有被提到但未写入 .claude/state/MANIFEST.yaml 的任务（关键词：还需要/另外/记得/别忘了/后续/TODO/注意）
2. 将遗漏任务追加到 .claude/state/MANIFEST.yaml 的 tasks 列表，source 标注 "claude-chat"
3. 同步更新 .claude/state/TASKS.md 的人类可读视图
4. 输出报告：发现 N 个遗漏任务，已补录 M 个
5. 询问用户确认每个新任务的优先级
