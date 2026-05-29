# T010 — 128课件差异修复 · 任务拆分与验收计划

> 创建：2026-05-29
> 方法论：AutoResearchClaw CoPilot 模式（6个人类介入节点）
> 总任务：8个独立子任务，可并行
> 验收：每个任务完成后运行 test_all.py，128/128 通过

---

## 总览

| ID | 任务 | 优先级 | 状态 | 预估 | 依赖 |
|----|------|--------|------|------|------|
| T10-01 | CSS主题变量系统 | P1 | ⬜ | 30min | G1 |
| T10-02 | 解锁逻辑修正 | P1 | ⬜ | 15min | G1 |
| T10-03 | 宠物偏好食物机制 | P1 | ⬜ | 20min | G4 |
| T10-04 | Steve精灵图动画 | P0 | ⬜ | 45min | G3 |
| T10-05 | 3个占位故事补内容 | P0 | ⬜ | 60min | G5 |
| T10-06 | 像素风进度条 | P2 | ⬜ | 15min | G1 |
| T10-07 | 金币浮动动画 | P2 | ⬜ | 15min | G1 |
| T10-08 | onerror图片降级 | P2 | ⬜ | 20min | G1 |

**总预估**：~3.5小时（不含人类等待时间）

---

## T10-01：CSS主题变量系统

### 需求
在 `shared/courseware.css` 中按 `[data-type]` 定义4套CSS变量主题，使128个课件自动获得对应配色。

### 实现步骤（两步验收）
**第一步：定义变量**
- [ ] 1. 编辑 `shared/courseware.css`，添加 `html[data-type="nursery"]` 选择器（用 `html[data-type]` 提升特异性，覆盖内联样式）
- [ ] 2. 添加 `html[data-type="story"]` 选择器
- [ ] 3. 添加 `html[data-type="science"]` 选择器
- [ ] 4. 添加 `html[data-type="courseware"]` 选择器
- [ ] 5. 每个选择器定义：`--bg`, `--primary`, `--accent`, `--text`, `--card-bg`

**第二步：确保实际生效**
- [ ] 6. 修改各类型代表文件的 `body` 背景：从硬编码颜色改为 `background: var(--bg)`
- [ ] 7. 抽样验证：浏览器打开4种类型各1个文件，确认背景色来自CSS变量
- [ ] 8. 全量扫描：`python verify_gap_fix.py --check css-theme` 确认128文件的body背景使用`var(--bg)`

### CSS变量方案

```css
[data-type="nursery"] {
  --bg: #FFF9E6; --primary: #FF9800; --accent: #FFB347;
  --text: #5A3E2B; --card-bg: #FFF8E7;
}
[data-type="story"] {
  --bg: #FFF8F0; --primary: #E8751A; --accent: #FFB347;
  --text: #6B4F3A; --card-bg: #FFFCF5;
}
[data-type="science"] {
  --bg: #F0F8FF; --primary: #2196F3; --accent: #4FC3F7;
  --text: #333; --card-bg: #E3F2FD;
}
[data-type="courseware"] {
  --bg: #FAFAFA; --primary: #4CAF50; --accent: #81C784;
  --text: #333; --card-bg: #fff;
}
```

### 验收标准
- [ ] `python verify_gap_fix.py --check css-theme` → 128/128
- [ ] 浏览器打开 twinkle-twinkle.html（nursery）→ 暖黄背景
- [ ] 浏览器打开 story-block-battle.html（story）→ 暖白背景
- [ ] 浏览器打开 gears-transmission.html（science）→ 蓝白背景
- [ ] 浏览器打开 english-01-hello.html（courseware）→ 纯白背景
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-02：解锁逻辑修正

### 需求
数学集市：完成3课**英语**解锁（当前是总完成3课）
科学实验室：完成5课**任意**（当前逻辑正确，无需改）

### 实现步骤
- [ ] 1. 编辑 `shared/village.js` 的 `isZoneUnlocked()` 函数
- [ ] 2. 添加 `requiredZone` 字段到 ZONE_CONFIG
- [ ] 3. 数学集市：`unlockRequirement: 3, requiredZone: 'english'`
- [ ] 4. 修改解锁检查逻辑：检查特定zone而非总完成数
- [ ] 5. 更新锁定提示信息

### 验收标准
- [ ] 英语完成0课 → 数学集市锁定，提示"还需完成3课英语"
- [ ] 英语完成3课 → 数学集市解锁
- [ ] 总完成5课 → 科学实验室解锁（不论哪个学科）
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-03：宠物偏好食物机制

### 需求
每种宠物有偏好食物，喂偏好食物成长值×2。

### 实现步骤
- [ ] 1. 在 PET_TYPES 中添加 `preferredFood` 字段
- [ ] 2. 猫偏好鱼🐟，狗偏好骨头🦴，鹦鹉偏好种子，狐狸偏好浆果，兔子偏好胡萝卜🥕，熊猫偏好竹子🎋
- [ ] 3. 修改 `feedPet()` 函数，检查是否偏好食物
- [ ] 4. 偏好食物成长值×2，显示"喜欢！"提示
- [ ] 5. 商店添加对应食物项

