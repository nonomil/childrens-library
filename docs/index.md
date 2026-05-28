# 🎪 小朋友的互动学习乐园

<style>
/* ===== 全局 ===== */
*{box-sizing:border-box}

/* ===== 头部 ===== */
.play-header{text-align:center;padding:14px 0 6px}
.play-header h1{font-size:30px;margin:4px 0;color:#E8751A;font-weight:800}
.play-header .subtitle{font-size:15px;color:#8D6E63;margin:2px 0}
.play-header .stats{display:flex;justify-content:center;gap:8px;margin:8px 0;flex-wrap:wrap}
.play-header .stat-item{background:#FFFCF5;border-radius:20px;padding:5px 16px;font-size:13px;font-weight:600;color:#5D4037;border:2px solid #FFE0B2}

/* ===== 横向滚动行 ===== */
.section{margin:16px 0}
.section-header{display:flex;align-items:center;gap:8px;margin-bottom:6px;padding:0 4px}
.section-header .sh-icon{font-size:22px}
.section-header .sh-name{font-size:18px;font-weight:800;color:#5D4037}
.section-header .sh-count{font-size:12px;color:#999;font-weight:600}
.section-header .sh-arrow{font-size:13px;color:#FFB347;font-weight:700;margin-left:auto;text-decoration:none}
.section-header .sh-arrow:hover{text-decoration:underline}

.scroll-row{display:flex;gap:10px;overflow-x:auto;overflow-y:hidden;padding:6px 4px 10px;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;scrollbar-width:thin;scrollbar-color:#FFB347 transparent}
.scroll-row::-webkit-scrollbar{height:5px}
.scroll-row::-webkit-scrollbar-thumb{background:#FFD54F;border-radius:10px}
.scroll-row::-webkit-scrollbar-track{background:transparent}

/* ===== 横向卡片 ===== */
.scroll-card{flex:0 0 140px;background:#FFFCF5;border-radius:16px;padding:12px 8px;text-align:center;text-decoration:none;color:inherit;display:flex;flex-direction:column;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,0.06);border:2px solid transparent;transition:all .2s cubic-bezier(0.34,1.56,0.64,1);position:relative;touch-action:manipulation}
.scroll-card:hover{transform:translateY(-4px) scale(1.06);border-color:#FFB347;box-shadow:0 8px 24px rgba(255,179,71,0.2)}
.scroll-card:active{transform:scale(0.95)}
.scroll-card .sc-icon{font-size:34px;line-height:1.2;margin-bottom:4px}
.scroll-card .sc-name{font-size:12px;font-weight:700;color:#5D4037;line-height:1.3;word-break:break-word}
.scroll-card.card-new::after{content:'🆕';position:absolute;top:-6px;right:-6px;font-size:13px}

@media(max-width:500px){
  .play-header h1{font-size:24px}
  .scroll-card{flex:0 0 120px;padding:10px 6px}
  .scroll-card .sc-icon{font-size:28px}
  .scroll-card .sc-name{font-size:11px}
  .section-header .sh-name{font-size:16px}
}

/* ===== 颜色边框 ===== */
.card-blue{border-color:#42A5F5}.card-blue:hover{border-color:#42A5F5}
.card-red{border-color:#EF5350}.card-red:hover{border-color:#EF5350}
.card-green{border-color:#66BB6A}.card-green:hover{border-color:#66BB6A}
.card-orange{border-color:#FFB347}.card-orange:hover{border-color:#FFB347}
.card-purple{border-color:#A78BFA}.card-purple:hover{border-color:#A78BFA}
.card-yellow{border-color:#FFD93D}.card-yellow:hover{border-color:#FFD93D}
.card-pink{border-color:#FF9FF3}.card-pink:hover{border-color:#FF9FF3}
</style>

<div class="play-header">
  <h1>🎪 小朋友的互动学习乐园</h1>
  <p class="subtitle">✨ 每堂课都有互动游戏和语音朗读 🎧</p>
  <div class="stats">
    <span class="stat-item">📚 共 <strong>123</strong> 堂课</span>
    <span class="stat-item">🎵 <strong>27</strong> 首童谣</span>
    <span class="stat-item">🔤 <strong>24</strong> 个英语课</span>
    <span class="stat-item">🀄 <strong>24</strong> 个语文课</span>
    <span class="stat-item">🧮 <strong>24</strong> 个数学课</span>
    <span class="stat-item">📖 <strong>8</strong> 本绘本</span>
    <span class="stat-item">📚 <strong>10</strong> 个中文故事</span>
    <span class="stat-item">📖 <strong>10</strong> 个英文故事</span>
    <span class="stat-item">🎓 <strong>10</strong> 个教案</span>
    <span class="stat-item">🏯 <strong>20</strong> 个古诗</span>
  </div>
</div>

<!-- ===== 🎵 童谣 ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🎵</span>
  <span class="sh-name">童谣</span>
  <span class="sh-count">27 首</span>
</div>
<div class="scroll-row">

<a href="courseware/twinkle-twinkle.html" class="scroll-card card-purple"><span class="sc-icon">🌟</span><span class="sc-name">Twinkle Twinkle</span></a>
<a href="courseware/old-macdonald.html" class="scroll-card card-orange"><span class="sc-icon">🚜</span><span class="sc-name">Old MacDonald</span></a>
<a href="courseware/five-little-monkeys.html" class="scroll-card card-yellow"><span class="sc-icon">🐵</span><span class="sc-name">5 Little Monkeys</span></a>
<a href="courseware/wheels-on-bus.html" class="scroll-card card-blue"><span class="sc-icon">🚌</span><span class="sc-name">Wheels on Bus</span></a>
<a href="courseware/itsy-bitsy-spider.html" class="scroll-card card-green"><span class="sc-icon">🕷️</span><span class="sc-name">Itsy Bitsy Spider</span></a>
<a href="courseware/row-your-boat.html" class="scroll-card card-green"><span class="sc-icon">🚣</span><span class="sc-name">Row Your Boat</span></a>
<a href="courseware/bingo.html" class="scroll-card card-yellow"><span class="sc-icon">🐶</span><span class="sc-name">BINGO</span></a>
<a href="courseware/abc-song.html" class="scroll-card card-red"><span class="sc-icon">🔤</span><span class="sc-name">ABC Song</span></a>
<a href="courseware/head-shoulders.html" class="scroll-card card-pink"><span class="sc-icon">🧍</span><span class="sc-name">Head Shoulders</span></a>
<a href="courseware/humpty-dumpty.html" class="scroll-card card-purple"><span class="sc-icon">🥚</span><span class="sc-name">Humpty Dumpty</span></a>
<a href="courseware/if-youre-happy.html" class="scroll-card card-orange"><span class="sc-icon">😊</span><span class="sc-name">If You're Happy</span></a>
<a href="courseware/london-bridge.html" class="scroll-card card-blue"><span class="sc-icon">🌉</span><span class="sc-name">London Bridge</span></a>
<a href="courseware/mary-lamb.html" class="scroll-card card-pink"><span class="sc-icon">🐑</span><span class="sc-name">Mary's Little Lamb</span></a>
<a href="courseware/jack-and-jill.html" class="scroll-card card-red card-new"><span class="sc-icon">⛰️</span><span class="sc-name">Jack and Jill</span></a>
<a href="courseware/pat-a-cake.html" class="scroll-card card-orange card-new"><span class="sc-icon">🎂</span><span class="sc-name">Pat-A-Cake</span></a>
<a href="courseware/hush-little-baby.html" class="scroll-card card-purple card-new"><span class="sc-icon">🌙</span><span class="sc-name">Hush Little Baby</span></a>
<a href="courseware/mulberry-bush.html" class="scroll-card card-green card-new"><span class="sc-icon">🌳</span><span class="sc-name">Mulberry Bush</span></a>
<a href="courseware/skidamarink.html" class="scroll-card card-pink card-new"><span class="sc-icon">💕</span><span class="sc-name">Skidamarink</span></a>
<a href="courseware/silent-night.html" class="scroll-card card-blue card-new"><span class="sc-icon">⭐</span><span class="sc-name">Silent Night</span></a>
<a href="courseware/three-blind-mice.html" class="scroll-card card-yellow card-new"><span class="sc-icon">🐭</span><span class="sc-name">Three Blind Mice</span></a>
<a href="courseware/hickory-dickory.html" class="scroll-card card-red card-new"><span class="sc-icon">🕰️</span><span class="sc-name">Hickory Dickory</span></a>
<a href="courseware/rain-go-away.html" class="scroll-card card-blue card-new"><span class="sc-icon">🌧️</span><span class="sc-name">Rain Go Away</span></a>
<a href="courseware/baa-baa-black-sheep.html" class="scroll-card card-purple card-new"><span class="sc-icon">🐑</span><span class="sc-name">Baa Baa Black Sheep</span></a>
<a href="courseware/cat-and-fiddle.html" class="scroll-card card-orange card-new"><span class="sc-icon">🎻</span><span class="sc-name">Cat and Fiddle</span></a>
<a href="courseware/yankee-doodle.html" class="scroll-card card-red card-new"><span class="sc-icon">🎩</span><span class="sc-name">Yankee Doodle</span></a>
<a href="courseware/ring-around-rosy.html" class="scroll-card card-pink card-new"><span class="sc-icon">🌸</span><span class="sc-name">Ring Around Rosy</span></a>
<a href="courseware/jack-be-nimble.html" class="scroll-card card-yellow card-new"><span class="sc-icon">🕯️</span><span class="sc-name">Jack Be Nimble</span></a>

</div>
</div>

<!-- ===== 🧮 数学启蒙-Minecraft ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🧮</span>
  <span class="sh-name">数学 Minecraft</span>
  <span class="sh-count">8 课</span>
  <a href="courseware/" class="sh-arrow">全部 →</a>
</div>
<div class="scroll-row">

<a href="courseware/math-01-counting.html" class="scroll-card card-blue"><span class="sc-icon">🐑</span><span class="sc-name">数数1~10</span></a>
<a href="courseware/math-02-counting-11to20.html" class="scroll-card card-blue"><span class="sc-icon">💎</span><span class="sc-name">数到20</span></a>
<a href="courseware/math-03-compare.html" class="scroll-card card-blue"><span class="sc-icon">⚖️</span><span class="sc-name">比多少比大小</span></a>
<a href="courseware/math-04-addition.html" class="scroll-card card-blue"><span class="sc-icon">➕</span><span class="sc-name">认识加法5以内</span></a>
<a href="courseware/math-05-addition10.html" class="scroll-card card-blue"><span class="sc-icon">🧮</span><span class="sc-name">10以内加法</span></a>
<a href="courseware/math-06-subtraction5.html" class="scroll-card card-blue"><span class="sc-icon">➖</span><span class="sc-name">认识减法5以内</span></a>
<a href="courseware/math-07-subtraction10.html" class="scroll-card card-blue"><span class="sc-icon">➖</span><span class="sc-name">10以内减法</span></a>
<a href="courseware/math-08-addition20.html" class="scroll-card card-blue"><span class="sc-icon">➕</span><span class="sc-name">进位加法20</span></a>
<a href="courseware/math-09-subtraction20.html" class="scroll-card card-blue"><span class="sc-icon">➖</span><span class="sc-name">退位减法20</span></a>
<a href="courseware/math-10-shapes.html" class="scroll-card card-blue"><span class="sc-icon">🔷</span><span class="sc-name">认识图形</span></a>
<a href="courseware/math-11-measurement.html" class="scroll-card card-blue"><span class="sc-icon">📏</span><span class="sc-name">测量与长度</span></a>
<a href="courseware/math-12-review.html" class="scroll-card card-blue"><span class="sc-icon">🔄</span><span class="sc-name">总复习</span></a>
<a href="courseware/math-13-numbers100.html" class="scroll-card card-blue"><span class="sc-icon">💯</span><span class="sc-name">100以内数</span></a>
<a href="courseware/math-14-addsub2digit.html" class="scroll-card card-blue"><span class="sc-icon">📊</span><span class="sc-name">两位数加减</span></a>
<a href="courseware/math-15-money.html" class="scroll-card card-blue"><span class="sc-icon">💰</span><span class="sc-name">认识钱币</span></a>
<a href="courseware/math-16-clock.html" class="scroll-card card-blue"><span class="sc-icon">⏰</span><span class="sc-name">认识钟表</span></a>
<a href="courseware/math-17-shapes.html" class="scroll-card card-blue"><span class="sc-icon">🏗️</span><span class="sc-name">图形拼搭</span></a>
<a href="courseware/math-18-sorting.html" class="scroll-card card-blue"><span class="sc-icon">📊</span><span class="sc-name">比较与排序</span></a>
<a href="courseware/math-19-statistics.html" class="scroll-card card-blue"><span class="sc-icon">📈</span><span class="sc-name">简单统计</span></a>
<a href="courseware/math-20-direction.html" class="scroll-card card-blue"><span class="sc-icon">🧭</span><span class="sc-name">位置与方向</span></a>
<a href="courseware/math-21-multiplication.html" class="scroll-card card-blue"><span class="sc-icon">✖️</span><span class="sc-name">乘法启蒙</span></a>
<a href="courseware/math-22-fractions.html" class="scroll-card card-blue"><span class="sc-icon">🍕</span><span class="sc-name">分数的故事</span></a>
<a href="courseware/math-23-word-problems.html" class="scroll-card card-blue"><span class="sc-icon">🧩</span><span class="sc-name">应用题挑战</span></a>
<a href="courseware/math-24-carnival.html" class="scroll-card card-blue"><span class="sc-icon">🎪</span><span class="sc-name">数学嘉年华</span></a>

</div>
</div>

<!-- ===== 🀄 语文-Minecraft ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🀄</span>
  <span class="sh-name">语文 Minecraft</span>
  <span class="sh-count">7 课</span>
  <a href="courseware/" class="sh-arrow">全部 →</a>
</div>
<div class="scroll-row">

<a href="courseware/chinese-01-characters.html" class="scroll-card card-red"><span class="sc-icon">☀️</span><span class="sc-name">日月山水火</span></a>
<a href="courseware/chinese-02-strokes.html" class="scroll-card card-red"><span class="sc-icon">✏️</span><span class="sc-name">基本笔画</span></a>
<a href="courseware/chinese-03-heaven-earth.html" class="scroll-card card-red"><span class="sc-icon">🌍</span><span class="sc-name">天地人</span></a>
<a href="courseware/chinese-04-nature.html" class="scroll-card card-red"><span class="sc-icon">🌤️</span><span class="sc-name">大自然</span></a>
<a href="courseware/chinese-05-family.html" class="scroll-card card-red"><span class="sc-icon">👨‍👩‍👧</span><span class="sc-name">我爱我家</span></a>
<a href="courseware/chinese-06-school.html" class="scroll-card card-red"><span class="sc-icon">🏫</span><span class="sc-name">开心学校</span></a>
<a href="courseware/chinese-07-pinyin.html" class="scroll-card card-red"><span class="sc-icon">🔤</span><span class="sc-name">拼音是什么</span></a>
<a href="courseware/chinese-08-pinyin2.html" class="scroll-card card-red"><span class="sc-icon">🎯</span><span class="sc-name">拼音魔法进阶</span></a>
<a href="courseware/chinese-09-shengmu1.html" class="scroll-card card-red"><span class="sc-icon">🅰️</span><span class="sc-name">声母王国上</span></a>
<a href="courseware/chinese-10-shengmu2.html" class="scroll-card card-red"><span class="sc-icon">🅱️</span><span class="sc-name">声母王国中</span></a>
<a href="courseware/chinese-11-shengmu3.html" class="scroll-card card-red"><span class="sc-icon">🆎</span><span class="sc-name">声母王国下</span></a>
<a href="courseware/chinese-12-yunmu.html" class="scroll-card card-red"><span class="sc-icon">🔊</span><span class="sc-name">韵母大冒险</span></a>
<a href="courseware/chinese-13-body.html" class="scroll-card card-red"><span class="sc-icon">🧍</span><span class="sc-name">我的身体</span></a>
<a href="courseware/chinese-14-colors.html" class="scroll-card card-red"><span class="sc-icon">🎨</span><span class="sc-name">数字与颜色</span></a>
<a href="courseware/chinese-15-food.html" class="scroll-card card-red"><span class="sc-icon">🍜</span><span class="sc-name">美味食物</span></a>
<a href="courseware/chinese-16-actions.html" class="scroll-card card-red"><span class="sc-icon">🏃</span><span class="sc-name">动作乐园</span></a>
<a href="courseware/chinese-17-direction-time.html" class="scroll-card card-red"><span class="sc-icon">🧭</span><span class="sc-name">方向与时间</span></a>
<a href="courseware/chinese-18-animals.html" class="scroll-card card-red"><span class="sc-icon">🐾</span><span class="sc-name">动物世界</span></a>
<a href="courseware/chinese-19-compound.html" class="scroll-card card-red"><span class="sc-icon">🧩</span><span class="sc-name">复合词的秘密</span></a>
<a href="courseware/chinese-20-reading.html" class="scroll-card card-red"><span class="sc-icon">📖</span><span class="sc-name">短句阅读</span></a>
<a href="courseware/chinese-21-antonyms.html" class="scroll-card card-red"><span class="sc-icon">↔️</span><span class="sc-name">反义词</span></a>
<a href="courseware/chinese-22-qa.html" class="scroll-card card-red"><span class="sc-icon">❓</span><span class="sc-name">我会问答</span></a>
<a href="courseware/chinese-23-poems.html" class="scroll-card card-red"><span class="sc-icon">📜</span><span class="sc-name">古诗三首</span></a>
<a href="courseware/chinese-24-adventure.html" class="scroll-card card-red"><span class="sc-icon">🎪</span><span class="sc-name">大冒险</span></a>

</div>
</div>

<!-- ===== 🇬🇧 英语-Minecraft ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🇬🇧</span>
  <span class="sh-name">英语 Minecraft</span>
  <span class="sh-count">7 课</span>
  <a href="courseware/" class="sh-arrow">全部 →</a>
</div>
<div class="scroll-row">

<a href="courseware/english-01-hello.html" class="scroll-card card-green"><span class="sc-icon">👋</span><span class="sc-name">Hello!</span></a>
<a href="courseware/english-02-abc.html" class="scroll-card card-green"><span class="sc-icon">🔤</span><span class="sc-name">ABC A-M</span></a>
<a href="courseware/english-03-abc-nz.html" class="scroll-card card-green"><span class="sc-icon">🆎</span><span class="sc-name">ABC N-Z</span></a>
<a href="courseware/english-04-colors.html" class="scroll-card card-green"><span class="sc-icon">🌈</span><span class="sc-name">Colors</span></a>
<a href="courseware/english-05-numbers.html" class="scroll-card card-green"><span class="sc-icon">🔢</span><span class="sc-name">Numbers 1-5</span></a>
<a href="courseware/english-06-family.html" class="scroll-card card-green"><span class="sc-icon">👨‍👩‍👧</span><span class="sc-name">Family</span></a>
<a href="courseware/english-07-animals.html" class="scroll-card card-green"><span class="sc-icon">🐾</span><span class="sc-name">Animals</span></a>
<a href="courseware/english-08-body.html" class="scroll-card card-green"><span class="sc-icon">🧍</span><span class="sc-name">Body</span></a>
<a href="courseware/english-09-food.html" class="scroll-card card-green"><span class="sc-icon">🍎</span><span class="sc-name">Food</span></a>
<a href="courseware/english-10-toys.html" class="scroll-card card-green"><span class="sc-icon">🧸</span><span class="sc-name">Toys</span></a>
<a href="courseware/english-11-weather.html" class="scroll-card card-green"><span class="sc-icon">🌤️</span><span class="sc-name">Weather</span></a>
<a href="courseware/english-12-clothes.html" class="scroll-card card-green"><span class="sc-icon">👕</span><span class="sc-name">Clothes</span></a>
<a href="courseware/english-13-actions.html" class="scroll-card card-green"><span class="sc-icon">🏃</span><span class="sc-name">Actions</span></a>
<a href="courseware/english-14-places.html" class="scroll-card card-green"><span class="sc-icon">🏘️</span><span class="sc-name">Places</span></a>
<a href="courseware/english-15-feelings.html" class="scroll-card card-green"><span class="sc-icon">😊</span><span class="sc-name">Feelings</span></a>
<a href="courseware/english-16-time.html" class="scroll-card card-green"><span class="sc-icon">⏰</span><span class="sc-name">Time</span></a>
<a href="courseware/english-17-transport.html" class="scroll-card card-green"><span class="sc-icon">🚗</span><span class="sc-name">Transport</span></a>
<a href="courseware/english-18-review.html" class="scroll-card card-green"><span class="sc-icon">📚</span><span class="sc-name">Review Week</span></a>
<a href="courseware/english-19-lost-cat.html" class="scroll-card card-green"><span class="sc-icon">🐱</span><span class="sc-name">Lost Cat</span></a>
<a href="courseware/english-20-storm.html" class="scroll-card card-green"><span class="sc-icon">🌩️</span><span class="sc-name">The Storm</span></a>
<a href="courseware/english-21-birthday.html" class="scroll-card card-green"><span class="sc-icon">🎂</span><span class="sc-name">Birthday Party</span></a>
<a href="courseware/english-22-farm.html" class="scroll-card card-green"><span class="sc-icon">🐄</span><span class="sc-name">At the Farm</span></a>
<a href="courseware/english-23-treasure.html" class="scroll-card card-green"><span class="sc-icon">🏴‍☠️</span><span class="sc-name">Treasure Hunt</span></a>
<a href="courseware/english-24-review.html" class="scroll-card card-green"><span class="sc-icon">🏆</span><span class="sc-name">Phase 4 Review</span></a>

</div>
</div>

<!-- ===== 🌈 其他英语 ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">📖</span>
  <span class="sh-name">英语绘本</span>
  <span class="sh-count">5 课</span>
</div>
<div class="scroll-row">

<a href="courseware/phonics-fat-cat.html" class="scroll-card card-green"><span class="sc-icon">🐱</span><span class="sc-name">Fat Cat Phonics</span></a>
<a href="courseware/sight-word-tales-come-to-the-party.html" class="scroll-card card-orange"><span class="sc-icon">🎉</span><span class="sc-name">Come to Party</span></a>
<a href="courseware/sight-word-tales-can-we-get-a-pet.html" class="scroll-card card-purple"><span class="sc-icon">🐱</span><span class="sc-name">Can We Get Pet</span></a>
<a href="courseware/elephant-piggie-surprise.html" class="scroll-card card-pink"><span class="sc-icon">🐘</span><span class="sc-name">Elephant &amp; Piggie</span></a>
<a href="courseware/i-am-an-apple.html" class="scroll-card card-red"><span class="sc-icon">🍎</span><span class="sc-name">I Am an Apple</span></a>

</div>
</div>

<!-- ===== 📚 绘本阅读 (新) ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">📚</span>
  <span class="sh-name">绘本阅读</span>
  <span class="sh-count">6 本</span>
</div>
<div class="scroll-row">

<a href="./books/pete_cat.md" class="scroll-card card-red"><span class="sc-icon">🐱</span><span class="sc-name">Pete the Cat</span></a>
<a href="./books/pigeon_bus.md" class="scroll-card card-orange"><span class="sc-icon">🚌</span><span class="sc-name">Don't Let Pigeon</span></a>
<a href="./books/crayons_quit.md" class="scroll-card card-yellow"><span class="sc-icon">🖍️</span><span class="sc-name">Crayons Quit</span></a>
<a href="./books/gruffalo.md" class="scroll-card card-brown"><span class="sc-icon">🐭</span><span class="sc-name">The Gruffalo</span></a>
<a href="./books/knuffle_bunny.md" class="scroll-card card-pink"><span class="sc-icon">🐰</span><span class="sc-name">Knuffle Bunny</span></a>
<a href="./books/little_critter.md" class="scroll-card card-green"><span class="sc-icon">🐿️</span><span class="sc-name">Little Critter</span></a>
<a href="./books/wild_things.md" class="scroll-card card-blue"><span class="sc-icon">👹</span><span class="sc-name">Wild Things</span></a>
<a href="./books/winnie_witch.md" class="scroll-card card-purple"><span class="sc-icon">🧙</span><span class="sc-name">Winnie Witch</span></a>

</div>
</div>

<!-- ===== 🌱 科学 ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🌱</span>
  <span class="sh-name">科学</span>
  <span class="sh-count">3 课</span>
</div>
<div class="scroll-row">

<a href="courseware/rainforest-adventure.html" class="scroll-card card-green"><span class="sc-icon">🌴</span><span class="sc-name">雨林大冒险</span></a>
<a href="courseware/gears-transmission.html" class="scroll-card card-orange"><span class="sc-icon">⚙️</span><span class="sc-name">齿轮传动</span></a>
<a href="courseware/nature-lesson-4.html" class="scroll-card card-blue"><span class="sc-icon">🌿</span><span class="sc-name">大自然识字</span></a>

</div>
</div>

<!-- ===== 📚 中文绘本故事 (新) ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">📚</span>
  <span class="sh-name">中文绘本故事</span>
  <span class="sh-count">10 个</span>
</div>
<div class="scroll-row">

<a href="courseware/story_extra_01_小蜗牛慢慢游历记.html" class="scroll-card card-purple card-new"><span class="sc-icon">🐌</span><span class="sc-name">小蜗牛慢慢游历记</span></a>
<a href="courseware/story_extra_02_会唱歌的石头.html" class="scroll-card card-purple card-new"><span class="sc-icon">🎵</span><span class="sc-name">会唱歌的石头</span></a>
<a href="courseware/story_extra_03_森林里的圣诞节.html" class="scroll-card card-purple card-new"><span class="sc-icon">🎄</span><span class="sc-name">森林里的圣诞节</span></a>
<a href="courseware/story_extra_04_小鱼的美人鱼梦.html" class="scroll-card card-purple card-new"><span class="sc-icon">🧜</span><span class="sc-name">小鱼的美人鱼梦</span></a>
<a href="courseware/story_extra_05_时间的魔法.html" class="scroll-card card-purple card-new"><span class="sc-icon">⏰</span><span class="sc-name">时间的魔法</span></a>
<a href="courseware/story_extra_06_彩虹尽头的宝藏.html" class="scroll-card card-purple card-new"><span class="sc-icon">🌈</span><span class="sc-name">彩虹尽头的宝藏</span></a>
<a href="courseware/story_extra_07_小象的超级长鼻子.html" class="scroll-card card-purple card-new"><span class="sc-icon">🐘</span><span class="sc-name">小象的超级长鼻子</span></a>
<a href="courseware/story_extra_08_会变色的兔子.html" class="scroll-card card-purple card-new"><span class="sc-icon">🐰</span><span class="sc-name">会变色的兔子</span></a>
<a href="courseware/story_extra_09_图书馆里的龙.html" class="scroll-card card-purple card-new"><span class="sc-icon">🐉</span><span class="sc-name">图书馆里的龙</span></a>
<a href="courseware/story_extra_10_太空小探险家.html" class="scroll-card card-purple card-new"><span class="sc-icon">🚀</span><span class="sc-name">太空小探险家</span></a>

</div>
</div>

<!-- ===== 📖 英文故事 (新) ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">📖</span>
  <span class="sh-name">英文故事</span>
  <span class="sh-count">10 个</span>
</div>
<div class="scroll-row">

<a href="courseware/english_story_01_The_Talkative_Tortoise.html" class="scroll-card card-green card-new"><span class="sc-icon">🐢</span><span class="sc-name">Talkative Tortoise</span></a>
<a href="courseware/english_story_02_The_Lion_and_the_Mouse.html" class="scroll-card card-green card-new"><span class="sc-icon">🦁</span><span class="sc-name">Lion and Mouse</span></a>
<a href="courseware/english_story_03_The_Ugly_Duckling.html" class="scroll-card card-green card-new"><span class="sc-icon">🦢</span><span class="sc-name">Ugly Duckling</span></a>
<a href="courseware/english_story_04_The_Boy_Who_Cried_Wolf.html" class="scroll-card card-green card-new"><span class="sc-icon">🐺</span><span class="sc-name">Boy Cried Wolf</span></a>
<a href="courseware/english_story_05_The_Three_Little_Pigs.html" class="scroll-card card-green card-new"><span class="sc-icon">🐷</span><span class="sc-name">Three Little Pigs</span></a>
<a href="courseware/english_story_06_Goldilocks_and_the_Three_Bears.html" class="scroll-card card-green card-new"><span class="sc-icon">🐻</span><span class="sc-name">Goldilocks Bears</span></a>
<a href="courseware/english_story_07_The_Ant_and_the_Grasshopper.html" class="scroll-card card-green card-new"><span class="sc-icon">🦗</span><span class="sc-name">Ant Grasshopper</span></a>
<a href="courseware/english_story_08_Little_Red_Riding_Hood.html" class="scroll-card card-green card-new"><span class="sc-icon">🧣</span><span class="sc-name">Little Red Hood</span></a>
<a href="courseware/english_story_09_The_Tortoise_and_the_Hare.html" class="scroll-card card-green card-new"><span class="sc-icon">🐇</span><span class="sc-name">Tortoise Hare</span></a>
<a href="courseware/english_story_10_Jack_and_the_Beanstalk.html" class="scroll-card card-green card-new"><span class="sc-icon">🌱</span><span class="sc-name">Jack Beanstalk</span></a>

</div>
</div>

<!-- ===== 🎓 教案活动 (新) ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🎓</span>
  <span class="sh-name">教案活动</span>
  <span class="sh-count">10 个</span>
</div>
<div class="scroll-row">

<a href="courseware/lesson_extra_01_数学启蒙：比大小.html" class="scroll-card card-orange card-new"><span class="sc-icon">🔢</span><span class="sc-name">比大小</span></a>
<a href="courseware/lesson_extra_02_科学实验：吹泡泡.html" class="scroll-card card-orange card-new"><span class="sc-icon">🫧</span><span class="sc-name">吹泡泡</span></a>
<a href="courseware/lesson_extra_03_艺术创作：手指画.html" class="scroll-card card-orange card-new"><span class="sc-icon">🎨</span><span class="sc-name">手指画</span></a>
<a href="courseware/lesson_extra_04_语言游戏：绕口令.html" class="scroll-card card-orange card-new"><span class="sc-icon">🗣️</span><span class="sc-name">绕口令</span></a>
<a href="courseware/lesson_extra_05_户外活动：观察昆虫.html" class="scroll-card card-orange card-new"><span class="sc-icon">🐛</span><span class="sc-name">观察昆虫</span></a>
<a href="courseware/lesson_extra_06_音乐活动：打击乐器.html" class="scroll-card card-orange card-new"><span class="sc-icon">🥁</span><span class="sc-name">打击乐器</span></a>
<a href="courseware/lesson_extra_07_社会认知：认识职业.html" class="scroll-card card-orange card-new"><span class="sc-icon">👨‍⚕️</span><span class="sc-name">认识职业</span></a>
<a href="courseware/lesson_extra_08_健康教育：正确洗手.html" class="scroll-card card-orange card-new"><span class="sc-icon">🧼</span><span class="sc-name">正确洗手</span></a>
<a href="courseware/lesson_extra_09_数学游戏：分类整理.html" class="scroll-card card-orange card-new"><span class="sc-icon">📦</span><span class="sc-name">分类整理</span></a>
<a href="courseware/lesson_extra_10_创意构建：纸杯搭建.html" class="scroll-card card-orange card-new"><span class="sc-icon">🥤</span><span class="sc-name">纸杯搭建</span></a>

</div>
</div>

<!-- ===== 🏯 古诗讲解 (新) ===== -->
<div class="section">
<div class="section-header">
  <span class="sh-icon">🏯</span>
  <span class="sh-name">古诗讲解</span>
  <span class="sh-count">20 个</span>
</div>
<div class="scroll-row">

<a href="courseware/poem_explain_01_咏鹅.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 01</span></a>
<a href="courseware/poem_explain_02_春晓.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 02</span></a>
<a href="courseware/poem_explain_03_静夜思.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 03</span></a>
<a href="courseware/poem_explain_04_悯农.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 04</span></a>
<a href="courseware/poem_explain_05_登鹳雀楼.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 05</span></a>
<a href="courseware/poem_explain_06_望庐山瀑布.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 06</span></a>
<a href="courseware/poem_explain_07_江雪.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 07</span></a>
<a href="courseware/poem_explain_08_游子吟.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 08</span></a>
<a href="courseware/poem_explain_09_相思.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 09</span></a>
<a href="courseware/poem_explain_10_鹿柴.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 10</span></a>
<a href="courseware/poem_explain_11_鸟鸣涧.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 11</span></a>
<a href="courseware/poem_explain_12_竹里馆.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 12</span></a>
<a href="courseware/poem_explain_13_送别.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 13</span></a>
<a href="courseware/poem_explain_14_杂诗.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 14</span></a>
<a href="courseware/poem_explain_15_山中送别.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 15</span></a>
<a href="courseware/poem_explain_16_书事.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 16</span></a>
<a href="courseware/poem_explain_17_辛夷坞.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 17</span></a>
<a href="courseware/poem_explain_18_漆园.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 18</span></a>
<a href="courseware/poem_explain_19_辋川闲居.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 19</span></a>
<a href="courseware/poem_explain_20_田园乐.html" class="scroll-card card-red card-new"><span class="sc-icon">📜</span><span class="sc-name">古诗讲解 20</span></a>

</div>
</div>

<div style="text-align:center;margin:16px 0">
  <a href="courseware/" style="display:inline-flex;align-items:center;gap:6px;padding:8px 22px;border-radius:30px;background:linear-gradient(135deg,#FFB347,#FF8C42);color:white;font-size:14px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(255,179,71,0.4);">📚 查看全部课件 →</a>
</div>
