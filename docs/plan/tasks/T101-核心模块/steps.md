# T101 — 核心模块实现

> 优先级：P0 | 状态：✅ done | 前置任务：T001
> 完成日期：2026-05-09

## 目标

实现 PLDD 框架的 7 个核心模块，通过 Codex 审查零分歧。

## Steps

### 1. T101 图像配准（registration.py，159 行）
- [x] `register_images(test, gm)` → ECC 配准 + 3×3 中值滤波
- [x] ORB fallback（ECC 失败时自动降级）
- [x] 支持 MOTION_EUCLIDEAN 和 MOTION_HOMOGRAPHY

### 2. T102 加权欧氏色差（color_diff.py，65 行）
- [x] `weighted_euclidean_color_diff(img1, img2)` → Eq.1-6
- [x] BGR 正确映射：ch0=B, ch1=G, ch2=R
- [x] int32 做差 + float32 加权 + ×255/770 归一化

### 3. T103 LDCE 候选提取（ldce.py，123 行）
- [x] `extract_candidates(test, gm)` → n×4 滑动 + ΔC_best + T_filter 二值化 + 3×3 开运算
- [x] 边界处理：非整除尺寸自动裁剪

### 4. T104 RGB 平均梯度提取（gradient.py，49 行）
- [x] `compute_rgb_gradient(image)` → 三通道平均融合 Ḡ=1/3(G_R+G_G+G_B)
- [x] Sobel CV_32F，返回 gx/gy/magnitude

### 5. T105 背景掩码（mask.py，81 行）
- [x] `generate_candidate_mask(test_sub, gm_sub)` → Canny + 绝对差 + 膨胀 + 位与
- [x] `generate_bg_mask(gm_img)` → GM 梯度幅值 > T_bg

### 6. T106 ICSM（icsm.py，100 行）
- [x] `compute_icsm(test_sub, gm_sub, mask)` → Eq.10
- [x] 仅在 Canny 特征点上计算 + 1/N 归一化
- [x] `_f_activation(r_j, m_j)` 连续返回值（v1.1 修正：r_j 优先于 m_j）
- [x] 映射到 [0,1]：S = (Sim + 1) / 2

### 7. T107 T2G/G2T 双向匹配（matching.py，64 行）
- [x] `detect_defects(test, gm, candidate_mask)` → T2G 检测过印 + G2T 检测漏印
- [x] min(S_T2G, S_G2T) + T_score 阈值 + T_area 面积过滤

## Acceptance

- [x] 每个模块冒烟测试通过
- [x] Codex 代码审查 9/9 PASS（对照统一规格文档逐公式校验）
- [x] BGR 通道映射正确
- [x] F(r,m) 连续版本（不是二值门控）
- [x] ICSM 在 Canny 特征点上计算（不是逐像素）
- [x] RGB 三通道平均融合（不是取最大通道）

## 实际耗时

约 3 小时（含子代理并行执行 + Codex 审查）
