# T201 — Pipeline 集成

> 优先级：P0 | 状态：✅ done | 前置任务：T101-T107
> 完成日期：2026-05-09

## 目标

将 7 个核心模块串成完整 Pipeline，可通过 `pipeline.detect()` 一键检测。

## Steps

### 1. 全流程串联
- [x] `pipeline.detect(test_path, gm_path)` → load → register → LDCE → matching → regions
- [x] `_extract_regions(defect_mask, score_map)` → findContours → bbox + score

### 2. 评估模块
- [x] `evaluate.py`：像素级 TP/FP/FN/Precision/Recall/F1/IoU
- [x] 目标级检测率
- [x] 可视化截图生成（GM + Test + GT + Pred + ScoreMap 五联图）
- [x] JSON 结果输出

### 3. 基线测试（合成数据 50 张）
- [x] F1=0.519, Precision=0.997, Recall=0.432
- [x] 瓶颈：Recall 偏低

## Acceptance

- [x] `pipeline.detect()` 可运行并返回结构化结果
- [x] `evaluate.py` 可批量评估并输出 JSON
- [x] 基线数值可复现

## 实际耗时

约 1 小时
