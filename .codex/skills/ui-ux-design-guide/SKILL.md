---
name: ui-ux-design-guide
description: UI/UX 设计指南，包含风格数据库、配色、字体、图表、UX 规范和框架最佳实践
---

# UI/UX 设计指南

可搜索的 UI 风格、配色方案、字体搭配、图表类型、产品建议、UX 规范和框架最佳实践数据库。

## 使用场景

当用户要求 UI/UX 工作时（设计、构建、创建、实现、审查、修复、改进），遵循以下流程：

### Step 0：先看现有代码

如果用户在改进**已有** UI（非全新项目）：
- 先读取当前 UI 代码及其约束（组件/模板、CSS、设计系统、路由、数据流）
- 提出 1-2 个具体视觉方向，然后用实际代码变更实现最佳方案
- 只在理解当前 UI 后才使用搜索工具补充配色/字体/布局参考

### Step 1：分析用户需求

提取关键信息：
- **产品类型**：SaaS、电商、作品集、仪表盘、落地页等
- **风格关键词**：极简、活泼、专业、优雅、暗色模式等
- **行业**：医疗、金融、游戏、教育等
- **技术栈**：React、Vue、Next.js，默认 `html-tailwind`

### Step 2：搜索相关领域

```bash
python3 <path-to-skill>/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

推荐搜索顺序：
1. `product` — 产品类型建议
2. `style` — 详细风格指南
3. `typography` — 字体搭配
4. `color` — 配色方案
5. `landing` — 页面结构（落地页场景）
6. `chart` — 图表推荐（仪表盘/分析场景）
7. `ux` — 最佳实践和反模式
8. 指定 `--stack` 获取框架特定指南

### Step 3：交付前检查清单

- [ ] 不用 emoji 做 UI 图标（用 SVG）
- [ ] 所有可点击元素有 `cursor-pointer`
- [ ] 悬停状态提供视觉反馈
- [ ] 过渡动画平滑（150-300ms）
- [ ] 亮色模式文字对比度 ≥ 4.5:1
- [ ] 玻璃/透明元素在亮色模式下可见
- [ ] 固定导航栏不遮挡内容
- [ ] 响应式：320px / 768px / 1024px / 1440px
- [ ] 所有图片有 alt 文本
- [ ] 表单输入有 label

## 可用领域

| 领域 | 用途 | 示例关键词 |
|------|------|-----------|
| `product` | 产品类型推荐 | SaaS, e-commerce, portfolio |
| `style` | UI 风格、配色、效果 | glassmorphism, minimalism, dark mode |
| `typography` | 字体搭配、Google Fonts | elegant, playful, professional |
| `color` | 按产品类型的配色方案 | saas, ecommerce, healthcare |
| `landing` | 页面结构、CTA 策略 | hero, testimonial, pricing |
| `chart` | 图表类型、库推荐 | trend, comparison, funnel |
| `ux` | 最佳实践、反模式 | animation, accessibility, loading |

## 可用技术栈

| 技术栈 | 侧重点 |
|--------|--------|
| `html-tailwind` | Tailwind 工具类、响应式、无障碍（默认） |
| `react` | State、hooks、性能、模式 |
| `nextjs` | SSR、路由、图片、API routes |
| `vue` | Composition API、Pinia、Vue Router |
| `svelte` | Runes、stores、SvelteKit |
