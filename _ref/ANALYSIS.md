# HTML 课件批量转换分析

## 一、四个视觉变体颜色配置

| 变体 | 主色 | 渐变背景 | 辅助色 | 装饰元素 |
|------|------|---------|--------|---------|
| 太空冒险 | 深蓝 `#0B1026` | 星光渐变 | 星光色/银白 | 星球、火箭、星座 |
| 森林动物 | 森林绿 `#1A3A2A` | 薄雾渐变 | 浅绿/棕色 | 蘑菇、蝴蝶、树叶 |
| 海洋世界 | 海洋蓝 `#0A1628` | 水波渐变 | 浅蓝/珊瑚色 | 鱼群、珊瑚、气泡 |
| 童话城堡 | 紫色 `#2A1B3D` | 星光渐变 | 粉紫/金色 | 城堡、星星、皇冠 |

**通用设计规范：**
- 圆角 `8px` + 柔和阴影，无锐利元素
- 配色柔和不刺眼，对比度适中
- 角色大头小身（chibi风格），表情夸张友好
- 字体：圆体优先

## 二、现有课件代码结构分析（sample_courseware.html）

**结构层次：**
```
<!DOCTYPE html>
├── <head>  — meta + 内联 <style>
├── <body>
│   ├── .container  — max-width:480px, 居中
│   │   ├── .cover  — 封面卡片（标题+副标题+按钮）
│   │   └── .section — 内容区（标题+交互区+按钮）
│   └── <script> — Canvas 绘制逻辑
```

**CSS 模式：**
- 全局 reset：`*{margin:0;padding:0;box-sizing:border-box}`
- 卡片式布局：白色背景 + 圆角 20-24px + `box-shadow`
- 主色贯穿：`.cover-title` / `.section-title` / `.btn` 统一用 `#FF6B35`
- 交互区：`.interact-area` 带边框 + 浅色背景区分

**JS 模式：**
- Canvas 2D 绘制（齿轮示例）
- `requestAnimationFrame` 动画循环
- 简单交互（scrollIntoView、拖动）

## 三、三种故事类型内容特点

### 1. story_extra（中文绘本故事）
- **结构**：分站/分章叙事，用 `---` 分隔场景
- **格式**：标题 + 场景段落 + 角色对话 + 结尾感悟 + 互动问题
- **字数**：~70行，500-800字
- **模板需求**：封面页 + 多场景翻页 + 角色对话气泡 + 结尾互动页

### 2. english_story（英文故事）
- **结构**：线性叙事，单篇完整
- **格式**：标题 + 连贯段落 + 道德总结（Moral）
- **字数**：~57行，300-500词
- **模板需求**：封面页 + 全屏文本页 + 音频朗读支持 + 道德总结页

### 3. poem_explain（古诗讲解）
- **结构**：固定板块（诗句解释 / 诗人档案 / 诗的秘密 / 小故事）
- **格式**：emoji 标题 + 逐句注解 + 互动提示
- **字数**：~20行，短小精悍
- **模板需求**：古风封面页 + 诗句展示页 + 解释卡片 + 故事页 + 互动提示

## 四、TEMPLATE_CONFIG 架构设计建议

### 配置区（CONFIG）
```js
const TEMPLATE_CONFIG = {
  // 主题配置
  theme: 'space' | 'forest' | 'ocean' | 'fairy',
  title: '故事标题',
  subtitle: '副标题',
  coverEmoji: '🚀',

  // 颜色系统
  colors: {
    primary: '#0B1026',    // 主色
    secondary: '#1a237e',  // 辅助色
    accent: '#FFD700',     // 强调色
    bg: 'linear-gradient(...)', // 背景
    text: '#FFFFFF',       // 文字色
    card: '#FFFFFF'        // 卡片色
  },

  // 章节列表
  sections: [
    { type: 'cover', title, subtitle, emoji },
    { type: 'story', title, paragraphs: [...] },
    { type: 'interaction', component: 'choice-button', ... },
    { type: 'ending', questions: [...] }
  ]
}
```

### 可复用引擎区（REUSABLE）
```js
// 1. Canvas 渲染器
class CanvasRenderer { init, mount, unmount, resize, draw }

// 2. 游戏引擎（齿轮/拖拽等交互）
class GameEngine { init, mount, unmount, resize, update }

// 3. 测验引擎（选择题/判断题）
class QuizEngine { init, mount, unmount, resize, check }

// 4. 组件生命周期契约
// init(el, config) → { mount, unmount, resize, update }
```

### 组件库映射
| 故事类型 | 需要的组件 |
|---------|-----------|
| 中文绘本 | text-block, image-display, audio-player, choice-button |
| 英文故事 | text-block, audio-player（朗读）, choice-button |
| 古诗讲解 | text-block（诗句）, image-display（古风插图）, audio-player |

### 批量转换策略
1. **解析层**：读取 `.md` 文件，按 `---` 分隔场景，识别标题/对话/问题
2. **模板层**：根据文件名前缀（`story_extra_` / `english_` / `poem_explain_`）选择模板
3. **主题层**：按索引号 `01-10→太空, 11-20→森林, 21-30→海洋, 31-40→童话` 循环分配
4. **输出层**：生成完整 HTML，内联 CSS+JS，单文件可独立运行
