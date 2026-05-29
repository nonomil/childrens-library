# DOC-01：村庄地图入口设计方案（Phase 1）

> 目标：用一个"我的世界村庄地图"替换现有的课件列表页  
> 交付物：`docs/index.html`（或新建 `village.html`）  
> 周期：3-5天  
> 依赖：不依赖任何其他阶段

---

## 一、核心设计思路

不是"课件目录"，是"村庄地图"。

每个学科对应村庄里的一栋建筑：
- 🏫 学校 → 英语课件
- 📚 图书馆 → 语文/绘本
- 🔢 集市 → 数学
- 🎵 广场 → 童谣
- 🔬 实验室 → 科学/齿轮

孩子点击建筑，进入该学科的课件列表（不是全部115个堆在一起）。

---

## 二、页面结构

```
village.html
│
├── <header>  村庄名 + Steve头像 + 今日星星数
│
├── <main class="village-map">
│   ├── <canvas id="village-bg">  像素风背景（草地、天空、云）
│   └── <div class="buildings">
│       ├── .building[data-zone="english"]   学校
│       ├── .building[data-zone="chinese"]   图书馆
│       ├── .building[data-zone="math"]      集市
│       ├── .building[data-zone="songs"]     广场
│       └── .building[data-zone="science"]   实验室
│
├── <div class="village-characters">
│   ├── Steve（会走动的像素角色）
│   └── Alex（站在图书馆门口）
│
└── <div class="zone-panel">  点击建筑后弹出的课件列表面板
    ├── 建筑名 + 图标
    ├── 已完成 / 全部课件数
    └── 课件卡片列表（可滚动）
```

---

## 三、视觉规范（我的世界像素风）

### 3.1 整体配色

```css
:root {
  /* 地图背景 */
  --sky: #87CEEB;
  --grass: #5D8A3C;
  --dirt: #8B6914;
  --stone: #888888;

  /* UI */
  --mc-dark: #1D1D1D;
  --mc-brown: #3C1F0A;
  --mc-gold: #FFD700;
  --mc-green: #5D8A3C;
  --mc-panel: rgba(0,0,0,0.75);

  /* 字体 */
  --font-mc: 'Press Start 2P', 'Courier New', monospace;  /* 标题 */
  --font-body: 'Nunito', sans-serif;  /* 正文（孩子可读性优先）*/
}
```

### 3.2 建筑卡片样式

```css
.building {
  position: absolute;
  cursor: pointer;
  image-rendering: pixelated;  /* 像素图不模糊 */
  transition: transform 0.1s;
  filter: drop-shadow(3px 3px 0 rgba(0,0,0,0.4));
}

.building:hover,
.building:active {
  transform: scale(1.08) translateY(-4px);
  filter: drop-shadow(3px 8px 0 rgba(0,0,0,0.4))
          brightness(1.15);
}

/* 已解锁徽章 */
.building[data-unlocked="true"]::after {
  content: '✓';
  position: absolute;
  top: -8px; right: -8px;
  background: var(--mc-gold);
  color: var(--mc-dark);
  border-radius: 50%;
  width: 24px; height: 24px;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px;
  font-weight: bold;
}
```

### 3.3 进度条（像素风）

```css
.progress-bar {
  height: 20px;
  background: var(--mc-dark);
  border: 3px solid #555;
  position: relative;
  image-rendering: pixelated;
}

.progress-bar-fill {
  height: 100%;
  background: repeating-linear-gradient(
    90deg,
    var(--mc-green) 0px,
    var(--mc-green) 16px,
    #4a7030 16px,
    #4a7030 20px
  );
  transition: width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 四、建筑与课件的映射关系

```javascript
const ZONE_CONFIG = {
  english: {
    name: '英语学校',
    icon: '🏫',
    color: '#4FC3F7',
    building: 'images/building-school.webp',
    position: { left: '15%', top: '35%' },
    size: { width: 180, height: 160 },
    // 课件前缀匹配
    coursewarePrefix: ['english-'],
    totalCount: 25,
    description: 'Steve 和 Alex 在这里学英语！',
    unlockRequirement: 0  // 默认解锁
  },
  chinese: {
    name: '中文图书馆',
    icon: '📚',
    color: '#FF8A65',
    building: 'images/building-library.webp',
    position: { left: '55%', top: '30%' },
    size: { width: 160, height: 150 },
    coursewarePrefix: ['chinese-', 'poem-', 'story-'],
    totalCount: 25,
    description: 'Bob 爷爷在这里讲故事！',
    unlockRequirement: 0
  },
  math: {
    name: '数学集市',
    icon: '🔢',
    color: '#81C784',
    building: 'images/building-market.webp',
    position: { left: '35%', top: '55%' },
    size: { width: 170, height: 140 },
    coursewarePrefix: ['math-'],
    totalCount: 25,
    description: '买卖东西，学数学！',
    unlockRequirement: 3  // 完成3课英语后解锁
  },
  songs: {
    name: '音乐广场',
    icon: '🎵',
    color: '#F48FB1',
    building: 'images/building-stage.webp',
    position: { left: '70%', top: '55%' },
    size: { width: 150, height: 130 },
    coursewarePrefix: ['twinkle', 'old-macdonald', 'wheels', 'bingo',
                       'abc-song', 'head-shoulders', 'humpty'],
    totalCount: 27,
    description: '唱歌跳舞！',
    unlockRequirement: 0
  },
  science: {
    name: 'STEM 实验室',
    icon: '🔬',
    color: '#B39DDB',
    building: 'images/building-lab.webp',
    position: { left: '80%', top: '35%' },
    size: { width: 140, height: 150 },
    coursewarePrefix: ['gears-', 'science-', 'rainforest-'],
    totalCount: 7,
    description: '齿轮、太阳系、大冒险！',
    unlockRequirement: 5
  }
};
```

---

## 五、核心 JS 逻辑

### 5.1 主流程

```javascript
// 入口
document.addEventListener('DOMContentLoaded', () => {
  const state = loadVillageState();
  renderVillage(state);
  startSteveAnimation();
  checkDailyBonus(state);
});

