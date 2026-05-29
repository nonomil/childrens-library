# T010 验收标准 — 128课件差异修复

> 方法论：AutoResearchClaw CoPilot 模式
> 验收方式：自动化脚本（Python）+ 浏览器手动验证
> **验证注册表规则**：所有数字来自 `python test_all.py` 或 `python verify_gap_fix.py` 实际输出

---

## 自动化验收（统一用 Python 脚本，兼容 Windows）

### 主测试

```bash
python test_all.py
```

**预期输出**：`128/128 passed`

### 差异修复专项验证

```bash
python verify_gap_fix.py --check all
```

**预期输出**：
```
[CSS-THEME]    128/128 files using var(--bg)
[ONERROR]      128/128 files have onerror handler
[UNLOCK]       PASS (math requires english>=3)
[PET-FOOD]     PASS (6 pets have preferredFood)
```

### 验证指标

| 指标 | 验证脚本 | 目标值 | 判定 |
|------|---------|--------|------|
| 总文件数 | `test_all.py` 输出 | 128 | 精确匹配 |
| 测试通过率 | `test_all.py` 输出 | 128/128 | 精确匹配 |
| CSS主题变量生效 | `verify_gap_fix.py --check css-theme` | 128/128 | ≥125/128 |
| onerror降级 | `verify_gap_fix.py --check onerror` | 128/128 | ≥125/128 |
| 解锁逻辑 | `verify_gap_fix.py --check unlock` | PASS | 精确匹配 |
| 宠物偏好食物 | `verify_gap_fix.py --check pet-food` | PASS | 精确匹配 |

---

## 浏览器手动验收（量化标准）

### 村庄系统

| 验收项 | 量化标准 | 状态 |
|--------|---------|------|
| village.html 加载 | Console error count = 0（F12→Console→筛选Error→计数为0） | ⬜ |
| 6个建筑可点击 | 点击每个建筑→弹出面板→显示课件列表 | ⬜ |
| Steve 行走动画 | 每秒移动≥10px，到达边界自动转向 | ⬜ |
| Steve 点击说话 | 点击后0.5s内出现气泡，3s后自动消失 | ⬜ |
| 每日任务板 | 显示任务文本 + 奖励星数 + 状态 | ⬜ |

### 课件主题（4种类型各1个样本）

| 文件 | data-type | 预期背景色 | CSS变量 | 状态 |
|------|-----------|-----------|---------|------|
| twinkle-twinkle.html | nursery | #FFF9E6 暖黄 | `var(--bg)` | ⬜ |
| story-block-battle.html | story | #FFF8F0 暖白 | `var(--bg)` | ⬜ |
| gears-transmission.html | science | #F0F8FF 蓝白 | `var(--bg)` | ⬜ |
| english-01-hello.html | courseware | #FAFAFA 纯白 | `var(--bg)` | ⬜ |

### 解锁逻辑

| 测试步骤 | 预期结果 | 状态 |
|---------|---------|------|
| localStorage 清空，刷新 village.html | 数学集市锁定，科学实验室锁定 | ⬜ |
| 手动设置 zones.english.totalCompleted=3 | 数学集市解锁 | ⬜ |
| 手动设置总完成=5（任意学科） | 科学实验室解锁 | ⬜ |

### 宠物偏好食物

| 测试步骤 | 预期结果 | 状态 |
|---------|---------|------|
| 选择猫，喂面包 | 成长+5 | ⬜ |
| 选择猫，喂鱼（偏好食物） | 成长+10，显示"喜欢！" | ⬜ |

### 完成流程

| 测试步骤 | 预期结果 | 状态 |
|---------|---------|------|
| 完成任意课件 | 显示星星 + "返回村庄"按钮 + "+N 金币" | ⬜ |
| 点击返回村庄 | village.html 打开，进度+1 | ⬜ |

### 响应式

| 断点 | 预期 | 状态 |
|------|------|------|
| 768px | 建筑2列布局，面板全宽 | ⬜ |
| 480px | 建筑1列布局，字号≥14px | ⬜ |

---

## 验证脚本待创建

> `verify_gap_fix.py` 需在 T10-01 开始前创建，作为所有子任务的统一验收工具。

---

## 签收

| 角色 | 签收 | 日期 |
|------|------|------|
| AI（CC） | ⬜ | |
| 用户 | ⬜ | |
