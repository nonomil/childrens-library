# Background — 印刷标签缺陷检测（PLDD）

## 论文信息

- **标题**: Printed label defect detection using twice gradient matching based on improved cosine similarity measure
- **期刊**: Expert Systems With Applications, Vol 204, 2022
- **DOI**: 10.1016/j.eswa.2022.117372
- **作者**: Dongming Li, Jinxing Li, Yuanyi Fan, Guangming Lu 等（哈工大深圳 + 富贵精密工业）
- **开源状态**: 未公开代码和数据集

## 核心问题

1. **伪影干扰**：非刚性标签变形导致图减后大量伪影 → 误判
2. **泛化要求**：数千种标签类别，需检测未知类型缺陷
3. **实时性**：生产线要求 CPU 级实时检测

## 算法流程（PLDD）

```
输入：GM 图（金图）+ Test 图（工业相机实时采集）
  │
  ├─ Stage 1: 图像配准（shape-based template matching）
  │     └─ 中值滤波去噪 (3×3 核)
  │
  ├─ Stage 2: LDCE（潜在缺陷候选提取）
  │     ├─ GM/Test 各切分为 n×n 子图 (w×h 大小)
  │     ├─ 每个子图在 [-l, +l] 范围内滑动
  │     ├─ 计算 ∑ΔC_revised，取最小值位置为最佳差异图
  │     ├─ T_filter 二值化
  │     ├─ 形态学开运算 (3×3 核) 去噪
  │     └─ 轮廓提取 → 候选区域集合 C
  │
  ├─ Stage 3: 二次梯度匹配
  │     ├─ 对每个候选区域：
  │     │   ├─ Canny 边缘检测 (阈值 60/130)
  │     │   ├─ Mask 生成: Canny边缘 AND 差值二值图 → 膨胀 (5×5 核)
  │     │   ├─ Sobel 提取梯度 → Mask 按位与 → 消除背景梯度
  │     │   ├─ ICSM 相似度计算 (RGB 三通道融合)
  │     │   ├─ T2G 匹配: Test 作模板在 GM 滑动 → 检测过印
  │     │   ├─ G2T 匹配: GM 作模板在 Test 滑动 → 检测漏印
  │     │   └─ S_i = min(S_T2G, S_G2T)
  │     └─ 缺陷判定: S_i < T_score 且 像素面积 > T_area
  │
  └─ 输出：缺陷位置 + 相似度分数 + 缺陷面积
```

## 关键公式

### 色差近似 (Eq.1-6)
```
ΔC = √((2+r/256)·ΔR² + 4·ΔG² + (2+(255-r)/256)·ΔB²)
r = (C1_R + C2_R) / 2
ΔC_revised = ΔC × 255/770
```

### LDCE 二值化 (Eq.7)
```
d_bin = 255  if ΔC_revised >= T_filter
d_bin = 0    otherwise
```

### 改进余弦相似度 ICSM (Eq.10) — 核心
```
Sim(T_i, G_i^(u,v)) = Σ [G_x·G'_x + G_y·G'_y] / Σ [√(G_x²+G_y²)·√(G'_x²+G'_y²)] × F(r_j, m_j)
```
- 分子：梯度内积（方向一致性）
- 分母：梯度幅值乘积（归一化）
- F(r,m)：非线性激活函数

### 梯度融合 (Eq.11-14)
```
RGB 三通道梯度 → 按位与 Mask 操作
```

### 非线性激活函数 (Eq.17-19)
```
F(r_j, m_j) = 0  if r_j < T_r OR m_j > T_m
             = 1  otherwise

r_j = min(T_mag, G_mag) / max(T_mag, G_mag)   # 梯度幅值比
m_j = |T_mag - G_mag|                          # 梯度幅值差
```
- T_mag, G_mag: 测试图/GM 图的梯度幅值 (Eq.15-16)
- r_j → 1 表示幅值接近（正常区域），→ 0 表示差异大（缺陷区域）
- m_j → 0 表示幅值差小（正常区域），→ 大表示差异大（缺陷区域）

### 最终分数 (Eq.20)
```
S_i = min(S_T2G, S_G2T)
```

## 关键参数

| 参数 | 值 | 说明 |
|------|-----|------|
| n | 4 | 子图分割数（最优值） |
| l | 5 | LDCE 滑动范围 |
| T_filter | 20 | LDCE 二值化阈值 |
| T_score | 0.75 | 相似度判定阈值 |
| T_area | 5 | 最小缺陷面积阈值 |
| 中值滤波核 | 3×3 | 配准后去噪 |
| 形态学开运算核 | 3×3 | LDCE 去噪 |
| Mask 膨胀核 | 5×5 | Mask 扩展 |
| Canny 阈值 | 60 / 130 | 低/高阈值 |
| T_r, T_m | 未给出具体值 | 激活函数阈值 |
| openMP 线程 | 12 | 并行加速 |
| 检测时间 | 263.62ms (avg) | CPU only |