### 验收标准
- [ ] PET_TYPES 每个有 `preferredFood` 字段
- [ ] 喂偏好食物 → 成长值翻倍 + 显示"喜欢！"动画
- [ ] 喂普通食物 → 正常成长值
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-04：Steve精灵图动画

### 需求（需G3决策）
用CSS绘制像素风Steve，4帧行走动画。

### 方案A：纯CSS像素Steve（推荐）
- [ ] 1. 在 village.css 中用 CSS grid 画 16×16 像素 Steve
- [ ] 2. 定义4帧行走动画（左脚/直立/右脚/直立）
- [ ] 3. 用 `@keyframes` 实现帧切换
- [ ] 4. 鼠标悬停/点击时切换动画状态
- [ ] 5. Alex 同理

### 方案B：Canvas绘制
- [ ] 1. village.js 中用 canvas 画像素角色
- [ ] 2. requestAnimationFrame 驱动动画

### 方案C：保持emoji + GSAP动画（最低成本）
- [ ] 1. 给 emoji 🧑 添加 GSAP 行走动画（左右摆动 + 上下弹跳）
- [ ] 2. 添加转向效果（scaleX: -1）

### 验收标准
- [ ] Steve 有可见的行走动画（非静止）
- [ ] 点击 Steve 触发说话气泡
- [ ] Steve 到达边界自动转向
- [ ] 移动端触摸响应正常
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-05：3个占位故事补内容

### 需求（G5决策后执行，单一路径）
space-d2/d3/d4 三个文件当前只有emoji占位。

> **范围裁剪**：不提供删除选项。删除文件违反项目协作规范（禁止自动删除），且17→14会破坏故事屋完整性。唯一方案：补内容。

### 实现步骤
- [ ] 1. story-space-d2.html：宇宙飞船冒险（8页，中英双语）
- [ ] 2. story-space-d3.html：恐龙星球探险（8页，中英双语）
- [ ] 3. story-space-d4.html：太空城市生活（8页，中英双语）
- [ ] 4. 每页配 SVG 场景插图
- [ ] 5. 最后一页有 celebrate() + burstConfetti()

### 验收标准
- [ ] 每个文件有 ≥8 个 page 对象
- [ ] 每页有中英双语文字
- [ ] 每页有 SVG 场景
- [ ] 最后一页调用 celebrate()
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-06：像素风进度条

### 需求
将圆角渐变进度条替换为像素风分段条。

### 实现步骤
- [ ] 1. 编辑 village.css 的 `.progress-bar` 样式
- [ ] 2. 添加 `image-rendering: pixelated`
- [ ] 3. 用分段色块替代渐变
- [ ] 4. 添加像素风边框（2px solid #8B6914）

### 验收标准
- [ ] 进度条有明显分段感
- [ ] 与村庄像素风格一致
- [ ] 进度变化动画流畅
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-07：金币浮动动画

### 需求
完成课件时显示 `+N 金币` 浮动上升消失动画。

### 实现步骤
- [ ] 1. 编辑 village-reporter.js 的 `showReturnButton()` 函数
- [ ] 2. 添加金币浮动 div（金色文字 `+N`）
- [ ] 3. CSS动画：从底部浮起 + 淡出
- [ ] 4. 1.5秒后自动移除

### 验收标准
- [ ] 完成课件后出现 `+5 金币` 浮动文字
- [ ] 文字金色，从下往上飘动
- [ ] 1.5秒后消失
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## T10-08：onerror图片降级

### 需求
所有 `<img>` 标签添加 onerror 降级处理。

### 实现步骤
- [ ] 1. 扫描所有128个HTML文件，找出缺少onerror的img标签
- [ ] 2. 生成批量修复脚本
- [ ] 3. 添加 onerror="this.style.background='#f0f0f0';this.alt='图片加载中';this.onerror=null"
- [ ] 4. 对于GitHub图片URL，添加raw格式检查

### 验收标准
- [ ] `python verify_gap_fix.py --check onerror` → 128/128
- [ ] 图片加载失败时显示降级UI而非broken icon
- [ ] `python test_all.py` → 128/128 通过

### 自愈记录
| 轮次 | 错误 | 诊断 | 修复 |
|------|------|------|------|
| — | — | — | — |

---

## 最终验收清单（G6）

- [ ] `python test_all.py` → 128/128 通过
- [ ] village.html 浏览器打开正常
- [ ] 6个建筑可点击，课件列表正确
- [ ] Steve 有行走动画
- [ ] 完成课件→返回村庄→进度更新→金币动画
- [ ] 4种data-type有不同主题色
- [ ] 数学需英语3课才解锁
- [ ] 宠物喂偏好食物有提示
- [ ] 3个原占位故事有实际内容
- [ ] 移动端480px/768px响应式正常

---

## 经验库条目（完成后写入 .claude/memory/lessons/）

| ID | 教训 | 来源 |
|----|------|------|
| L-gap-01 | CSS变量应集中定义在shared文件，不应各文件内联 | T10-01 |
| L-gap-02 | 解锁逻辑需支持检查特定zone完成数 | T10-02 |
| L-gap-03 | 图片必须有onerror降级，GitHub图片需raw格式 | T10-08 |
