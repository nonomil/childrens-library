# 幼儿绘本教材 HTML 课件编写方法指南

> 基于 childrens-library 项目（115+ 课件）的实践经验总结  
> 适用于 5-7 岁幼儿的交互式 HTML 课件开发

---

## 一、设计原则

### 1.1 核心理念

| 原则 | 说明 |
|:--|:--|
| **一页一课** | 每课一个独立 HTML，不依赖后端 |
| **零加载等待** | 所有资源内联/CDN，打开即用 |
| **离线可玩** | 纯前端，无服务器依赖 |
| **触摸优先** | 专为平板/触屏设计，兼顾键鼠 |
| **语音驱动** | 所有文字可点击朗读，适配低龄不识字儿童 |

### 1.2 目标年龄

- 主目标：5-7 岁（幼小衔接）
- 需满足：大按钮（80px+）、少文字、多图片、语音全覆盖

---

## 二、字体策略

### 2.1 双字体体系

| 用途 | 字体 | 原因 |
|:--|:--|:--|
| **儿歌/韵律** | `Fredoka One` | 圆润可爱，短文本表现佳 |
| **绘本/教材** | `Nunito` | 阅读友好，长文本可读性强 |

### 2.2 Google Fonts 加载

```html
<!-- 儿歌用 -->
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">

<!-- 教材用 -->
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
```

> ⚠️ 务必加 `&display=swap` 防止 FOIT（字体阻塞渲染）

### 2.3 中文字体回退

```css
font-family: 'Nunito', 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

---

## 三、页面结构模板

### 3.1 标准教材课结构（75% 的课件使用）

```
Cover（封面/导入）
  → Story Scene（故事引入，Steve & Alex 对话）
  → Concept Teaching（概念教学，图文结合）
  → Practice（互动练习，点读/配对/选择）
  → Quiz（小测验，计分）
  → Review（复习总结）
  → Celebration（完成庆祝，彩纸效果）
```

### 3.2 绘本故事书结构

```
Cover（封面）
  → Page 1-14（逐页故事，双语对照）
  → Review（字卡/词卡复习）
  → Game（互动游戏）
```

### 3.3 儿歌结构

```
Cover（标题页，播放按钮）
  → Verse 1-4（逐段歌词 + 插图）
  → Sing-along（卡拉OK模式）
  → Activities（动作/游戏）
```

---

## 四、导航系统

### 4.1 推荐的统一范式

**底部导航栏**（所有课件统一）：

```
┌─────────────────────────────────────┐
│         页面内容...                   │
│                                     │
│  🏠  ◀  ● ● ●  ▶  🔊 [读给我听]   │
└─────────────────────────────────────┘
```

### 4.2 HTML 结构

```html
<nav class="nav-bar">
  <button class="btn-home" onclick="navGoTo(0)">🏠</button>
  <button class="btn-prev" onclick="navPrev()">◀</button>
  <div class="page-dots" id="pageDots"></div>
  <button class="btn-next" onclick="navNext()">▶</button>
  <button class="btn-speak" onclick="speakPage()">🔊</button>
  <button class="read-btn" onclick="speakCurrentPage()">📖 读给我听</button>
</nav>
```

### 4.3 导航 JavaScript

```javascript
// 统一函数名
var cur = 0, total = 14;

function navGoTo(n) {
  if (n < 0 || n >= total) return;
  document.querySelectorAll('.page,.content,.slide')[cur]?.classList.remove('active');
  document.querySelectorAll('.page,.content,.slide')[n]?.classList.add('active');
  cur = n;
  updateDots();
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}

function navPrev() { navGoTo(cur - 1); }
function navNext() { navGoTo(cur + 1); }

function updateDots() {
  document.querySelectorAll('.dot').forEach(function(d, i) {
    d.classList.toggle('active', i === cur);
  });
}
```

### 4.4 触摸滑动支持

```javascript
var touchX = 0;
document.addEventListener('touchstart', function(e) {
  touchX = e.changedTouches[0].screenX;
});
document.addEventListener('touchend', function(e) {
  var diff = touchX - e.changedTouches[0].screenX;
  if (Math.abs(diff) > 50) {
    diff > 0 ? navNext() : navPrev();
  }
});
```

### 4.5 键盘支持

```javascript
document.addEventListener('keydown', function(e) {
  if (e.key === 'ArrowRight') navNext();
  if (e.key === 'ArrowLeft') navPrev();
  if (e.key === 'Home') navGoTo(0);
});
```

---

## 五、语音系统

### 5.1 双层策略

```
点击 → 尝试播放 MP3（本地音频文件）
       → MP3 加载失败 → 回退到浏览器 TTS
       → TTS 不可用 → 静默（不报错）
```

### 5.2 通用语音函数

```javascript
var lang = 'zh-CN';  // 或 'en-US'

function playClick(src, text) {
  var audio = new Audio(src);
  audio.onerror = function() {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      u.lang = lang;
      u.rate = 0.85;
      window.speechSynthesis.speak(u);
    }
  };
  audio.play().catch(function() {
    // 自动播放限制，走TTS
    if (window.speechSynthesis) {
      var u = new SpeechSynthesisUtterance(text);
      u.lang = lang;
      window.speechSynthesis.speak(u);
    }
  });
}
```

### 5.3 整页朗读

```javascript
function speakPage() {
  if (!window.speechSynthesis) return;
  var el = document.querySelector('.active');
  if (!el) return;
  var text = (el.innerText || '').replace(/\s+/g, ' ').trim();
  if (text.length < 2) return;
  window.speechSynthesis.cancel();
  var u = new SpeechSynthesisUtterance(text);
  u.lang = lang;
  u.rate = 0.85;
  window.speechSynthesis.speak(u);
}
```

---

## 六、图片处理

### 6.1 标准工作流

```
源图（PNG，来自 GitHub 仓库）
  → 下载到本地
  → 用 cwebp 压缩为 WebP（质量 q=80）
  → 存入 images/<课件名>/webp/
  → HTML 引用本地 WebP
