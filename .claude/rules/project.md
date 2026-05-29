# 项目架构（Label_Defect）

## 项目来源

基于论文 "Printed label defect detection using twice gradient matching based on improved cosine similarity measure" (Expert Systems With Applications, 2022) 的复现与研究项目。

## 技术栈
Python 3.10+ / OpenCV / NumPy / Pillow

## 入口点
- `src/` — 核心算法实现
- `tests/` — pytest 测试
- `scripts/` — 实验脚本

## 核心算法（PLDD 框架）
| 模块 | 职责 |
|------|------|
| 图像配准 | shape-based template matching 对齐 GM 与测试图 |
| LDCE | 潜在缺陷候选提取（RGB 子图滑动 + 色差近似 + 二值化 + 形态学） |
| 梯度匹配 | 二次梯度匹配（改进余弦相似度 + Mask 机制） |
| 缺陷判定 | 漏印/过印同时检测 |

## 架构约束
- 算法实现与实验脚本分离
- 不依赖 GPU，CPU 实时检测
- 不引入 PyTorch/TensorFlow 等深度学习框架（传统 CV 方法）

## 图像处理规范
- 合并前统一颜色空间转换
- 资源用 `with` 语句管理
- 允许的文件格式：`.jpg` / `.jpeg` / `.png` / `.bmp` / `.tiff`

## 关键测试场景
- GM 与测试图的配准精度
- 伪影消除效果（非刚性变形）
- 漏印/过印检测
- 颜色偏差检测
- 不同缺陷类型的 F1/Precision/Recall

## 输出验证
- 检测结果与标注对比（F1, Precision, Recall）
- 检测时间 < 0.3s（CPU）
