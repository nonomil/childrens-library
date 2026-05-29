# Prompt Pack

## 固定参数

```text
model: "gpt-5.4"
sandbox: "danger-full-access"
approval-policy: "on-failure"
```

## 全量扫描（M4）

```text
## Context
- 项目根目录：[DEV_DIR]
- 需求主题：[TOPIC]
- 扫描范围：[SCOPE]
- 参考文档：
  - [path1]：[用途]
  - [path2]：[用途]
- 输出目录：docs/scan/[YYYY-MM-DD]-[TOPIC]/

## Task
只做扫描分析，不修改源码。生成：
- 00-scan-meta.json
- 01-architecture.md
- 02-dataflow.md
- 03-api-surface.md
- 04-reference-constraints.md
- 05-impact-matrix.md
- 06-exec-brief.md
- 可选 scan-data.json（遵循 schema）

## Output Rules
- 表格优先，散文最少
- 每个高风险点必须绑定回归验证点
- 每个结论必须可追溯到文件/函数/行号或参考文档
- 信息不足时写入”信息缺口”，不要猜测

## Document Format Rules（扫描报告排版规范）

> 完整规范：`references/doc-format-spec.md`

### 图表（强制）
- 图优先于代码：能用 Mermaid/SVG 表达的不用代码块
- 按内容类型选图（依赖→graph TD，流程→flowchart，调用→sequenceDiagram，数据结构→classDiagram）
- Mermaid 节点 ID 只用英文，显示文本用双引号：A[“中文标签”]
- 每张图节点 ≤20，超过拆分 subgraph
- SVG 必须设 viewBox，源码无空白行，文字用 <text> 不用 foreignObject
- 每份文档最少图数：01→3, 02→3, 03→2, 04→2, 05→3, 06→3

### 文档结构（强制）
- 每份文档必须有：一句话说明（≤30字）→ 目录 → 概览图 → 主体章节
- 正文顺序：文字介绍 → 图 → 补充说明，不颠倒

### 代码块（强制）
- 禁止完整函数体（>15行），只用签名+流程图
- 所有代码块标注语言（python/bash/sql）

### 文字（强制）
- 每段 ≤5 行，超过拆分或改列表
- 模块名/函数名/路径用反引号
- 不写”如上所示”等废话

## Constraints
- 不执行业务代码
- 不修改源码
- 仅写 docs/scan 目录
```

## 多参考文档融合（独立调用）

```text
## Context
- 参考文档：
  - [doc1]
  - [doc2]
  - [doc3]
- 需求主题：[TOPIC]

## Task
输出：
1) 文档冲突矩阵
2) 约束汇总（带来源）
3) 实现必须遵守清单
4) 文档待更新位置

## Output Rules
- 冲突矩阵必须给出“建议采用版本+理由”
- 约束汇总必须标明对本需求的直接影响
```
