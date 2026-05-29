# DOC-02：成就与存档系统（Phase 2）

> 目标：孩子有自己的进度，每次打开看到上次的成果  
> 依赖：Phase 1 村庄地图已完成  
> 周期：4-6天  
> 核心机制：localStorage 存档 + 课件完成上报 + 村庄成长动画

---

## 一、设计原则

**进度要"可见"，不是数字，是建筑。**

- 完成3课英语 → 学校门口多了一个旗帜
- 完成5课语文 → 图书馆多了一个书架（窗户里能看见）
- 收集10颗星 → 村庄中央多了一个路灯
- 完成任意10课 → Bob 爷爷从村庄外面走进来，永久住在村里

这些变化孩子**自己就会发现**，不需要弹窗告诉他。

---

## 二、localStorage 数据结构

```javascript
// key: 'village_state'
const VILLAGE_STATE_SCHEMA = {
  version: 1,
  lastVisit: '2026-05-28',          // ISO date
  totalStars: 0,                     // 累计星星数
  streakDays: 0,                     // 连续学习天数
  
  // 每个区域的进度
  zones: {
    english: {
      completed: ['english-01-hello.html', 'english-02-abc.html'],
      stars: { 'english-01-hello.html': 3, 'english-02-abc.html': 2 },
      totalCompleted: 2,
      firstCompletedAt: '2026-05-20'
    },
    chinese: { completed: [], stars: {}, totalCompleted: 0 },
    math: { completed: [], stars: {}, totalCompleted: 0 },
    songs: { completed: [], stars: {}, totalCompleted: 0 },
    science: { completed: [], stars: {}, totalCompleted: 0 }
  },
  
  // 解锁的村庄装饰（成就触发）
  decorations: {
    school_flag: false,       // 解锁条件：英语完成3课
    library_bookshelf: false, // 解锁条件：语文完成5课
    village_lamp: false,      // 解锁条件：累计10星
    bob_resident: false,      // 解锁条件：任意完成10课
    secret_chest: false,      // 解锁条件：连续3天
    rainbow: false            // 解锁条件：全部区域各完成1课
  },
  
  // 成就徽章
  badges: [],
  
  // 每日任务
  dailyMission: {
    date: '',
    task: '',
    completed: false
  }
};
```

---

## 三、课件完成上报协议

### 3.1 课件如何通知村庄"我完成了"

每个课件在庆祝页（最后一页）加一段 JS，**这是对现有课件的唯一改动**：

```javascript
// 加在课件的 celebrate() 函数里，或庆祝页的 onload
// 文件：每个课件的最后一页或庆祝触发点

function reportCourseComplete(stars) {
  // stars: 1-3，根据课件内答题表现传入
  const filename = location.pathname.split('/').pop();
  
  // 写入 localStorage
  const raw = localStorage.getItem('village_state');
  const state = raw ? JSON.parse(raw) : getDefaultState();
  
  // 找到这个课件属于哪个zone
  const zone = detectZone(filename);
  if (!zone) return;
  
  if (!state.zones[zone].completed.includes(filename)) {
    state.zones[zone].completed.push(filename);
    state.zones[zone].totalCompleted++;
    state.totalStars += stars || 1;
  }
  state.zones[zone].stars[filename] = stars || 1;
  
  localStorage.setItem('village_state', JSON.stringify(state));
  
  // 显示"返回村庄"按钮，带上完成参数
  showReturnButton(stars);
}

function detectZone(filename) {
  if (filename.startsWith('english-')) return 'english';
  if (filename.startsWith('chinese-') || filename.startsWith('poem-')) return 'chinese';
  if (filename.startsWith('math-')) return 'math';
  if (filename.startsWith('gears-') || filename.startsWith('science-')) return 'science';
  // 童谣通过白名单判断
  const songFiles = ['twinkle-twinkle', 'old-macdonald', 'wheels-on-the-bus'];
  if (songFiles.some(s => filename.startsWith(s))) return 'songs';
  return null;
}
```

### 3.2 返回村庄按钮

