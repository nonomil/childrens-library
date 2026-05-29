# T203 — v1.2 Bug Fix + 参数优化

> 优先级：P0 | 状态：🔄 doing | 前置任务：T202
> 开始日期：2026-05-10

## 目标

修复三项结构性 bug（m_j 符号、M_bg RGB 梯度、M_bg 接入匹配链路），然后通过 T_score 参数扫描提升 F1 至 ≥ 0.70。

## Codex 审查记录

- 第一轮：Fix-1 (F=0→F=1) FAIL → 移除，改为参数策略
- 第二轮：Fix-1 (np.abs) PASS, Fix-2 (RGB) PASS, Fix-3 (M_bg) PASS, Fix-4 (T_score) PARTIAL
- 整体判定：论文忠实，可执行

## Steps

### 1. Fix-1: m_j 加 np.abs()（icsm.py）
- [ ] 修改 `icsm.py` 第 65 行：`m_j = np.abs(mt - mg)`
- [ ] 验证：m_j 始终 ≥ 0

### 2. Fix-2: M_bg 用 RGB 平均梯度（mask.py）
- [ ] 修改 `generate_bg_mask()` 使用 `compute_rgb_gradient()` 替代灰度 Sobel
- [ ] 验证：纯色图像 bg_mask 全 0

### 3. Fix-3: M_bg 接入 matching.py
- [ ] 导入 `generate_bg_mask`
- [ ] 在 `detect_defects()` 中生成 bg_mask
- [ ] effective_mask = candidate_mask & bg_mask
- [ ] 用 effective_mask 替换 candidate_mask
- [ ] 验证：effective_mask = candidate AND bg_mask

### 4. 单元测试
- [ ] test_m_j_has_abs: m_j 始终 ≥ 0
- [ ] test_m_j_branch_fires: np.abs 后 m_j > T_m 分支可触发
- [ ] test_bg_mask_uses_rgb: 彩色图与灰度图 bg_mask 结果不同
- [ ] test_effective_mask_is_intersection: effective = candidate AND bg_mask
- [ ] test_detect_defects_with_bg_mask: bg_mask 过滤后轮廓/输出变化

### 5. 集成评估
- [ ] 固定参数基线：T_filter=5, T_score=0.6, T_r=0.1, T_m=50, t_bg=10
- [ ] 200 张合成数据评估（默认参数）
- [ ] T_score 扫描：[0.3, 0.4, 0.5, 0.6]
- [ ] 回归验证：F1 > 0.516，Precision ≥ 0.85
- [ ] 记录 F1/P/R/IoU 到 results.json

### 6. Codex 代码审查
- [ ] 提交改动给 Codex 独立审查
- [ ] 修复审查发现的问题

## Acceptance

- [ ] F1 > 0.516（baseline）
- [ ] 目标 F1 ≥ 0.70
- [ ] Codex 代码审查 PASS
- [ ] 4 个新单元测试全部通过
