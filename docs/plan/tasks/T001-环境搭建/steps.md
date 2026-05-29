# T001 — 环境搭建与数据准备

> 优先级：P0 | 状态：✅ done | 前置任务：无
> 完成日期：2026-05-09

## 目标

建立项目目录结构、Python 虚拟环境、合成数据集和工具函数。

## Steps

### 1. 项目骨架
- [x] 创建 `Project/Label_Detect/` 目录结构（src/, tests/, scripts/, utils/, calibration/）
- [x] 创建 `requirements.txt`（opencv-python, numpy, Pillow, matplotlib, scikit-learn, pytest）
- [x] 创建 `.venv/` 虚拟环境并安装依赖
- [x] 创建 `conftest.py`（sys.path 配置）
- [x] 创建 `src/config.py`（参数定义 + `get_params()` 动态传递）

### 2. 合成数据集
- [x] `scripts/build_synthetic_data.py`：生成 200 对 512×512 合成标签图
- [x] 三类缺陷注入：漏印（underprint）、过印（overprint）、划痕（scratch）
- [x] 同步生成像素级 GT 掩码 + meta.json

### 3. DAGM 2007 数据集
- [x] 用户下载到 `Data/archiveDAGM2007_raw/`（Class10，1151+1151 张）
- [x] `scripts/prepare_dagm.py` 整理为 PLDD 兼容格式
- [x] 输出到 `Data/DAGM2007/`（gm/、test/、gt/、meta.json）

### 4. 工具函数
- [x] `utils/vis.py`：load_image、save_image、show_grid、show_heatmap、overlay_mask

## Acceptance

- [x] `.venv/Scripts/python -c "import cv2; print(cv2.__version__)"` 通过
- [x] `Data/synthetic/` 下有 200 对图像 + meta.json
- [x] `Data/DAGM2007/` 下有整理后的图像
- [x] 所有模块可 import 无报错

## 实际耗时

约 1 小时
