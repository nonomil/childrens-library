# 🎪 小朋友的互动学习乐园 — Children's Interactive Learning Courseware

> **115+ 交互式 HTML 课件** · 适用于 5-7 岁幼儿 · 触摸屏/键盘双模式 · 零服务器依赖

[![GitHub Pages](https://img.shields.io/badge/🌐-在线体验-4CAF50)](https://nonomil.github.io/childrens-library/)
[![课件数](https://img.shields.io/badge/📚-115+_课件-2196F3)](docs/courseware/)
[![开源](https://img.shields.io/badge/📖-开源学习项目-FF5722)](LICENSE)

---

## 📖 这是什么？

一个**纯前端的幼儿互动课件库**，所有课程都是独立 HTML 文件，**打开即用、无需联网、零加载等待**。

### 核心理念

| 特点 | 说明 |
|:--|:--|
| 🎯 **一页一课** | 每个 HTML 就是一节课，直接打开就能学 |
| 🚀 **零依赖** | 纯前端，只需一个浏览器 |
| 🖱️ **触摸优先** | 专为平板/触屏设计，也支持键鼠 |
| 🎤 **语音驱动** | 所有文字可点击朗读，适配不识字的低龄儿童 |
| 🧱 **Minecraft 主题** | Steve & Alex 引导学习，情境式教学 |
| 🎮 **游戏化** | 配对、闯关、测验、彩纸庆祝 |

---

## 📚 课件分类

### 🔤 英语启蒙（25 课）
| 系列 | 内容 | 课号 |
|:--|:--|:--|
| **Minecraft Hello!** | 打招呼、名字、问候 | 01–05 |
| **Minecraft 主题** | 家庭、动物、身体、食物、玩具 | 06–10 |
| **Minecraft 进阶** | 天气、衣服、动作、地点、情绪 | 11–17 |
| **Minecraft 故事** | 复习、走失的猫、暴风雨、生日派对、农场、寻宝 | 18–24 |

### 🀄 语文/中文（25 课）
| 系列 | 内容 | 课号 |
|:--|:--|:--|
| **象形识字** | 天地人、大自然、家庭、学校 | 01–06 |
| **拼音王国** | 拼音入门、声母、韵母 | 07–12 |
| **主题识字** | 身体、颜色、食物、动作、方向、动物 | 13–18 |
| **进阶阅读** | 复合词、短句、反义词、问答、古诗、大冒险 | 19–24 |

### 🔢 数学启蒙（25 课）
- 数数 1~10、数到 20
- 比大小、认识加法、减法
- 20 以内进退位
- 图形、测量、钱币、钟表
- 统计、位置、乘法启蒙、分数
- 应用题挑战、数学嘉年华

### 🎵 英语童谣（27 首）
Twinkle Twinkle · Old MacDonald · Wheels on the Bus · Five Little Monkeys · BINGO · ABC Song · Head Shoulders · Humpty Dumpty · If You're Happy · London Bridge · Mary's Little Lamb · Jack and Jill · 以及更多...

### 🌱 科学/自然（4 课）
- 齿轮传动原理（STEM 互动）
- 雨林大冒险（点触探索）
- 大自然识字（云雨风雪星花草虫鸟）

### 📖 绘本故事
- 英文绘本 + 互动课件
- 双语对照逐页阅读

---

## 🚀 快速开始

### 在线体验
访问 [https://nonomil.github.io/childrens-library/](https://nonomil.github.io/childrens-library/)

### 本地使用
```bash
git clone https://github.com/nonomil/childrens-library.git
cd childrens-library/docs/courseware
# 直接用浏览器打开任意 .html 文件
open english-01-hello.html
```

### 本地启动服务
```bash
cd docs/courseware
python3 -m http.server 8080
# 访问 http://localhost:8080/english-01-hello.html
```

---

## 🛠 技术栈

| 技术 | 用途 |
|:--|:--|
| **原生 HTML/CSS/JS** | 每课一个独立 HTML |
| **GSAP 3.12** | 页面过渡动画、彩纸庆祝效果 |
| **Web Speech API** | 文字朗读 TTS |
| **MP3 音频** | 优先使用本地音源，TTS 作为后备 |
| **WebP 图片** | 所有图片压缩为 WebP，节省 90%+ 带宽 |
| **Google Fonts** | Nunito（教材）/ Fredoka One（童谣） |

### 共享工具库
`docs/courseware/shared/courseware.js` 提供可选的公共功能：
- `playClick()` — MP3 播放 + TTS 降级
- `speakPage()` — 整页朗读
- `celebrate()` — GSAP 彩纸庆祝
- `navGoTo/navPrev/navNext` — 翻页导航（可选）
- `initSwipe()` — 触摸滑动支持（可选）

---

## 📂 项目结构

```
childrens-library/
├── docs/
│   ├── index.md                    # MkDocs 首页
│   ├── courseware/                 # 🎯 全部课件 HTML
│   │   ├── shared/                 # 共享 JS/CSS 库
│   │   │   ├── courseware.js
│   │   │   └── courseware.css
│   │   ├── images/                 # WebP 图片资源
│   │   ├── english-01-hello.html
│   │   ├── chinese-04-nature.html
│   │   └── ... (115+ 课件)
│   ├── books/                      # 绘本清单
│   └── images/                     # 网站用图
├── scripts/                        # 生成/转换脚本
├── mkdocs.yml                      # MkDocs 配置
└── README.md                       # 👈 你现在在看这个
```

---

## 📊 统计数据

| 指标 | 数值 |
|:--|:--|
| 课件总数 | 115+ |
| 代码行数 | ~120,000 |
| 图片文件 | 423+ (全部 WebP) |
| 共享 JS 库 | 133 行 |
| 覆盖科目 | 英语 · 中文 · 数学 · 童谣 · 科学 · 绘本 |

---

## 🧑‍💻 参与贡献

- 发现 Bug？[提 Issue](https://github.com/nonomil/childrens-library/issues)
- 想改进课件？Fork 后 PR
- 想了解课件制作方法？看 [COURSEWARE-METHODOLOGY.md](docs/COURSEWARE-METHODOLOGY.md)

---

## 📜 许可

本项目为个人学习项目，课件内容仅供教育参考使用。

---

*用爱发电 · 为小朋友做的互动学习乐园* 🎪
