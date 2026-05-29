---
name: report-format-baseline
description: 生成测试报告前必须先读已有终版报告作格式基线
type: feedback
---

生成任何 Docs/测试报告/ 下的报告前，先 Grep `Docs/测试报告/*FINAL*` 找最近终版报告，以其格式为基线。包括：嵌入图片路径、SVG 图表、面板说明、表格结构。

**Why:** 第一次生成的报告是纯表格无图片，用户明确要求参考 T010-A FINAL 格式后重写。浪费一轮迭代。

**How to apply:** 报告生成流程第一步 = 读 1 份已有 FINAL 报告 → 提取格式骨架 → 再填充内容。不仅限于 DL 报告，所有测试报告都适用。
