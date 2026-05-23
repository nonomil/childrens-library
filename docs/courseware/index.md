# 🎪 小朋友的互动学习乐园

<style>
/* ===== 瀑布流布局 ===== */
.waterfall-grid {
  column-count: 8;
  column-gap: 10px;
  padding: 4px 0;
}
.wf-item {
  break-inside: avoid;
  margin-bottom: 10px;
  display: inline-block;
  width: 100%;
}
.wf-card {
  background:#FFFCF5; border-radius:16px; padding:8px;
  text-align:center; box-shadow:0 3px 12px rgba(0,0,0,0.06);
  transition:all .2s cubic-bezier(0.34,1.56,0.64,1);
  border:2px solid transparent; text-decoration:none; color:inherit; display:block;
}
.wf-card:hover {
  transform:translateY(-4px) scale(1.04);
  box-shadow:0 8px 24px rgba(0,0,0,0.12);
}
.wf-card .icon { font-size:28px; line-height:1.2; }
.wf-card .name { font-size:12px; font-weight:700; margin:2px 0; line-height:1.3; color:#5D4037; }
.wf-card .tag-sm { font-size:9px; padding:1px 6px; border-radius:10px; display:inline-block; font-weight:600; }

/* ===== 分类标题 ===== */
.cat-header {
  font-size:22px; font-weight:800; padding:4px 12px; border-radius:16px;
  display:inline-flex; align-items:center; gap:6px; margin:8px 0 4px;
}
.cat-divider { height:2px; background:linear-gradient(90deg,transparent,#FFE0B2,#FFB347,#FFE0B2,transparent); margin:2px 0 6px; }

/* ===== 头部统计 ===== */
.play-header { text-align:center; padding:10px 0 4px; }
.play-header h1 { font-size:28px; margin:4px 0; }
.play-header .subtitle { font-size:14px; color:#8D6E63; margin:2px 0; }
.play-header .stats { display:flex; justify-content:center; gap:10px; margin:6px 0; flex-wrap:wrap; }
.play-header .stat-item {
  background:#FFFCF5; border-radius:20px; padding:4px 14px;
  font-size:12px; font-weight:600; color:#5D4037;
  border:2px solid #FFE0B2;
}

/* ===== 颜色主题 ===== */
.card-red { border-color:#FF6B6B; } .card-red:hover { border-color:#FF6B6B; }
.card-orange { border-color:#FFB347; } .card-orange:hover { border-color:#FFB347; }
.card-green { border-color:#4ECDC4; } .card-green:hover { border-color:#4ECDC4; }
.card-purple { border-color:#A78BFA; } .card-purple:hover { border-color:#A78BFA; }
.card-blue { border-color:#667eea; } .card-blue:hover { border-color:#667eea; }
.card-pink { border-color:#FF9FF3; } .card-pink:hover { border-color:#FF9FF3; }
.card-yellow { border-color:#FFD93D; } .card-yellow:hover { border-color:#FFD93D; }

.tag-red { background:#FFEBEE; color:#D94F4F; }
.tag-orange { background:#FFF3E0; color:#E07C00; }
.tag-green { background:#E8F5E9; color:#2E9E95; }
.tag-purple { background:#F3E5F5; color:#7C5CFC; }
.tag-blue { background:#E3F2FD; color:#4C63D4; }
.tag-pink { background:#FCE4EC; color:#D96FC4; }
.tag-yellow { background:#FFFDE7; color:#C79500; }

/* ===== 新徽章 ===== */
.wf-card.card-new::after { content:'🆕'; position:absolute; top:-6px; right:-6px; font-size:14px; }
.wf-card { position:relative; }

/* ===== 响应式 ===== */
@media(max-width:1200px){ .waterfall-grid { column-count:6; } }
@media(max-width:900px){ .waterfall-grid { column-count:4; } }
@media(max-width:600px){ .waterfall-grid { column-count:2; column-gap:8px; }
  .wf-card { padding:6px; }
  .wf-card .icon { font-size:22px; }
  .wf-card .name { font-size:11px; }
}
</style>

<div class="play-header">
  <a href="../" style="font-size:13px;color:#FFB347;text-decoration:none;font-weight:bold">🏠 回到主页</a>
  <h1>🎪 小朋友的互动学习乐园</h1>
  <p class="subtitle">✨ 每堂课都有互动游戏和语音朗读 🎧</p>
  <div class="stats">
    <span class="stat-item">📚 共 <strong>50</strong> 堂课</span>
    <span class="stat-item">🎵 <strong>27</strong> 首童谣</span>
    <span class="stat-item">🔤 <strong>10</strong> 个英语课</span>
    <span class="stat-item">🌱 <strong>3</strong> 个科学课</span>
    <span class="stat-item">🀄 <strong>5</strong> 个语文课</span>
    <span class="stat-item">🔢 <strong>5</strong> 个数学课</span>
  </div>
</div>

## 🎵 童谣 <span style="font-size:14px">⭐⭐⭐</span>
<div class="cat-divider"></div>
<div class="waterfall-grid">

<a href="twinkle-twinkle.html" class="wf-item"><div class="wf-card card-purple">
  <div class="icon">🌟</div><div class="name">Twinkle Twinkle</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="old-macdonald.html" class="wf-item"><div class="wf-card card-orange">
  <div class="icon">🚜</div><div class="name">Old MacDonald</div>
  <span class="tag-sm tag-orange">🎵 童谣</span>
</div></a>

<a href="five-little-monkeys.html" class="wf-item"><div class="wf-card card-yellow">
  <div class="icon">🐵</div><div class="name">5 Little Monkeys</div>
  <span class="tag-sm tag-yellow">🎵 童谣</span>
</div></a>

<a href="wheels-on-bus.html" class="wf-item"><div class="wf-card card-blue">
  <div class="icon">🚌</div><div class="name">Wheels on Bus</div>
  <span class="tag-sm tag-blue">🎵 童谣</span>
</div></a>

<a href="itsy-bitsy-spider.html" class="wf-item"><div class="wf-card card-green">
  <div class="icon">🕷️</div><div class="name">Itsy Bitsy Spider</div>
  <span class="tag-sm tag-green">🎵 童谣</span>
</div></a>

<a href="row-your-boat.html" class="wf-item"><div class="wf-card card-green">
  <div class="icon">🚣</div><div class="name">Row Your Boat</div>
  <span class="tag-sm tag-green">🎵 童谣</span>
</div></a>

<a href="bingo.html" class="wf-item"><div class="wf-card card-yellow">
  <div class="icon">🐶</div><div class="name">BINGO</div>
  <span class="tag-sm tag-yellow">🎵 童谣</span>
</div></a>

<a href="abc-song.html" class="wf-item"><div class="wf-card card-red">
  <div class="icon">🔤</div><div class="name">ABC Song</div>
  <span class="tag-sm tag-red">🎵 童谣</span>
</div></a>

<a href="head-shoulders.html" class="wf-item"><div class="wf-card card-pink">
  <div class="icon">🧍</div><div class="name">Head Shoulders</div>
  <span class="tag-sm tag-pink">🎵 童谣</span>
</div></a>

<a href="humpty-dumpty.html" class="wf-item"><div class="wf-card card-purple">
  <div class="icon">🥚</div><div class="name">Humpty Dumpty</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="if-youre-happy.html" class="wf-item"><div class="wf-card card-orange">
  <div class="icon">😊</div><div class="name">If You're Happy</div>
  <span class="tag-sm tag-orange">🎵 童谣</span>
</div></a>

<a href="london-bridge.html" class="wf-item"><div class="wf-card card-blue">
  <div class="icon">🌉</div><div class="name">London Bridge</div>
  <span class="tag-sm tag-blue">🎵 童谣</span>
</div></a>

<a href="mary-lamb.html" class="wf-item"><div class="wf-card card-pink">
  <div class="icon">🐑</div><div class="name">Mary's Little Lamb</div>
  <span class="tag-sm tag-pink">🎵 童谣</span>
</div></a>

<a href="jack-and-jill.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">⛰️</div><div class="name">Jack and Jill</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="pat-a-cake.html" class="wf-item"><div class="wf-card card-orange card-new">
  <div class="icon">🎂</div><div class="name">Pat-A-Cake</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="hush-little-baby.html" class="wf-item"><div class="wf-card card-purple card-new">
  <div class="icon">🌙</div><div class="name">Hush Little Baby</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="mulberry-bush.html" class="wf-item"><div class="wf-card card-green card-new">
  <div class="icon">🌳</div><div class="name">Mulberry Bush</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="skidamarink.html" class="wf-item"><div class="wf-card card-pink card-new">
  <div class="icon">💕</div><div class="name">Skidamarink</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="silent-night.html" class="wf-item"><div class="wf-card card-blue card-new">
  <div class="icon">⭐</div><div class="name">Silent Night</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="three-blind-mice.html" class="wf-item"><div class="wf-card card-yellow card-new">
  <div class="icon">🐭</div><div class="name">Three Blind Mice</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="hickory-dickory.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">🕰️</div><div class="name">Hickory Dickory</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="rain-go-away.html" class="wf-item"><div class="wf-card card-blue card-new">
  <div class="icon">🌧️</div><div class="name">Rain Go Away</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="baa-baa-black-sheep.html" class="wf-item"><div class="wf-card card-purple card-new">
  <div class="icon">🐑</div><div class="name">Baa Baa Black Sheep</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="cat-and-fiddle.html" class="wf-item"><div class="wf-card card-orange card-new">
  <div class="icon">🎻</div><div class="name">Cat and Fiddle</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="yankee-doodle.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">🎩</div><div class="name">Yankee Doodle</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="ring-around-rosy.html" class="wf-item"><div class="wf-card card-pink card-new">
  <div class="icon">🌸</div><div class="name">Ring Around Rosy</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

<a href="jack-be-nimble.html" class="wf-item"><div class="wf-card card-yellow card-new">
  <div class="icon">🕯️</div><div class="name">Jack Be Nimble</div>
  <span class="tag-sm tag-purple">🎵 童谣</span>
</div></a>

</div>

## 🔤 英语
<div class="cat-divider"></div>
<div class="waterfall-grid">

<a href="phonics-fat-cat.html" class="wf-item"><div class="wf-card card-green">
  <div class="icon">🐱</div><div class="name">Fat Cat Phonics</div>
  <span class="tag-sm tag-green">🔤 英语</span>
</div></a>

<a href="sight-word-tales-come-to-the-party.html" class="wf-item"><div class="wf-card card-orange">
  <div class="icon">🎉</div><div class="name">Come to Party</div>
  <span class="tag-sm tag-orange">🔤 英语</span>
</div></a>

<a href="sight-word-tales-can-we-get-a-pet.html" class="wf-item"><div class="wf-card card-purple">
  <div class="icon">🐱</div><div class="name">Can We Get Pet</div>
  <span class="tag-sm tag-purple">🔤 英语</span>
</div></a>

<a href="elephant-piggie-surprise.html" class="wf-item"><div class="wf-card card-pink">
  <div class="icon">🐘</div><div class="name">Elephant &amp; Piggie</div>
  <span class="tag-sm tag-pink">🔤 英语</span>
</div></a>

<a href="i-am-an-apple.html" class="wf-item"><div class="wf-card card-red">
  <div class="icon">🍎</div><div class="name">I Am an Apple</div>
  <span class="tag-sm tag-red">🔤 英语</span>
</div></a>

</div>

## 🌱 科学
<div class="cat-divider"></div>
<div class="waterfall-grid">

<a href="gears-transmission.html" class="wf-item"><div class="wf-card card-orange">
  <div class="icon">⚙️</div><div class="name">齿轮传动</div>
  <span class="tag-sm tag-orange">🌱 科学</span>
</div></a>

<a href="rainforest-adventure.html" class="wf-item"><div class="wf-card card-green">
  <div class="icon">🌴</div><div class="name">雨林大冒险</div>
  <span class="tag-sm tag-green">🌱 科学</span>
</div></a>

<a href="nature-lesson-4.html" class="wf-item"><div class="wf-card card-blue">
  <div class="icon">🌿</div><div class="name">大自然识字</div>
  <span class="tag-sm tag-blue">🌱 科学</span>
</div></a>

</div>

## 🔢 数学启蒙
<div class="cat-divider"></div>
<div class="waterfall-grid">

<a href="math-numbers-1-10.html" class="wf-item"><div class="wf-card card-blue">
  <div class="icon">🔢</div><div class="name">认识数字 1~10</div>
  <span class="tag-sm tag-blue">🔢 数学</span>
</div></a>

<a href="math-01-counting.html" class="wf-item"><div class="wf-card card-blue card-new">
  <div class="icon">🔢</div><div class="name">🐑 数数1~10</div>
  <span class="tag-sm tag-blue">🔢 Minecraft</span>
</div></a>

<a href="math-02-counting-11to20.html" class="wf-item"><div class="wf-card card-blue card-new">
  <div class="icon">💎</div><div class="name">💎 数到20</div>
  <span class="tag-sm tag-blue">🔢 Minecraft</span>
</div></a>

<a href="math-03-compare.html" class="wf-item"><div class="wf-card card-blue card-new">
  <div class="icon">⚖️</div><div class="name">⚖️ 比多少比大小</div>
  <span class="tag-sm tag-blue">🔢 Minecraft</span>
</div></a>

<a href="math-04-addition.html" class="wf-item"><div class="wf-card card-blue card-new">
  <div class="icon">➕</div><div class="name">➕ 认识加法5以内</div>
  <span class="tag-sm tag-blue">🔢 Minecraft</span>
</div></a>

</div>

## 🀄 汉字
<div class="cat-divider"></div>
<div class="waterfall-grid">

<a href="chinese-magic-characters.html" class="wf-item"><div class="wf-card card-red">
  <div class="icon">🀄</div><div class="name">神奇汉字</div>
  <span class="tag-sm tag-red">🀄 汉字</span>
</div></a>

<a href="chinese-01-characters.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">☀️</div><div class="name">日月山水火</div>
  <span class="tag-sm tag-red">🀄 Minecraft</span>
</div></a>

<a href="chinese-02-strokes.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">✏️</div><div class="name">基本笔画</div>
  <span class="tag-sm tag-red">🀄 Minecraft</span>
</div></a>

<a href="chinese-03-heaven-earth.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">🌍</div><div class="name">天地人</div>
  <span class="tag-sm tag-red">🀄 Minecraft</span>
</div></a>

<a href="chinese-04-nature.html" class="wf-item"><div class="wf-card card-red card-new">
  <div class="icon">🌤️</div><div class="name">大自然</div>
  <span class="tag-sm tag-red">🀄 Minecraft</span>
</div></a>

</div>

## 🌈 英语启蒙
<div class="cat-divider"></div>
<div class="waterfall-grid">

<a href="english-colors.html" class="wf-item"><div class="wf-card card-green">
  <div class="icon">🌈</div><div class="name">彩虹颜色</div>
  <span class="tag-sm tag-green">🌈 英语</span>
</div></a>

<a href="english-01-hello.html" class="wf-item"><div class="wf-card card-green card-new">
  <div class="icon">👋</div><div class="name">Hello!</div>
  <span class="tag-sm tag-green">🇬🇧 Minecraft</span>
</div></a>

<a href="english-02-abc.html" class="wf-item"><div class="wf-card card-green card-new">
  <div class="icon">🔤</div><div class="name">ABC A-M</div>
  <span class="tag-sm tag-green">🇬🇧 Minecraft</span>
</div></a>

<a href="english-03-abc-nz.html" class="wf-item"><div class="wf-card card-green card-new">
  <div class="icon">🆎</div><div class="name">ABC N-Z</div>
  <span class="tag-sm tag-green">🇬🇧 Minecraft</span>
</div></a>

<a href="english-04-colors.html" class="wf-item"><div class="wf-card card-green card-new">
  <div class="icon">🌈</div><div class="name">Colors 颜色</div>
  <span class="tag-sm tag-green">🇬🇧 Minecraft</span>
</div></a>

</div>

<div style="text-align:center;margin:12px 0">
  <a href="../courseware/" class="view-all" style="
    display:inline-flex;align-items:center;gap:6px;padding:8px 22px;
    border-radius:30px;background:linear-gradient(135deg,#FFB347,#FF8C42);
    color:white;font-size:14px;font-weight:700;text-decoration:none;
    box-shadow:0 4px 14px rgba(255,179,71,0.4);
  ">📚 查看全部课件 →</a>
</div>