```

### 6.2 压缩效果

| 指标 | 数值 |
|:--|:--|
| 原始 PNG | 25.3 MB（14张） |
| WebP q=80 | 1.8 MB |
| 节省 | **93%** |

### 6.3 HTML 引用

```html
<img loading="lazy" class="lesson-img"
     src="images/nature-lesson-4/webp/page-01.webp"
     onerror="this.style.display='none'"
     alt="描述文字">
```

### 6.4 压缩命令

```bash
cwebp -q 80 input.png -o output.webp
```

---

## 七、动画系统

### 7.1 GSAP 配置

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">
```

### 7.2 翻页过渡

```css
.page, .content, .slide {
  display: none;
  animation: fadeIn 0.3s ease;
}
.page.active, .content.active, .slide.active {
  display: flex;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### 7.3 庆祝特效（彩纸）

```javascript
function celebrate() {
  for (var i = 0; i < 60; i++) {
    var el = document.createElement('div');
    el.className = 'confetti-piece';
    el.style.cssText =
      'position:fixed;width:10px;height:10px;' +
      'background:' + ['#ff6b6b','#ffd93d','#6bcb77','#4d96ff','#ff6b6b'][i%5] + ';' +
      'left:' + Math.random() * 100 + 'vw;' +
      'top:-10px;border-radius:2px;z-index:9999';
    document.body.appendChild(el);
    gsap.to(el, {
      y: window.innerHeight + 20,
      x: (Math.random() - 0.5) * 200,
      rotation: Math.random() * 720 - 360,
      duration: 1.5 + Math.random(),
      delay: Math.random() * 0.5,
      ease: 'power2.out',
      onComplete: function() { this.targets()[0].remove(); }
    });
  }
}
```

---

## 八、交互组件

### 8.1 字卡组件

```html
<div class="char-grid">
  <div class="char-grid-item" onclick="playClick('audio/char-yun.mp3','云')">
    <div class="big">云</div>
    <div class="small">yún 🔊</div>
  </div>
</div>
```

### 8.2 词卡组件

```html
<div class="word-group">
  <div class="word-card" onclick="playClick('audio/word-baiyun.mp3','白云')">
    <div class="word">白云</div>
    <div class="meaning">bái yún</div>
  </div>
</div>
```

### 8.3 句子朗读

```html
<div class="sentence" onclick="playClick('audio/sent-baiyun.mp3','白云在天上。')">
  📖 白云在天上。
</div>
```

### 8.4 选择题

```html
<div class="quiz-options">
  <div class="quiz-option" data-correct="true" onclick="checkAnswer(this, true)">
    正确答案
  </div>
  <div class="quiz-option" data-correct="false" onclick="checkAnswer(this, false)">
    错误答案
  </div>
</div>

<script>
function checkAnswer(el, correct) {
  el.classList.add(correct ? 'correct' : 'wrong');
  playClick('audio/' + (correct ? 'correct.mp3' : 'wrong.mp3'),
    correct ? '答对了！' : '再想想～');
  if (correct) celebrate();
}
</script>
```

---

## 九、样式规范

### 9.1 CSS Reset

```css
html, body {
  width: 100%; height: 100%;
  margin: 0; padding: 0;
  overflow: hidden;
  touch-action: manipulation;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
}
```

### 9.2 颜色体系

| 学科 | 主色 | 用途 |
|:--|:--|:--|
| 数学 | 蓝 `#2196F3` | `background: #f0f7ff` |
| 英语 | 绿 `#4CAF50` | `background: #f0fdf4` |
| 中文 | 红 `#EF5350` | `background: #fff5f5` |
| 儿歌 | 橙 `#FF9800` | `background: #fff8e1` |

### 9.3 按钮规范

```css
.nav-bar button {
  min-width: 48px;
  min-height: 48px;
  font-size: 24px;
  border: none;
  border-radius: 12px;
  background: rgba(255,255,255,0.9);
  cursor: pointer;
  touch-action: manipulation;
}
```

---

## 十、部署检查清单

- [ ] 所有图片压缩为 WebP
- [ ] 所有图片用 `loading="lazy"`（首图用 eager）
- [ ] 所有图片加 `onerror` 降级
- [ ] 导航栏统一：🏠 + ◀ + dots + ▶ + 🔊
- [ ] 所有文字可点击发声
- [ ] 触摸滑动支持
- [ ] 键盘左右键导航
- [ ] GSAP CDN 引用正确
- [ ] `font-display: swap` 已加
- [ ] 中文字体回退链完整
- [ ] `<meta>` viewport 正确
- [ ] 无远程 PNG 引用

---

## 十一、常见陷阱

| 陷阱 | 解决方案 |
|:--|:--|
| GSAP 版本不一致 | 全部锁定 3.12.5 |
| 导航函数名不统一 | 全用 `navGoTo/navPrev/navNext` |
| 语言标签错 | 英文课 `lang="en"`，中文课 `lang="zh-CN"` |
| 触摸滑动缺失 | 必须实现 touchstart/touchend |
| 图片过大 | 强制 WebP q=80 工作流 |
| 字体渲染阻塞 | 加 `&display=swap` |
| 音频文件缺失 | 双层降级策略保底 |
| 彩纸内存泄漏 | GSAP onComplete 清理 DOM 元素 |

---

*最后更新：2026-05-23*  
*基于 childrens-library 项目 115+ 课件的实践总结*
