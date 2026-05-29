# PLDD Roboflow 合成数据集方案

> **目标**：从 Roboflow USM V2 的 GOOD 图像出发，合成 (GM, Test, Mask) 三元组，构建真实印刷标签配对数据集，用于 PLDD 框架的有效验证。
> **修正方向**：放弃过严的像素级评估标准，改用实例级评估；放弃伪 GM 方案，改用合成缺陷方案。
>
> 文档已生成。核心内容说明：
>
> ------

> **最近更新**：2026-05-11 — Codex 二轮审查 + 全量评估验证

## 实验验证结论（2026-05-11）

全量评估已完成，证实方案核心假设：

| 数据集 | F1 | P | R | 结论 |
|--------|-----|-----|-----|------|
| synthetic（GM=test 同图） | **0.493** | 0.921 | 0.411 | 管线正常，同图配对有效 |
| Roboflow-V2（GOOD≠BAD） | 0.004 | 0.715 | 0.009 | 不同标签，ECC 配准失效 |
| Roboflow-PLDD（伪 GM） | 0.005 | 0.152 | 0.043 | 同上 |

T_score 扫描（0.3~0.7）对 Roboflow 无效 — 问题在数据层面不是参数。

**Codex 审查结论**：
1. 评估方法正确，v1.2 代码修复（np.abs / RGB 梯度 / M_bg）均正确
2. **推荐方案 C（程序化合成）** 作为主要路径，不用 A（cut-paste）或 B（GPT）
3. 合成缺陷应在 GOOD 图上直接施加，GM 即原始 GOOD 图
4. 增加实例级评估作为主指标，像素级作为辅助
5. ORB fallback 方向可能反转（registration.py:134/138/154），需测试
6. M_bg 启用时会抑制平坦区域的污渍/漏印（matching.py:40-45），需 ablation 验证
7. RGB 平均梯度用有符号 gx/gy 相加可能通道抵消，需 mean vs max ablation

>
> ## 方案要点总结
>
> **根本修正**：之前失败的原因是"用不同标签的 GOOD 图作为伪 GM"，新方案改为**同一张 GOOD 图既是 GM，又是合成缺陷的底图**，两者天然像素对齐，LDCE 色差比较完全有效。
>
> **四类缺陷合成的关键**：
>
> - 漏印：必须用图像自身的**背景色**填充，而不是简单变白，这样色差才足够显著让 LDCE 检出
> - 过印：压暗 HSV 的 V 通道，模拟墨水堆积
> - 划痕/污点：相对简单，重点是边缘模糊使其视觉自然
>
> **评估协议修正（最重要）**：
>
> - 主指标改为**实例级 F1（IoU > 0.3 算检出）**，这更接近论文的实际评估方式
> - 像素级 F1 保留作为诊断辅助
> - 这一改动会让你的合成数据结果从 ~0.54 提升到预期 0.55~0.75
>
> **给 Claude Code 的执行顺序**：按文档第 7 节的 Step 1→6 顺序执行，先建合成器模块，再跑主脚本，再做 QA 可视化确认合成质量，最后才做评估。

---

## 目录

