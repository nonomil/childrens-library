# HTML 课件模板系统使用说明

## 概述

模板系统提供四种主题风格的 HTML 课件模板，支持三种故事类型（中文绘本、英文故事、古诗讲解），单文件可独立运行。

## 模板文件

| 模板 | 主题 | 主色 | 强调色 |
|------|------|------|--------|
| `template_space.html` | 太空冒险 | 深蓝 `#0B1026` | 星光金 `#FFD700` |
| `template_forest.html` | 森林动物 | 森林绿 `#1A3A2A` | 浅绿 `#8BC34A` |
| `template_ocean.html` | 海洋世界 | 海洋蓝 `#0A1628` | 珊瑚绿 `#4DD4AC` |
| `template_fairy.html` | 童话城堡 | 紫色 `#2A1B3D` | 金色 `#FFB74D` |

## 模板结构

每个模板包含以下核心组件：

### 1. TEMPLATE_CONFIG 配置区
```js
const TEMPLATE_CONFIG = {
  theme: 'space',           // 主题标识
  title: '故事标题',         // 课件标题
  subtitle: '副标题',       // 副标题
  colors: {                 // 颜色系统
    primary, secondary, accent, text, card
  },
  decorations: [...]        // 主题装饰元素
};
```

### 2. CanvasRenderer 渲染器
用于 Canvas 绑定的动画和图形绘制。

```js
const renderer = new CanvasRenderer('canvasId');
renderer.mount();
renderer.animate((ctx, canvas) => {
  // 绘制逻辑
});
renderer.unmount();
```

### 3. QuizEngine 测验引擎
支持选择题交互，自动计分。

```js
const quiz = new QuizEngine('containerId');
quiz.init([
  { question: '问题', options: ['A', 'B', 'C'], answer: 0 }
]);
quiz.mount();
```

### 4. StoryEngine 故事引擎
支持三种故事类型的渲染。

```js
const story = new StoryEngine('containerId');
story.init('chinese', [     // 类型: chinese/english/poem
  { type: 'text', title: '章节', content: '内容', emoji: '📖' },
  { type: 'dialogue', title: '对话', lines: [{name: '角色', text: '台词'}] },
  { type: 'poem', title: '诗句', lines: ['诗句1', '诗句2'], explain: '解释' }
]);
story.mount();
```

## 占位符说明

| 占位符 | 说明 |
|--------|------|
| `{{TITLE}}` | 课件标题 |
| `{{SUBTITLE}}` | 副标题 |
| `{{COVER_EMOJI}}` | 封面图标 emoji |
| `{{CONTENT_SECTIONS}}` | 内容区域 HTML |

## 主题分配策略

根据文件索引号循环分配主题：
- 01-10 → 太空 (space)
- 11-20 → 森林 (forest)
- 21-30 → 海洋 (ocean)
- 31-40 → 童话 (fairy)

## 使用流程

1. 选择合适的主题模板
2. 替换占位符为实际内容
3. 在 `<script>` 中初始化引擎并填充数据
4. 保存为独立 HTML 文件

## 批量转换

```python
# 伪代码示例
for story in stories:
    theme = get_theme_by_index(story.index)
    template = load_template(f'template_{theme}.html')
    html = template.replace('{{TITLE}}', story.title)
    # ... 其他替换
    save(f'{story.filename}.html', html)
```
