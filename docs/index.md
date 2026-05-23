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
    <span class="stat-item">📚 共 <strong>60</strong> 堂课</span>
    <span class="stat-item">🎵 <strong>27</strong> 首童谣</span>
    <span class="stat-item">🔤 <strong>8</strong> 个英语课</span>
    <span class="stat-item">🌿 <strong>2</strong> 个科学课</span>
    <span class="stat-item">🀄 <strong>8</strong> 个语文课</span>
    <span class="stat-item">🔢 <strong>9</strong> 个数学课</span>
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

<div style="text-align:center;margin:16px 0">
  <a href="courseware/" style="display:inline-flex;align-items:center;gap:6px;padding:8px 22px;border-radius:30px;background:linear-gradient(135deg,#FFB347,#FF8C42);color:white;font-size:14px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(255,179,71,0.4);">📚 查看全部课件 →</a>
</div>
