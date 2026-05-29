# DL 实验报告工作流规范

> 适用范围：所有深度学习训练/推理实验（PatchCore / EfficientAD / RT-DETR / YOLO 等）
> 核心模块：`Project/DL/report_generator.py`
> 输出目录：`Docs/测试报告/`

---

## 1. 触发条件

**触发方**：AI 工作流（CC），不由训练脚本触发。训练脚本保持纯净。

| 触发方式 | 说明 |
|---------|------|
| **CC 自动触发（默认）** | CC 完成 DL 训练任务（`engine.train` / `python train_*.py` 完成）后，主动调用 `report_generator.py` |
| **用户说"生成实验报告"** | CC 识别意图后立即调用 |
| **用户说"跳过报告"** | CC 跳过本步骤，标注 `[报告未生成]` |

**CC 调用方式（标准命令）**：

```bash
cd E:\Project_LM\SPC_Floor\Project\DL
.venv\Scripts\python.exe report_generator.py \
    --task-id T003 \
    --algorithm PatchCore \
    --dataset "MVTec AD Wood" \
    --dataset-root "E:\Project_LM\SPC_Floor\Data\DL_OpenSource_Dataset\MVTec_AD\wood" \
    --output-dir "outputs\patchcore_wood" \
    --results-tsv "outputs\patchcore_wood\results.tsv" \
    --best-exp-json "outputs\patchcore_wood\results.json" \
    --inference-images-dir "outputs\patchcore_wood\inference_images"
```

---

## 2. 报告模板（10 节）

所有 DL 实验报告必须包含以下章节（允许额外章节）：

| # | 章节 | 内容要求 | 数据来源 |
|---|------|---------|---------|
| 1 | 元数据 | 日期/算法/数据集/GPU/最佳AUROC | 自动 |
| 2 | 算法概述 | 算法描述、核心原理 | 自动填充算法名 |
| 3 | 数据集详情 | 路径/名称/各子目录图片数 | `dataset_root` 自动统计 |
| 4 | 代码路径与运行命令 | 训练/推理脚本路径 | `output_dir` 自动扫描 |
| 5 | 模型输出 | 权重文件/结果文件清单 | `output_dir` 自动扫描 |
| 6 | 实验结果 | TSV 全量表格 + 最佳实验详情 | `results.tsv` + JSON |
| 7 | 推理结果图片 | 按类别嵌入，每类 ≤3 张 | `inference_images_dir` |
| 8 | 算法特定章节 | 模型架构/参数/特殊分析 | `extra_sections` 参数 |
| 9 | 关键发现与结论 | 最佳AUROC/实验数/核心发现 | 自动 + 人工补充 |
| 10 | 附录：文件清单 | 报告/TSV/JSON 路径 | 自动 |

---

## 3. 输出路径与命名规范

### 文件命名

```
Docs/测试报告/YYYY-MM-DD-{task_id}-{algorithm}-详细报告.md
```

示例：
- `Docs/测试报告/2026-04-16-T003-PatchCore-详细报告.md`
- `Docs/测试报告/2026-04-16-T007-EfficientAD-详细报告.md`

### 推理图片目录

```
Project/DL/outputs/{algorithm}_{dataset}/inference_images/{category}/
```

---

## 4. 图片嵌入规则

- 按缺陷/类别分子目录展示
- 每类嵌入 ≤3 张典型图片
- 使用相对路径引用
- 无图片时输出 `[无推理图片]` 占位

---

## 5. CC 工作流步骤

### 训练完成后（CC 标准动作）

```
1. 确认训练脚本已输出 results.tsv 和 exp_{tag}.json
2. 检查推理图片目录是否存在（outputs/{algorithm}_wood/inference_images/）
   - 不存在时：提示用户运行可视化脚本（如 inference_patchcore.py），或跳过图片节
3. 调用 report_generator.py CLI（见第1节命令模板）
4. 确认报告生成在 Docs/测试报告/ 下
5. 执行质量门禁检查
```

### 各算法参数表

| 算法 | task_id | output_dir | results_tsv | inference_images_dir |
|------|---------|-----------|-------------|---------------------|
| PatchCore | T003 | `outputs/patchcore_wood` | `outputs/patchcore_wood/results.tsv` | `outputs/patchcore_wood/inference_images` |
| EfficientAD | T007 | `outputs/efficientad_wood` | `outputs/efficientad_wood/results.tsv` | `outputs/efficientad_wood/*/` （Anomalib 自动生成） |
| FFT-Demo | T002 | `outputs/fft_demo` | `outputs/fft_demo/results.tsv` | `outputs/fft_demo`（根目录图片） |

---

## 6. 质量门禁

报告生成后自动检查：

- [ ] 所有 10 节非空
- [ ] 至少嵌入 3 张推理图片（或标注无图片原因）
- [ ] TSV 数据与报告表格数值一致
- [ ] 报告行数 ≥50 行
- [ ] 文件名符合命名规范

---

## 7. 新训练脚本接入清单

添加新的 DL 训练脚本时，需要：

1. 确保脚本输出 `results.tsv` 和 `exp_{tag}.json`
2. 在本文件第 5 节"各算法参数表"中新增一行
3. **不需要**在训练脚本中添加任何报告相关代码（训练脚本保持纯净）
4. （可选）创建推理可视化脚本（`inference_{algorithm}.py`），供用户在训练后运行
5. 训练完成后，CC 按第 5 节步骤自动触发报告生成