// 点击建筑
function onBuildingClick(zone) {
  const config = ZONE_CONFIG[zone];
  const state = loadVillageState();

  // 检查是否解锁
  if (!isZoneUnlocked(zone, state)) {
    showLockMessage(config);
    return;
  }

  // 打开课件面板
  openZonePanel(zone, config, state);
  playSound('open-door');
}

// 打开课件面板
function openZonePanel(zone, config, state) {
  const panel = document.getElementById('zone-panel');
  const courses = getCoursewareList(zone);

  panel.innerHTML = renderZonePanel(zone, config, courses, state);
  panel.classList.add('open');

  // 动画：从建筑位置飞出
  gsap.fromTo(panel,
    { scale: 0.5, opacity: 0 },
    { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(1.7)' }
  );
}
```

### 5.2 课件卡片渲染

```javascript
function renderCourseCard(course, isCompleted, isLocked) {
  return `
    <div class="course-card ${isCompleted ? 'completed' : ''} ${isLocked ? 'locked' : ''}"
         onclick="${isLocked ? 'showLockedHint()' : `openCourse('${course.file}')`}">
      <div class="course-thumbnail">
        <img src="${course.thumbnail || 'images/default-thumb.webp'}" 
             alt="${course.title}"
             loading="lazy">
        ${isCompleted ? '<div class="complete-badge">⭐</div>' : ''}
        ${isLocked ? '<div class="lock-overlay">🔒</div>' : ''}
      </div>
      <div class="course-title">${course.title}</div>
      <div class="course-meta">${course.lesson} · ${course.duration || '~5分钟'}</div>
    </div>
  `;
}
```

### 5.3 打开课件（关键：完成后回调）

```javascript
function openCourse(filename) {
  // 记录"正在学习"状态
  const state = loadVillageState();
  state.currentCourse = filename;
  state.courseStartTime = Date.now();
  saveVillageState(state);

  // 打开课件（新标签页，方便返回村庄）
  window.open(`../courseware/${filename}`, '_blank');

  // 提示孩子
  showToast('学完回来，村庄会有惊喜！🎁');
}
```

---

## 六、Steve 动画角色

Steve 是一个 32×32 像素的精灵图，在村庄地图上来回走动。

```javascript
const steve = {
  x: 200, y: 300,
  direction: 1,  // 1=右 -1=左
  frame: 0,
  frameTimer: 0,
  FRAME_INTERVAL: 8,  // 每8帧换一格
  SPEED: 1.2,
  // 精灵图：走路4帧（左脚/右脚各2帧）
  spritesheet: 'images/steve-walk.webp',
  // 巡逻区域
  patrol: { minX: 100, maxX: 600 }
};

function updateSteve() {
  steve.x += steve.SPEED * steve.direction;
  if (steve.x > steve.patrol.maxX || steve.x < steve.patrol.minX) {
    steve.direction *= -1;
  }

  steve.frameTimer++;
  if (steve.frameTimer >= steve.FRAME_INTERVAL) {
    steve.frame = (steve.frame + 1) % 4;
    steve.frameTimer = 0;
  }
}

// 点击 Steve：他说一句话
steveEl.addEventListener('click', () => {
  const lines = [
    '今天想去哪里学习？',
    '我们去图书馆吧！',
    '数学集市有好吃的！',
    '嘿！Alex 在等你！',
  ];
  showSpeechBubble(steve, randomPick(lines));
  speakText(randomPick(lines));  // TTS朗读
});
```

---

## 七、建筑图片规范

如果没有像素风建筑图，可以用 CSS 纯绘制（方块堆叠感）：

```css
.building-school {
  width: 180px; height: 160px;
  background:
    /* 屋顶 */
    linear-gradient(135deg, #c0392b 50%, #e74c3c 50%) 0 0 / 180px 60px no-repeat,
    /* 墙体 */
    repeating-linear-gradient(
      0deg,
      #e8d5b7 0, #e8d5b7 15px,
      #d4c4a8 15px, #d4c4a8 16px
    ) 0 60px / 180px 100px no-repeat;
  image-rendering: pixelated;
  border: 3px solid #7a6040;
}
```

---

## 八、验收标准

- [ ] 平板横屏打开，看到村庄地图，不是列表
- [ ] 五个建筑区域清晰可辨，有名字标签
- [ ] 点击建筑，弹出该区域课件列表（有动画）
- [ ] Steve 在地图上会走动，点击会说话
- [ ] 进度条显示每个区域完成了几课
- [ ] 返回村庄按钮在每个课件页都能找到（见 DOC-04）
- [ ] 首次打开有欢迎动画（Steve 跑进画面）
- [ ] 加载时间 < 2秒（平板 WiFi）

---

## 九、文件清单

```
新建/修改文件：
├── village.html               ← 主入口（新建）
├── courseware/shared/
│   ├── village.js             ← 村庄状态管理（新建）
│   └── village.css            ← 村庄样式（新建）
└── courseware/images/
    ├── steve-walk.webp        ← Steve精灵图（新建，可用emoji占位）
    ├── building-school.webp   ← 学校建筑（新建，可用CSS占位）
    ├── building-library.webp
    ├── building-market.webp
    ├── building-stage.webp
    └── building-lab.webp

不动的文件：
└── courseware/*.html          ← 全部课件，一个字不改（Phase 1）
```