## 数据集（论文原始）

- 19 类印刷标签（工厂采集），3 类用于测试 (Label-1/2/3)
- 训练集：2985 张 → 256×256 patches，含 6 类人工模拟缺陷
  - 缺陷类型概率：过印 0.2 / 漏印 0.2 / 模糊 0.15 / 色斑 0.15 / 短线 0.15 / 长线 0.15
- 测试集：4429 张，44,628 个缺陷（含少量真实缺陷：285+2+51）
- 对比方法：SSIM, RTPDS, DSIM, FCN-VGG16, DeepLabV3+, Valente et al.
- 评估：object level，IoU > 0.001 为 TP
- 硬件：Intel Xeon E5-2620 CPU, RTX2080 Ti, 32GB RAM

## 性能指标（论文结果）

| 指标 | 值 |
|------|-----|
| Mean F1 | 0.9702 |
| FP 总数 | 103 / 44,628 GT |
| 平均 FP | 34.33 per label |
| 平均检测时间 | 263.62ms |
| GPU 需求 | 无（CPU only） |

## 数据集与复现资源

### 可用公开数据集

| 数据集 | 规模 | 适合复现？ | 来源 |
|--------|------|-----------|------|
| **DAGM 2007** | 10 类纹理 + 人造缺陷 | **较适合** — 有 GM/缺陷对 | [Kaggle](https://www.kaggle.com/datasets/bassam165/dagm-2007-industrial-defect-detection-dataset) |
| **MVTec AD** | 5000+ 图, 15 类 | **部分适合** — 纹理异常检测 | [MVTec](https://www.mvtec.com/research-teaching/datasets/mvtec-ad) |
| **AITEX** | 245 张, 7 种织物 | **部分适合** — 可验证 LDCE 模块 | [AITEX](https://www.aitex.es/afid/) |
| **Roboflow OBB Printing** | 印刷缺陷, OBB 标注 | **方向匹配** — 印刷品缺陷 | [Roboflow](https://universe.roboflow.com/cose-chen/obb-printing-defects-no-text-defects) |
| **NEU Surface Defect** | 1800 张, 6 类钢材 | 不太适合 — 金属表面差异大 | [Kaggle](https://www.kaggle.com/datasets/kaustubhdikshit/neu-surface-defect-database) |

### 复现路径建议

**推荐：自造合成数据** — PLDD 核心是 GM vs Test 梯度匹配，可用以下方式构造：
1. 收集真实印刷标签图像作为 GM
2. OpenCV 合成漏印（降低色值/区域遮挡）和过印（增加色值/区域扩展）
3. 用 DAGM 2007 做基准对照验证算法通用性

### 相关开源项目

| 项目 | 相关度 | 说明 |
|------|--------|------|
| [Mukosame/Print-Defect-Detection](https://github.com/Mukosame/Print-Defect-Detection-and-Quality-Assessment) | 中 | 印刷缺陷论文+代码索引 |
| [ParvinZE/Industrial-Defect-Detection](https://github.com/ParvinZE/Industrial-Defect-Detection) | 中 | 传统 CV + CNN 工业缺陷检测 |
| [waico/CV-for-anomaly-detection](https://github.com/waico/CV-for-anomaly-detection-in-industrial-applications) | 中 | 工业异常检测 CV 方法集 |
| [PMC 论文 Color Detection of Printing](https://pmc.ncbi.nlm.nih.gov/articles/PMC11461889/) | 高 | 直接引用 PLDD 改进余弦相似度 |

### 技术栈

- Python + OpenCV（cv2.matchTemplate, cv2.Sobel/Scharr, cv2.Canny）
- NumPy（改进余弦相似度实现）
- 无需深度学习框架（传统 CV 方法）

## ICSM 改进点总结

1. **RGB 三通道梯度融合**（非灰度化）→ 解决低对比度缺陷漏检
2. **非线性激活函数 F(r,m)** → 结合梯度幅值比和幅值差，缺陷区域得分趋 0、正常区域得分趋 1
3. **Mask 机制** → Canny + 差值二值图 AND + 膨胀 → 消除候选区域背景梯度
4. **二次匹配** → T2G 检测过印 + G2T 检测漏印 → min 融合 → 同时检测两种缺陷
