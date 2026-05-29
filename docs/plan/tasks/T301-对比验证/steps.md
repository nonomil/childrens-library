# T301 — 对比实验与测试报告

> 优先级：P1 | 状态：⏳ pending | 前置任务：T202
> 预计完成日期：2026-05-10

## 目标

与论文结果对比，输出带截图的正式测试报告（doc-gen report 模式）。

## Steps

### 1. 最终性能基准
- [ ] 用最优参数在全量 200 张合成数据上评估
- [ ] 按 3 类缺陷分层分析（underprint/overprint/scratch）
- [ ] 记录 F1/Precision/Recall/IoU/速度

### 2. DAGM 灰度验证
- [ ] DAGM Class10 上跑 PLDD（灰度模式，跳过 RGB ΔC）
- [ ] 记录检测率

### 3. 与论文结果对比
- [ ] 对比论文 Table 3（Mean F1=0.9702, FP=103）
- [ ] 对比论文 Table 4（各方法 FP/FN/时间）
- [ ] 差距分析

### 4. 输出测试报告
- [ ] 按 doc-gen report 模式生成 `docs/测试报告/0001-PLDD合成数据评估.md`
- [ ] 嵌入截图（GM+Test+GT+Pred+ScoreMap 五联图）
- [ ] 嵌入参数扫描热力图
- [ ] SVG 条形图对比各参数组合 F1

## Acceptance

- [ ] 测试报告包含至少 2 张 SVG/Mermaid 图 + 3 张截图
- [ ] 量化指标完整（F1/P/R/IoU/TP/FP/FN/时间）
- [ ] 分层分析覆盖 3 类缺陷
- [ ] 有明确结论（PASS/FAIL/PARTIAL）
