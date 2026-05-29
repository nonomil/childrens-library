---
name: scan-doc-gen-gate
description: largebase-scan 生成 00-06 文档时必须读完整 SKILL.md 并触发 doc-gen 校验门禁
type: feedback
---

执行 largebase-structured-scan 流程生成 00-06 文档时，我跳过了 SKILL.md 的 doc-gen 校验门禁（第 170-193 行），导致产出的文档全是纯 Markdown 表格，没有 SVG/Mermaid 图表，远低于参照质量。

**Why:** SKILL.md 里明确写了：
- 01-06 每份文档有图表数量下限（01≥3, 02≥3, 03≥2, 04≥2, 05≥3, 06≥3）
- 必须按 doc-gen skill 的 SVG/Mermaid 规范生成图
- 生成后必须按校验清单逐项检查
我只读了 extract/scan 命令用法就跳去生成文档了。

**How to apply:**
1. 执行任何 skill 前，必须**读完整个 SKILL.md**（不只是命令用法部分）
2. 生成扫描文档时，先加载 doc-gen skill 获取图表规范
3. 生成后对照 SKILL.md 的图表数量下限逐项校验
4. 更新 `largebase-structured-scan/SKILL.md`：在 Step 3（文档生成）中增加显式提示"必须先读取 doc-gen SKILL.md"
