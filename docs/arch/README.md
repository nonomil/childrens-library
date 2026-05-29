# docs/arch/ — 架构决策记录

> 记录项目中的重要架构决策，回答"为什么这样设计"。

## 目录用途

存放架构决策记录（ADR，Architecture Decision Records）。每个重要决策一个文件。

## ADR 文档格式

文件命名：`[topic]-adr.md`

每份 ADR 包含：

```markdown
# [决策标题]

## 背景
[为什么要做这个决策？面临什么问题？]

## 决策
[选择了什么方案]

## 备选方案
[考虑过但没选的方案，每个一句话说明]

## 后果
### 正面
- [好处 1]

### 负面
- [代价 1]

### 风险
- [风险 1] — 缓解措施：[xxx]
```

## 生成时机

- complex workflow Phase 2-3 方案对比有结论时自动生成
- 用户或 CC 主动记录重要架构决策时手动创建

## 与其他文档的关系

- `docs/prd/`：PRD 定义"要什么"，ADR 记录"怎么设计"的决策理由
- `docs/scan/01-architecture.md`：描述"当前结构是什么"，ADR 记录"为什么选这个结构"
- `.claude/memory/context/`：AI 记忆中的技术决策节与 ADR 互补（AI 版更偏实操注意事项）