```javascript
function showReturnButton(stars) {
  const btn = document.createElement('div');
  btn.className = 'return-village-btn';
  btn.innerHTML = `
    <div class="stars-earned">${'⭐'.repeat(stars || 1)}</div>
    <div class="btn-text">返回村庄</div>
    <div class="hint">看看村庄有什么变化！</div>
  `;
  btn.onclick = () => {
    window.location.href = '../village.html?justCompleted=' + 
                           encodeURIComponent(location.pathname.split('/').pop());
  };
  document.body.appendChild(btn);
}
```

### 3.3 村庄接收完成事件

```javascript
// village.html 启动时检查
function checkJustCompleted() {
  const params = new URLSearchParams(location.search);
  const justCompleted = params.get('justCompleted');
  if (!justCompleted) return;

  // 清除URL参数
  history.replaceState({}, '', location.pathname);

  // 短暂延迟后触发庆祝
  setTimeout(() => {
    triggerCompletionCelebration(justCompleted);
    checkAndUnlockDecorations();
  }, 800);
}

function triggerCompletionCelebration(filename) {
  // Steve 跑到屏幕中间，跳一下，说话
  animateSteveCelebrate();
  speakText('太棒了！你完成了一课！');
  
  // GSAP 彩纸
  celebrate();
  
  // 检查是否触发新装饰
  const state = loadVillageState();
  const newDecorations = checkNewDecorations(state);
  if (newDecorations.length > 0) {
    setTimeout(() => showDecorationUnlock(newDecorations[0]), 2000);
  }
}
```

---

## 四、装饰解锁系统

### 4.1 解锁条件配置

```javascript
const DECORATION_RULES = [
  {
    id: 'school_flag',
    condition: (s) => s.zones.english.totalCompleted >= 3,
    unlockMessage: '学校门口多了一面旗帜！',
    speakText: '英语学了三课，学校更漂亮了！',
    zone: 'english'
  },
  {
    id: 'library_bookshelf',
    condition: (s) => s.zones.chinese.totalCompleted >= 5,
    unlockMessage: '图书馆多了好多书！',
    speakText: '语文学了五课，图书馆装满了书！',
    zone: 'chinese'
  },
  {
    id: 'village_lamp',
    condition: (s) => s.totalStars >= 10,
    unlockMessage: '村庄中央亮起了路灯！',
    speakText: '收集了十颗星星，村庄更亮了！',
    zone: null
  },
  {
    id: 'bob_resident',
    condition: (s) => {
      const total = Object.values(s.zones).reduce((a, z) => a + z.totalCompleted, 0);
      return total >= 10;
    },
    unlockMessage: 'Bob 爷爷搬进村庄住了！',
    speakText: 'Bob 爷爷说：你学了这么多，我要住在这里陪你！',
    zone: null
  },
  {
    id: 'secret_chest',
    condition: (s) => s.streakDays >= 3,
    unlockMessage: '发现了一个神秘宝箱！',
    speakText: '连续三天来学习，发现了宝藏！',
    zone: null
  },
  {
    id: 'rainbow',
    condition: (s) => Object.values(s.zones).every(z => z.totalCompleted >= 1),
    unlockMessage: '彩虹出现了！',
    speakText: '每个地方都去了一次，天空出现了彩虹！',
    zone: null
  }
];
```

### 4.2 装饰渲染（CSS层叠）

```javascript
function renderDecorations(state) {
  const decorations = state.decorations;
  
  // 每个装饰是叠加在建筑/地图上的绝对定位元素
  Object.entries(decorations).forEach(([id, unlocked]) => {
    const el = document.querySelector(`[data-decoration="${id}"]`);
    if (!el) return;
    
    if (unlocked) {
      el.classList.add('visible');
      el.classList.remove('hidden');
    }
  });
}

// 装饰解锁动画
function animateDecorationUnlock(decorationId) {
  const el = document.querySelector(`[data-decoration="${decorationId}"]`);
  el.classList.add('visible');
  
  // 从天而降
  gsap.fromTo(el,
    { y: -100, opacity: 0, scale: 0 },
    { y: 0, opacity: 1, scale: 1, duration: 0.8, ease: 'bounce.out' }
  );
  
  // 闪光效果
  gsap.to(el, { filter: 'brightness(2)', duration: 0.2, yoyo: true, repeat: 3 });
}
```

---

## 五、每日任务系统

### 5.1 任务生成

