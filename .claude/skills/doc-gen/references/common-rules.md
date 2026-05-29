# doc-gen 通用规则

> 所有模式共用。按需从 SKILL.md 路由表加载。

---

## 图表选型

| 内容类型 | 首选图 | 备选图 |
|----------|--------|--------|
| 模块依赖 / 层次 | `graph TD` | SVG 网络图 |
| 执行流程 / 控制流 | `flowchart TD` | SVG 流程图 |
| 时序 / 调用顺序 | `sequenceDiagram` | — |
| 数据结构 | `classDiagram` | SVG 表格型 |
| 数据流向 | `graph LR` 带格式标注 | SVG 管道图 |
| 状态机 | `stateDiagram-v2` | — |
| 决策 / 算法 | `flowchart TD` + 菱形 | SVG 带伪码 |
| 文件 / 目录树 | SVG 树形图 | `graph TD` |
| 数量对比 / 性能 | SVG 条形图 | `xychart-beta` |
| 实体关系 | `erDiagram` | — |
| 时间线 / 里程碑 | `timeline` | SVG 甘特条 |
| 影响范围 / 热力 | SVG 矩阵色块图 | — |
| 优先级排布 | SVG 四象限 | — |

---

## Mermaid 规范

⚠️ **强制规则**：

- 节点 ID 只用英文字母、数字、下划线：`A["中文标签"]`
- 箭头标注用 `|文本|`：`A -->|"调用"| B`
- 每张图节点 ≤ 20；超过时拆分 subgraph
- subgraph 标题用英文或加引号的中文
- 图内不写长段说明，图外列表补充
- `classDiagram` 字段类型写在冒号后：`+String name`
- `sequenceDiagram` 关键返回值标注在 `-->>` 箭头上

---

## SVG 规范

⚠️ **强制规则**：

- SVG 源码中**不含空白行**（每行之间无空行）
- 注释 `<!-- -->` 只在必要时使用，不超过 3 条
- 必须设置 `viewBox`，不依赖固定 `width`/`height` 像素适配
- 文字用 `<text>` 标签，不用 `<foreignObject>` 嵌入 HTML
- 颜色用固定 hex（如 `#4a9edd`），不用颜色名（避免渲染差异）
- 图形元素分组用 `<g>` 并加 `id` 属性
- 不使用外部字体引用

⚠️ **SVG 结构顺序**（固定，不可调换）：

```xml
<svg viewBox="..." xmlns="http://www.w3.org/2000/svg">
<defs>[渐变 / 标记 / 滤镜定义]</defs>
<g id="background">[背景层]</g>
<g id="edges">[连线层，先画线再画节点避免遮挡]</g>
<g id="nodes">[节点层]</g>
<g id="labels">[标签层]</g>
</svg>
```

**SVG 最小示例（三层架构）**：

```xml
<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
<path d="M0,0 L0,6 L8,3 z" fill="#555"/>
</marker>
</defs>
<g id="background">
<rect x="20" y="20" width="560" height="70" rx="8" fill="#e8f4fd" stroke="#4a9edd" stroke-width="1.5"/>
<rect x="20" y="110" width="560" height="70" rx="8" fill="#e8fde8" stroke="#4add6a" stroke-width="1.5"/>
<rect x="20" y="200" width="560" height="70" rx="8" fill="#fdf5e8" stroke="#ddaa4a" stroke-width="1.5"/>
</g>
<g id="edges">
<line x1="300" y1="90" x2="300" y2="108" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<line x1="300" y1="180" x2="300" y2="198" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
</g>
<g id="nodes"/>
<g id="labels">
<text x="300" y="50" text-anchor="middle" font-size="13" font-weight="bold" fill="#1a5f8a">入口层</text>
<text x="300" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#1a7a2a">核心层</text>
<text x="300" y="230" text-anchor="middle" font-size="13" font-weight="bold" fill="#7a4a1a">IO 层</text>
</g>
</svg>
```

---

## 公式规范

⚠️ **强制规则**：

- 正文中所有公式用 `$$`，**单独成行**，上下各空一行
- 正文句子中**禁止**用 `$` 行内公式
- `$$` 符号**必须单独占一行**，不与公式内容同行
- 表格单元格内的简单公式可以用 `$`，不需要换行

**希腊字母处理**：
- **文字优先**：单独出现的希腊字母（φ, π, θ, λ, α, β, γ, σ, ω 等）直接使用 Unicode 字符，**不包裹 `$`**，当作普通文字
- **公式保护**：希腊字母在复杂数学表达式中（如 φ = 2πf、λ = h/p），或去掉格式会丢失数学含义时，使用 `$$` 独占行格式

**正确示例**：

```markdown
批量处理的时间复杂度为：

$$
T(n) = O(n \cdot k)
$$

其中 n 为文件总数，k 为单文件平均处理时间。
```

**错误示例**：

```markdown
<!-- ❌ 错误：$ 行内，与文字混排 -->
时间复杂度为 $T(n) = O(n \cdot k)$，其中 n 为文件数。

<!-- ❌ 错误：$$ 与公式同行 -->
时间复杂度为 $$T(n) = O(n \cdot k)$$。
```

**表格内公式**（正确，无需换行）：

| 指标 | 公式 | 说明 |
|------|------|------|
| 时间复杂度 | $O(n \cdot k)$ | n 文件数，k 单次耗时 |

---

## 代码块规范

⚠️ **强制规则**：

- **禁止**粘贴完整函数体（> 15 行的函数不直接引用）
- 代码块只用于：关键签名、核心算法片段（≤ 10 行）、命令示例
- 复杂逻辑**优先用流程图表达**，代码块作为补充
- 所有代码块必须标注语言：` ```python ` / ` ```bash ` / ` ```sql `
- 注释只说"为什么"，不说"是什么"

**代码 → 图替换原则**：

| 原本想写的代码 | 替换为 |
|----------------|--------|
| 完整函数体 | 函数签名 + 流程图 |
| 多层 if/else | 决策树图（`flowchart TD` + 菱形） |
| 循环处理逻辑 | 带循环标注的流程图 |
| 数据结构定义 | `classDiagram` 或字段表格 |
| 调用链 | `sequenceDiagram` |
| 状态转换 | `stateDiagram-v2` |

---

## 文字规范

⚠️ **强制规则**：

- 每段正文不超过 5 行，超过则拆分或改为列表
- 技术术语首次出现时在括号内给中英文对照
- 不写"如上所示""如图所示"等废话，直接描述
- 模块名 / 函数名 / 文件名 / 路径用反引号包裹：`` `merge_images()` ``
- 重要结论加粗

💡 **建议**：

- 每节开头用一句话概括该节核心结论，不用铺垫
- 列表项保持平行结构（都动词开头，或都名词开头）
- 跨文档引用写明文档编号：（见 `02-dataflow.md` §数据结构）