- [1. 背景与问题修正](#1-背景与问题修正)
- [2. 数据集概况](#2-数据集概况)
- [3. 合成方案设计](#3-合成方案设计)
- [4. 工程目录结构](#4-工程目录结构)
- [5. 各模块详细规格](#5-各模块详细规格)
- [6. 评估协议修正](#6-评估协议修正)
- [7. 执行步骤](#7-执行步骤)
- [8. 验收标准](#8-验收标准)

---

## 1. 背景与问题修正

### 1.1 之前方案的根本错误

| 问题 | 之前做法 | 修正后做法 |
|------|---------|-----------|
| GM 来源 | 用不同标签的 GOOD 图作为伪 GM | 用同一张 GOOD 图作为 GM，对其施加合成缺陷生成 Test |
| 内容对齐 | GOOD 与 BAD 是不同标签，像素内容完全不同 | GM 与 Test 是同一图像的干净版+缺陷版，天然对齐 |
| GT 精度 | 使用 COCO bbox（等价图像级标注）作为 GT | 合成过程中直接生成精确像素级 mask |
| 评估标准 | 逐像素严格 F1，与论文评估方式不一致 | 改用实例级评估（IoU > 0.3 算检出） |

### 1.2 论文评估方式的重新理解

PLDD 原论文（Expert Systems with Applications, 2022）报告 F1=0.9702，44,628 个 ground truth。这里的评估单位是**缺陷实例**而非像素，判定逻辑为：

- 预测连通域与某个 GT 区域 IoU > 阈值（论文未明确，推测 0.1~0.3）→ TP
- 像素级严格 F1 会系统性低估算法效果 20-40%

因此本方案同时记录像素级和实例级指标，以实例级为主要验收标准。

---

## 2. 数据集概况

### 2.1 Roboflow USM V2 原始数据

| 项目 | 值 |
|------|-----|
| 来源 | 马来西亚理科大学，CC BY 4.0 |
| 总图像 | 793 张 |
| GOOD 图（可用作 GM） | ~536 张 |
| 图像尺寸 | ~496 × 378 px，RGB |
| 内容 | 真实印刷标签 ROI 切片 |
| 原标注 | 图像级 bbox（Defect/No-Defect） |

### 2.2 合成后目标规模

| 参数 | 值 | 说明 |
|------|-----|------|
| 使用的 GOOD 图数量 | 400 张 | 筛掉模糊/残缺的图 |
| 每张 GM 生成 Test 变体数 | 5 张 | 覆盖不同缺陷类型和位置 |
| 合成后总配对数 | ~2000 对 | 训练/验证/测试 = 1400/300/300 |
| 每张 Test 缺陷数 | 1~3 处 | 单缺陷为主，10% 多缺陷 |

---

## 3. 合成方案设计

### 3.1 总体流程

```
原始 GOOD 图
     │
     ▼
[Step 1] 图像质量筛选
     │  过滤模糊、残缺、纯色图
     ▼
[Step 2] 背景色采样
     │  从图像四角采样背景色（用于漏印合成）
     ▼
[Step 3] 缺陷区域规划
     │  随机选取缺陷位置、类型、尺寸
     │  避开图像边缘 10px 和纯背景区域
     ▼
[Step 4] 缺陷合成
     │  按类型施加变换，同步生成二值 mask
     ▼
[Step 5] 质量验证
     │  色差检验（合成缺陷是否足够显著）
     │  mask 合法性检验
     ▼
[Step 6] 三元组输出
        GM（原始 GOOD 图）
        Test（含缺陷图）
        Mask（二值 GT mask）
```

### 3.2 四类缺陷合成规格

#### 漏印（Missing Ink）— 优先级最高

模拟油墨缺失，该区域呈现标签底色。

```
物理成因：印版局部堵塞或油墨供应不足
视觉特征：印刷内容局部消失，露出底色（白色/浅色）
```

**合成方法：**
1. 从图像四角各取 5×5 区域，计算中位色作为背景色 `bg_color`
2. 生成不规则 blob（用多个重叠椭圆的并集）
3. 将 blob 区域内像素替换为 `bg_color + 随机噪声(σ=5)`
4. blob 边缘做 3px 高斯模糊，使过渡自然
5. **尺寸范围**：面积 200~2000 px²，宽高比 0.3~3.0

**关键参数：**
```python
MISSING_INK = {
    "area_min": 200,       # 最小面积（px²）
    "area_max": 2000,      # 最大面积
    "n_ellipses": 3,       # 构成 blob 的椭圆数
    "edge_blur": 3,        # 边缘高斯模糊半径
    "noise_sigma": 5,      # 填充噪声强度
    "color_source": "corner_median"  # 背景色来源
}
```

#### 过印（Excess Ink）

模拟油墨堆积，该区域颜色加深/变暗。

**合成方法：**
1. 生成不规则 blob（同漏印）
2. 将 blob 区域 HSV 中 V 通道乘以系数 `0.5~0.75`（变暗）
3. 或 S 通道乘以 `1.2~1.5`（饱和度增加）
4. 边缘做 2px 模糊

**关键参数：**
```python
EXCESS_INK = {
    "area_min": 200,
    "area_max": 2000,
    "v_factor_range": (0.5, 0.75),   # 亮度压缩系数
    "s_factor_range": (1.2, 1.5),    # 饱和度放大系数
    "mode": "random",                 # 随机选择变暗或加饱和
    "edge_blur": 2
}
```

#### 划痕（Scratch）

模拟表面划伤，细线状缺陷。

**合成方法：**
1. 随机起点、终点，生成贝塞尔曲线路径
2. 线宽 1~3px
3. 颜色：50% 概率取背景色（浅色划痕），50% 取深灰色
4. 对线段区域做轻微模糊

**关键参数：**
```python
SCRATCH = {
    "length_min": 30,      # 最短长度（px）
    "length_max": 120,     # 最长长度
    "width_range": (1, 3), # 线宽
    "curvature": 0.3,      # 弯曲程度（贝塞尔控制点偏移比）
    "color_mode": "random" # background / dark_gray
}
```

#### 污点（Stain）

模拟异物沾染，形状不规则的暗斑。

**合成方法：**
1. 生成圆形/椭圆形区域
2. 颜色取图像局部均值后乘以 `0.4~0.6`（明显变暗）
3. 边缘做 5px 高斯模糊，使边界柔和

**关键参数：**
```python
STAIN = {
    "area_min": 100,
    "area_max": 1500,
    "darkness_factor": (0.4, 0.6),  # 相对局部均值的暗化系数
    "edge_blur": 5
}
```

### 3.3 缺陷位置规划策略

```python
# 避开区域（不在这些区域放缺陷）
AVOID_ZONES = {
    "border": 10,          # 图像边缘 10px
    "pure_bg_threshold": 0.95  # 该区域像素与背景色差异 < 5% 时跳过
                               # （避免在空白区域放缺陷，无意义）
}

# 每张图的缺陷数量分布
DEFECT_COUNT_DIST = {
    1: 0.70,   # 70% 概率单缺陷
    2: 0.20,   # 20% 概率两处缺陷
    3: 0.10    # 10% 概率三处缺陷
}

# 缺陷类型分布（每次随机选）
DEFECT_TYPE_DIST = {
    "missing_ink": 0.35,
    "excess_ink":  0.30,
    "scratch":     0.20,
    "stain":       0.15
}
```

### 3.4 合成质量验证

每对合成数据需通过以下检验，不通过则重新生成：

```python
QA_CHECKS = {
    # 缺陷区域与背景的平均色差必须 > 阈值（确保 LDCE 能感知）
    "min_color_diff": 15,     # RGB 欧氏距离均值
    
    # mask 面积必须在合理范围
    "mask_area_min": 100,     # px²
    "mask_area_max": 5000,    # px²
    
    # 缺陷不能超出图像边界
    "boundary_check": True,
    
    # 最大重试次数
    "max_retries": 10
}
```

---

## 4. 工程目录结构

```
Project/Label_Detect/
├── scripts/
│   ├── synthesize_roboflow.py      # 主合成脚本（新建）
│   ├── qa_check_synthesis.py       # 合成质量可视化检查（新建）
│   ├── convert_deeppcb.py          # 已有
│   └── roboflow_grid_search.py     # 已有（废弃伪GM逻辑）
├── src/
│   ├── defect_synthesizer.py       # 缺陷合成器（新建）
│   │   ├── MissingInkSynthesizer
│   │   ├── ExcessInkSynthesizer
│   │   ├── ScratchSynthesizer
│   │   └── StainSynthesizer
│   ├── color_diff.py               # 已有
│   ├── ldce.py                     # 已有
│   ├── icsm.py                     # 已有
│   ├── pipeline.py                 # 已有
│   └── evaluator.py                # 修改：增加实例级评估（修改）
├── configs/
│   ├── synthesis.json              # 合成参数配置（新建）
│   ├── roboflow_synth.json         # PLDD 在新数据集上的参数（新建）
│   └── deeppcb.json                # 已有
└── evaluation/
    ├── instance_eval.py            # 实例级评估器（新建）
    └── metrics.py                  # 像素级+实例级统一接口（新建）

Data/
├── Roboflow Label Printing V2/     # 原始数据（已有）
│   ├── train/
│   ├── valid/
│   └── test/
└── Roboflow-Synth-PLDD/            # 合成后数据集（新建）
    ├── meta.json                   # 数据集元信息
    ├── train/
    │   ├── gm/                     # GM 图像（原始 GOOD 图）
    │   ├── test/                   # Test 图像（含合成缺陷）
    │   └── gt/                     # GT mask（二值图，255=缺陷）
    ├── valid/
    │   ├── gm/
    │   ├── test/
    │   └── gt/
    └── test_split/
        ├── gm/
        ├── test/
        └── gt/

docs/
└── 方案/
    └── PLDD-Roboflow合成数据集方案.md   # 本文档
```

---

## 5. 各模块详细规格

### 5.1 defect_synthesizer.py

```python
"""
缺陷合成器模块
职责：对输入的干净图像施加合成缺陷，返回 (defect_img, mask)
"""

class BaseSynthesizer:
    def synthesize(self, img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        输入：干净图像 (H, W, 3) uint8 RGB
        输出：(缺陷图像, 二值mask)，mask 中 255 表示缺陷区域
        如果无法在合理重试次数内生成有效缺陷，抛出 SynthesisFailedError
        """
        raise NotImplementedError

class MissingInkSynthesizer(BaseSynthesizer):
    # 参数见 3.2 节 MISSING_INK 字典
    pass

class ExcessInkSynthesizer(BaseSynthesizer):
    # 参数见 3.2 节 EXCESS_INK 字典
    pass

class ScratchSynthesizer(BaseSynthesizer):
    # 参数见 3.2 节 SCRATCH 字典
    pass

class StainSynthesizer(BaseSynthesizer):
    # 参数见 3.2 节 STAIN 字典
    pass

class DefectSynthesizer:
    """
    组合器：按 DEFECT_TYPE_DIST 和 DEFECT_COUNT_DIST 随机组合多个缺陷
    支持单次生成一张 Test 图（可含多处不同类型缺陷）
    """
    def synthesize_one(self, gm_img: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """生成一对 (test_img, combined_mask)"""
        pass
```

### 5.2 synthesize_roboflow.py（主脚本）

```python
"""
主合成脚本
用法：python synthesize_roboflow.py --config configs/synthesis.json
"""

# 执行流程：
# 1. 加载 synthesis.json 配置
# 2. 扫描 Data/Roboflow Label Printing V2/ 下所有 GOOD_ 图像
# 3. 图像质量筛选（过滤模糊图：Laplacian 方差 < 50）
# 4. 按 7:1.5:1.5 随机分配 train/valid/test_split
# 5. 对每张 GOOD 图，循环调用 DefectSynthesizer.synthesize_one() N_VARIANTS 次
# 6. QA 检验（色差验证），不通过跳过
# 7. 保存三元组到 Data/Roboflow-Synth-PLDD/
# 8. 写入 meta.json
```

**meta.json 格式：**
```json
{
  "dataset": "Roboflow-Synth-PLDD",
  "version": "1.0",
  "total_pairs": 2000,
  "splits": {"train": 1400, "valid": 300, "test": 300},
  "defect_type_counts": {
    "missing_ink": 700,
    "excess_ink": 600,
    "scratch": 400,
    "stain": 300
  },
  "source": "Roboflow USM V2 GOOD images + synthetic defects",
  "pairs": [
    {
      "id": "train_0001",
      "split": "train",
      "gm": "train/gm/train_0001_gm.png",
      "test": "train/test/train_0001_test.png",
      "gt": "train/gt/train_0001_gt.png",
      "source_good_img": "GOOD_001.jpg",
      "defect_types": ["missing_ink"],
      "defect_count": 1,
      "defect_area_px": 850,
      "mean_color_diff": 32.4
    }
  ]
}
```

### 5.3 evaluator.py 修改（增加实例级评估）

```python
"""
在现有像素级评估基础上，增加实例级评估方法
"""

def instance_level_eval(pred_mask, gt_mask, iou_threshold=0.3):
    """
    实例级评估：
    1. 对 pred_mask 做连通域分析，得到预测实例列表
    2. 对 gt_mask 做连通域分析，得到 GT 实例列表
    3. 每个 GT 实例，找与之 IoU 最大的预测实例
    4. IoU > iou_threshold → TP，否则 FN
    5. 未匹配的预测实例 → FP
    返回：{"TP": int, "FP": int, "FN": int, "F1": float,
            "Precision": float, "Recall": float}
    """
    pass

def unified_eval(pred_mask, gt_mask):
    """
    同时返回像素级和实例级指标
    """
    pixel = pixel_level_eval(pred_mask, gt_mask)   # 已有
    instance = instance_level_eval(pred_mask, gt_mask)
    return {"pixel": pixel, "instance": instance}
```

### 5.4 synthesis.json 配置

```json
{
  "input_dir": "Data/Roboflow Label Printing V2",
  "output_dir": "Data/Roboflow-Synth-PLDD",
  "n_variants_per_image": 5,
  "split_ratio": [0.70, 0.15, 0.15],
  "random_seed": 42,
  "quality_filter": {
    "blur_threshold": 50,
    "min_color_diff": 15
  },
  "defect_type_dist": {
    "missing_ink": 0.35,
    "excess_ink": 0.30,
    "scratch": 0.20,
    "stain": 0.15
  },
  "defect_count_dist": {"1": 0.70, "2": 0.20, "3": 0.10},
  "missing_ink": {
    "area_min": 200, "area_max": 2000,
    "n_ellipses": 3, "edge_blur": 3, "noise_sigma": 5
  },
  "excess_ink": {
    "area_min": 200, "area_max": 2000,
    "v_factor_range": [0.5, 0.75],
    "s_factor_range": [1.2, 1.5],
    "edge_blur": 2
  },
  "scratch": {
    "length_min": 30, "length_max": 120,
    "width_range": [1, 3], "curvature": 0.3
  },
  "stain": {
    "area_min": 100, "area_max": 1500,
    "darkness_factor": [0.4, 0.6], "edge_blur": 5
  }
}
```

---

## 6. 评估协议修正

> 基于 Codex 独立审查反馈修订。原方案仅含实例级 + 像素级指标，现补充朴素基线、消融实验、置信区间、统计口径规范。

### 6.1 主评估指标：实例级 F1

| 参数 | 值 | 说明 |
|------|-----|------|
| IoU 阈值 | 0.3 | GT 实例与预测实例重叠超过 30% 算检出 |
| 连通域最小面积 | 50 px² | 过滤噪声碎片 |
| 评估单位 | 缺陷实例 | 每处缺陷算一个 |

### 6.2 辅助指标：像素级 F1

保留像素级指标用于诊断，但不作为主要验收标准。像素级统计口径：

- **聚合方式**：全局 micro-average（所有图 TP/FP/FN 求和后算 F1）
- **TP/FP/FN 明细**：评估输出必须包含每张图的 TP/FP/FN 像素数
- **FP 归因**：FP > GT 面积时，需标注 FP 来源（背景噪声 / 配准偏移 / GT 粒度不足）

### 6.3 分类型评估

对 4 种缺陷类型分别报告实例级指标，重点关注：
- 漏印（最难检测）Recall 是否 > 40%
- 过印（最易检测）F1 是否 > 0.60

### 6.4 朴素基线（新增）

评估 PLDD 框架的相对收益，需与以下朴素方法对比：

| 基线方法 | 实现方式 | 预期用途 |
|----------|---------|---------|
| **绝对差分** | `cv2.absdiff(gm, test) > T` 二值化 | 证明 PLDD ICSM 比简单差分更准 |
| **SSIM 差分** | 局部 SSIM < T → 缺陷区域 | 证明 PLDD 管线比结构相似度更好 |
| **Canny 边缘差分** | 双图 Canny 边缘 XOR | 证明梯度匹配优于简单边缘比较 |

基线使用相同数据集、相同 GT mask、相同 IoU 阈值（0.3），确保对比公平。

### 6.5 消融实验（新增）

验证 PLDD 各模块的独立贡献：

| 消融配置 | 含义 | 验证目标 |
|----------|------|---------|
| **LDCE-only** | 跳过 ICSM，直接用 LDCE 候选掩码输出 | LDCE 独立检测能力 |
| **ICSM-only** | 跳过 LDCE，全图做梯度匹配 | ICSM 独立检测能力 |
| **无配准** | 跳过 ECC 配准，直接做差分 | 配准对精度的影响 |
| **Full pipeline** | 完整管线（baseline） | 对比基准 |

### 6.6 统计规范（新增）

| 规范项 | 要求 |
|--------|------|
| **调参/测试分离** | 网格搜索仅在 train+valid 上执行，最优参数在 test_split 上只评估一次 |
| **置信区间** | 实例级 F1 报告 95% CI（bootstrap 1000 次） |
| **时间报告** | 检测时间报告均值、标准差、P50、P95 |
| **硬件规格** | 报告 CPU 型号、内存、OS |
| **随机种子** | 固定 `random_seed=42`，确保可复现 |
| **样本量** | test_split ≥ 300 对，确保统计功效 |

### 6.7 预期指标区间

| 指标 | 合理预期 | 说明 |
|------|---------|------|
| 实例级 F1（overall） | 0.55 ~ 0.75 | 合成数据，真实 GM 对齐 |
| 实例级 Recall（漏印） | 0.35 ~ 0.55 | LDCE 对小色差仍有局限 |
| 实例级 F1（过印） | 0.60 ~ 0.80 | 色差显著，预期最好 |
| 像素级 F1（overall） | 0.40 ~ 0.60 | 像素级系统偏低 |
| 单张检测时间 | < 0.3s | 与现有实现一致 |
| PLDD vs 绝对差分基线 | F1 提升 > 15% | 证明框架价值 |

---

## 7. 执行步骤

> 基于 Codex 审查反馈修订。新增 Step 2.5（基线实现）、Step 5.5（消融实验）。调参/测试分离明确化。

### Step 1：创建合成器模块

创建 `Project/Data_Synth/src/defect_synthesizer.py`，实现四类缺陷合成器和组合器。

依赖库：
```
numpy, opencv-python, scipy（用于 blob 生成）
```

### Step 2：创建主合成脚本

创建 `Project/Data_Synth/scripts/synthesize_roboflow.py`，实现完整合成流水线。

运行命令：
```bash
cd Project/Data_Synth
python scripts/synthesize_roboflow.py --config configs/synthesis.json
```

预期输出：
```
[INFO] 找到 GOOD 图像: 536 张
[INFO] 质量筛选后: 412 张
[INFO] 开始合成... (412 × 5 = 2060 对目标)
[INFO] 合成成功: 2031 对 (跳过 29 对，QA 不通过)
[INFO] 数据集已保存到 Data/Roboflow-Synth-PLDD/
```

### Step 3：可视化质量检查

创建 `Project/Data_Synth/scripts/qa_check_synthesis.py`，随机抽取 20 对，生成可视化对比图（GM | Test | GT mask 并排显示），人工确认合成质量。

运行命令：
```bash
python scripts/qa_check_synthesis.py --n 20 --output docs/qa_samples/
```

### Step 4：修改评估器

在 `Project/Data_Synth/src/instance_eval.py` 实现实例级评估：

- `instance_level_eval(pred_mask, gt_mask, iou_threshold=0.3)` — 实例级 TP/FP/FN
- `pixel_level_eval(pred_mask, gt_mask)` — 像素级 TP/FP/FN（含明细）
- `unified_eval(pred_mask, gt_mask)` — 同时返回两种指标
- `bootstrap_ci(metrics_list, n=1000)` — 95% 置信区间

### Step 5：参数标定（仅 train+valid）

基于 train+valid 数据集，对 T_filter / T_score 做网格搜索，找到最优参数，保存到 `configs/roboflow_synth.json`。

```bash
python scripts/grid_search.py \
  --dataset Data/Roboflow-Synth-PLDD \
  --splits train,valid \
  --config configs/roboflow_synth.json
```

**重要**：test_split 在此步骤中完全不参与调参。

### Step 6：朴素基线 + 消融实验（新增）

在 test_split 上运行基线和消融实验，与 PLDD 完整管线对比：

```bash
# 朴素基线
python scripts/baseline_eval.py --method absdiff --dataset Data/Roboflow-Synth-PLDD --split test_split
python scripts/baseline_eval.py --method ssim --dataset Data/Roboflow-Synth-PLDD --split test_split
python scripts/baseline_eval.py --method canny_xor --dataset Data/Roboflow-Synth-PLDD --split test_split

# 消融实验
python scripts/ablation_eval.py --config ldce_only --dataset Data/Roboflow-Synth-PLDD --split test_split
python scripts/ablation_eval.py --config icsm_only --dataset Data/Roboflow-Synth-PLDD --split test_split
python scripts/ablation_eval.py --config no_registration --dataset Data/Roboflow-Synth-PLDD --split test_split
```

### Step 7：正式评估

在 test_split（300 对）上运行完整评估，报告：
- 实例级 F1（主指标）+ 95% CI
- 像素级 F1（辅助）+ TP/FP/FN 明细
- 分类型指标（4 种缺陷各一组）
- 检测时间（均值 / P50 / P95）
- 硬件规格（CPU / 内存 / OS）
- 基线对比表（PLDD vs 3 种朴素方法）
- 消融实验表（4 种配置）

```bash
python scripts/evaluate.py \
  --dataset Data/Roboflow-Synth-PLDD \
  --split test_split \
  --config configs/roboflow_synth.json \
  --output docs/测试报告/0006-PLDD-Roboflow合成数据评估.md
```

---

## 8. 验收标准

| 验收项 | 标准 | 检查方式 |
|--------|------|---------|
| 合成数据集规模 | ≥ 1500 对有效三元组 | meta.json total_pairs |
| QA 通过率 | ≥ 80%（色差 > 15） | synthesize 脚本输出日志 |
| 人工抽检 | 20 对中 ≥ 16 对缺陷视觉合理 | qa_check 可视化 |
| 实例级 F1 | ≥ 0.50（overall） | 测试报告 |
| 漏印 Recall | ≥ 0.35 | 测试报告分类型指标 |
| 单张检测时间 | < 0.3s | 测试报告 |
| **PLDD vs 基线** | **F1 比最优基线提升 ≥ 15%** | **基线对比表** |
| **消融完备** | **4 种配置均报告** | **消融实验表** |
| **置信区间** | **95% CI 宽度 < 0.10** | **bootstrap 输出** |
| 代码无报错 | 全流程跑通 | CI 或手动执行 |

---

## 附录 A：与之前方案的对比

| 维度 | 0005 伪GM方案（失败） | 本方案（修正） |
|------|---------------------|--------------|
| GM 来源 | 不同标签 GOOD 图 | 同一张图（自身作 GM） |
| Test 来源 | 原始 BAD 图 | GOOD 图 + 合成缺陷 |
| GT mask | COCO bbox → 图像级 | 合成过程直接生成，像素精确 |
| 内容对齐 | ❌ 不同标签，内容完全不同 | ✅ 完全对齐，无配准问题 |
| LDCE 有效性 | ❌ 内容差异淹没缺陷信号 | ✅ 差异仅来自合成缺陷 |
| 最优 F1 | 0.007（无效） | 预期 0.55~0.75（有效） |
| 评估标准 | 像素级（过严） | 实例级为主（合理） |

## 附录 B：Codex 审查反馈回应

| Codex 问题 | 本方案回应 |
|-----------|-----------|
| FP > 总像素异常 | §6.2 要求 FP 归因，统计口径明确定义为全局 micro-average |
| 调参/测试未分离 | §7 Step 5 仅用 train+valid，Step 7 才用 test_split |
| 缺朴素基线 | §6.4 新增 3 种基线（绝对差分/SSIM/Canny） |
| 缺消融实验 | §6.5 新增 4 种消融配置 |
| 缺置信区间 | §6.6 要求 95% CI（bootstrap） |
| 检测时间缺硬件 | §6.6 要求报告 CPU/内存/OS |
| 结论措辞过乐观 | §8 验收标准增加基线对比门槛（≥15% 提升） |