```javascript
const DAILY_TASK_POOL = [
  { task: '完成一节英语课', condition: (e) => e.zone === 'english', reward: 2 },
  { task: '唱一首童谣', condition: (e) => e.zone === 'songs', reward: 1 },
  { task: '做三道数学题', condition: (e) => e.zone === 'math', reward: 2 },
  { task: '读一个中文故事', condition: (e) => e.zone === 'chinese', reward: 2 },
  { task: '探索科学实验室', condition: (e) => e.zone === 'science', reward: 3 },
  { task: '今天学两门课', condition: (e) => e.totalToday >= 2, reward: 3 },
];

function getDailyMission(state) {
  const today = new Date().toISOString().split('T')[0];
  if (state.dailyMission.date === today) return state.dailyMission;

  // 新的一天，生成新任务（倾向于孩子最少学的区域）
  const weakestZone = getWeakestZone(state);
  const task = DAILY_TASK_POOL.find(t => t.task.includes(ZONE_LABELS[weakestZone]))
               || randomPick(DAILY_TASK_POOL);

  const mission = { date: today, task: task.task, reward: task.reward, completed: false };
  state.dailyMission = mission;
  saveVillageState(state);
  return mission;
}
```

### 5.2 任务展示

```html
<!-- 村庄地图右上角的任务板 -->
<div class="daily-board">
  <div class="board-title">📋 今日任务</div>
  <div class="board-task" id="daily-task-text">完成一节英语课</div>
  <div class="board-reward">奖励：⭐⭐</div>
  <div class="board-status" id="daily-status">未完成</div>
</div>
```

---

## 六、连续学习天数

```javascript
function updateStreak(state) {
  const today = new Date().toISOString().split('T')[0];
  const last = state.lastVisit;

  if (!last) {
    state.streakDays = 1;
  } else {
    const dayDiff = (new Date(today) - new Date(last)) / (1000 * 60 * 60 * 24);
    if (dayDiff === 1) {
      state.streakDays++;
    } else if (dayDiff > 1) {
      state.streakDays = 1;  // 断了，重置
    }
    // dayDiff === 0：同一天多次打开，不变
  }

  state.lastVisit = today;
  return state;
}
```

---

## 七、对现有课件的改动清单

Phase 2 对现有课件的改动**极小**，仅在每个课件的庆祝触发点加一个函数调用：

### 改动方式一（推荐）：修改 shared/courseware.js

在现有 `celebrate()` 函数里加调用：

```javascript
// shared/courseware.js 的 celebrate() 函数末尾追加：
function celebrate() {
  // ... 原有彩纸代码 ...

  // 新增：上报完成
  if (window.reportCourseComplete) {
    window.reportCourseComplete(calculateStars());
  }
}

function calculateStars() {
  // 根据课件内正确率计算星星
  // 如果课件没有追踪答题，默认给1星
  if (typeof window.quizCorrect !== 'undefined' && typeof window.quizTotal !== 'undefined') {
    const ratio = window.quizCorrect / window.quizTotal;
    if (ratio >= 0.9) return 3;
    if (ratio >= 0.6) return 2;
    return 1;
  }
  return 1;
}
```

在每个课件的 `<head>` 里加：

```html
<script src="../shared/village-reporter.js"></script>
```

### 改动方式二（批量脚本）

用 Python 脚本批量在所有课件 `</head>` 前插入一行：

```python
# scripts/add_village_reporter.py
import os, re

COURSEWARE_DIR = 'courseware'
INSERT_LINE = '<script src="../shared/village-reporter.js"></script>\n'

for f in os.listdir(COURSEWARE_DIR):
    if not f.endswith('.html'): continue
    path = os.path.join(COURSEWARE_DIR, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if 'village-reporter' not in content:
        content = content.replace('</head>', INSERT_LINE + '</head>', 1)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'Updated: {f}')
```

---

## 八、验收标准

- [ ] 完成任意课件后，返回村庄能看到星星数增加
- [ ] 完成3课英语，学校门口出现旗帜（有动画）
- [ ] 第二天打开，进度还在（localStorage 持久化）
- [ ] 连续2天打开，连续天数显示正确
- [ ] 每日任务显示，完成后有奖励动画
- [ ] 累计10颗星，路灯出现
- [ ] 平板上返回村庄按钮容易点击（最小48×48px）
