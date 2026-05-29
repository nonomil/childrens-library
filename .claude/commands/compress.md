执行上下文压缩：
1. 读取 .claude/state/MANIFEST.yaml 的完整任务状态
2. 生成结构化快照，包含：当前焦点、全部待处理任务、关键决策、关键事实
3. 将快照写入 CONTEXT_SNAPSHOT.md
4. 更新 .claude/state/MANIFEST.yaml 的 context_snapshot 字段
5. 提示：建议开启新对话，把 CONTEXT_SNAPSHOT.md 粘贴到开头
