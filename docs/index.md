# 🎪 小朋友的互动学习乐园

<style>
/* ===== 全局 ===== */
*{box-sizing:border-box}
body{background:#FFF8E7}

/* ===== 头部 ===== */
.play-header{text-align:center;padding:14px 0 6px}
.play-header h1{font-size:30px;margin:4px 0;color:#E8751A;font-weight:800}
.play-header .subtitle{font-size:15px;color:#8D6E63;margin:2px 0}
.play-header .stats{display:flex;justify-content:center;gap:8px;margin:8px 0;flex-wrap:wrap}
.play-header .stat-item{background:#FFFCF5;border-radius:20px;padding:5px 16px;font-size:13px;font-weight:600;color:#5D4037;border:2px solid #FFE0B2}

/* ===== 分类大卡片 ===== */
.cat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:14px 0;max-width:900px;margin-left:auto;margin-right:auto}
.cat-card{border-radius:24px;padding:20px 16px;text-align:center;cursor:pointer;transition:all .3s cubic-bezier(0.34,1.56,0.64,1);border:3px solid transparent;position:relative;overflow:hidden;user-select:none;touch-action:manipulation}
.cat-card:hover{transform:translateY(-4px) scale(1.03);box-shadow:0 12px 32px rgba(0,0,0,0.12)}
.cat-card:active{transform:scale(0.97)}
.cat-card .cat-icon{font-size:44px;display:block;margin:0 auto 6px;line-height:1.2}
.cat-card .cat-name{font-size:20px;font-weight:800;margin:2px 0;display:block}
.cat-card .cat-count{font-size:13px;opacity:.75;display:block;margin-top:2px}
.cat-card .cat-arrow{display:block;margin-top:6px;font-size:16px;transition:transform .35s ease}
.cat-card.open .cat-arrow{transform:rotate(180deg)}

/* 颜色主题 */
.cat-purple{background:linear-gradient(145deg,#F3E5F5,#E1BEE7);border-color:#CE93D8;color:#6A1B9A}
.cat-purple:hover{border-color:#AB47BC;box-shadow:0 8px 24px rgba(171,71,188,0.25)}
.cat-blue{background:linear-gradient(145deg,#E3F2FD,#BBDEFB);border-color:#90CAF9;color:#1565C0}
.cat-blue:hover{border-color:#42A5F5;box-shadow:0 8px 24px rgba(66,165,245,0.25)}
.cat-green{background:linear-gradient(145deg,#E8F5E9,#C8E6C9);border-color:#A5D6A7;color:#2E7D32}
.cat-green:hover{border-color:#66BB6A;box-shadow:0 8px 24px rgba(102,187,106,0.25)}
.cat-red{background:linear-gradient(145deg,#FFEBEE,#FFCDD2);border-color:#EF9A9A;color:#B71C1C}
.cat-red:hover{border-color:#EF5350;box-shadow:0 8px 24px rgba(239,83,80,0.25)}

/* ===== 子卡片容器 ===== */
.sub-container{max-width:900px;margin:0 auto;overflow:hidden;transition:all .4s ease;max-height:0;opacity:0}
.sub-container.open{max-height:5000px;opacity:1;margin:6px auto 14px}
.sub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.sub-card{background:#FFFCF5;border-radius:16px;padding:10px 8px;text-align:center;text-decoration:none;color:inherit;display:flex;flex-direction:column;align-items:center;box-shadow:0 2px 8px rgba(0,0,0,0.06);border:2px solid #FFF;transition:all .2s cubic-bezier(0.34,1.56,0.64,1);position:relative}
.sub-card:hover{transform:translateY(-3px) scale(1.05);border-color:#FFB347;box-shadow:0 6px 20px rgba(255,179,71,0.2)}
.sub-card:active{transform:scale(0.95)}
.sub-card .s-icon{font-size:30px;line-height:1.2}
.sub-card .s-name{font-size:13px;font-weight:700;margin:4px 0 2px;color:#5D4037;line-height:1.3}
.sub-card .s-tag{font-size:10px;padding:2px 10px;border-radius:12px;font-weight:600;display:inline-block}
.sub-card.card-new::after{content:'🆕';position:absolute;top:-6px;right:-6px;font-size:13px}

/* ===== 响应式 ===== */
@media(max-width:820px){.cat-grid{grid-template-columns:repeat(2,1fr);gap:10px}}
@media(max-width:500px){.cat-grid{grid-template-columns:repeat(2,1fr);gap:8px}
  .cat-card{padding:14px 10px}.cat-card .cat-icon{font-size:34px}.cat-card .cat-name{font-size:17px}
  .sub-grid{grid-template-columns:repeat(2,1fr);gap:6px}
  .sub-card .s-icon{font-size:24px}.sub-card .s-name{font-size:12px}
  .play-header h1{font-size:24px}
}
</style>

<script>
// ===== 分类展开/收起 =====
document.addEventListener('DOMContentLoaded', function(){
  var cats = document.querySelectorAll('.cat-card');
  cats.forEach(function(cat){
    cat.addEventListener('click', function(){
      var target = this.getAttribute('data-target');
      var container = document.getElementById(target);
      if(!container) return;
      var isOpen = container.classList.contains('open');
      // 收起所有
      document.querySelectorAll('.sub-container').forEach(function(c){c.classList.remove('open')});
      document.querySelectorAll('.cat-card').forEach(function(c){c.classList.remove('open')});
      // 展开点击的
      if(!isOpen){
        container.classList.add('open');
        this.classList.add('open');
      }
    });
  });
});
</script>

<div class="play-header">
  <h1>🎪 小朋友的互动学习乐园</h1>
  <p class="subtitle">✨ 每堂课都有互动游戏和语音朗读 🎧</p>
  <div class="stats">
    <span class="stat-item">📚 共 <strong>35</strong> 堂课</span>
    <span class="stat-item">🎵 <strong>27</strong> 首童谣</span>
    <span class="stat-item">🔤 <strong>5</strong> 个英语课</span>
    <span class="stat-item">🌱 <strong>3</strong> 个科学课</span>
    <span class="stat-item">🀄 <strong>1</strong> 个语文课</span>
  </div>
</div>

<!-- ===== 分类大卡片 ===== -->
<div class="cat-grid">

<div class="cat-card cat-purple" data-target="sub-nursery">
  <span class="cat-icon">🎵</span>
  <span class="cat-name">童谣</span>
  <span class="cat-count">27 首儿歌</span>
  <span class="cat-arrow">▼</span>
</div>

<div class="cat-card cat-blue" data-target="sub-english">
  <span class="cat-icon">🔤</span>
  <span class="cat-name">英语</span>
  <span class="cat-count">5 个英语课</span>
  <span class="cat-arrow">▼</span>
</div>

<div class="cat-card cat-green" data-target="sub-science">
  <span class="cat-icon">🌱</span>
  <span class="cat-name">科学</span>
  <span class="cat-count">3 个科普课</span>
  <span class="cat-arrow">▼</span>
</div>

<div class="cat-card cat-red" data-target="sub-chinese">
  <span class="cat-icon">🀄</span>
  <span class="cat-name">语文</span>
  <span class="cat-count">1 堂识字课</span>
  <span class="cat-arrow">▼</span>
</div>

</div>

<!-- ===== 童谣子卡片 ===== -->
<div class="sub-container" id="sub-nursery">
<div class="sub-grid">

<a href="courseware/twinkle-twinkle.html" class="sub-card"><span class="s-icon">🌟</span><span class="s-name">Twinkle Twinkle</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/old-macdonald.html" class="sub-card"><span class="s-icon">🚜</span><span class="s-name">Old MacDonald</span><span class="s-tag" style="background:#FFF3E0;color:#E65100">🎵 童谣</span></a>
<a href="courseware/five-little-monkeys.html" class="sub-card"><span class="s-icon">🐵</span><span class="s-name">5 Little Monkeys</span><span class="s-tag" style="background:#FFFDE7;color:#F57F17">🎵 童谣</span></a>
<a href="courseware/wheels-on-bus.html" class="sub-card"><span class="s-icon">🚌</span><span class="s-name">Wheels on Bus</span><span class="s-tag" style="background:#E3F2FD;color:#1565C0">🎵 童谣</span></a>
<a href="courseware/itsy-bitsy-spider.html" class="sub-card"><span class="s-icon">🕷️</span><span class="s-name">Itsy Bitsy Spider</span><span class="s-tag" style="background:#E8F5E9;color:#2E7D32">🎵 童谣</span></a>
<a href="courseware/row-your-boat.html" class="sub-card"><span class="s-icon">🚣</span><span class="s-name">Row Your Boat</span><span class="s-tag" style="background:#E8F5E9;color:#2E7D32">🎵 童谣</span></a>
<a href="courseware/bingo.html" class="sub-card"><span class="s-icon">🐶</span><span class="s-name">BINGO</span><span class="s-tag" style="background:#FFFDE7;color:#F57F17">🎵 童谣</span></a>
<a href="courseware/abc-song.html" class="sub-card"><span class="s-icon">🔤</span><span class="s-name">ABC Song</span><span class="s-tag" style="background:#FFEBEE;color:#C62828">🎵 童谣</span></a>
<a href="courseware/head-shoulders.html" class="sub-card"><span class="s-icon">🧍</span><span class="s-name">Head Shoulders</span><span class="s-tag" style="background:#FCE4EC;color:#AD1457">🎵 童谣</span></a>
<a href="courseware/humpty-dumpty.html" class="sub-card"><span class="s-icon">🥚</span><span class="s-name">Humpty Dumpty</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/if-youre-happy.html" class="sub-card"><span class="s-icon">😊</span><span class="s-name">If You're Happy</span><span class="s-tag" style="background:#FFF3E0;color:#E65100">🎵 童谣</span></a>
<a href="courseware/london-bridge.html" class="sub-card"><span class="s-icon">🌉</span><span class="s-name">London Bridge</span><span class="s-tag" style="background:#E3F2FD;color:#1565C0">🎵 童谣</span></a>
<a href="courseware/mary-lamb.html" class="sub-card"><span class="s-icon">🐑</span><span class="s-name">Mary's Little Lamb</span><span class="s-tag" style="background:#FCE4EC;color:#AD1457">🎵 童谣</span></a>
<a href="courseware/jack-and-jill.html" class="sub-card card-new"><span class="s-icon">⛰️</span><span class="s-name">Jack and Jill</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/pat-a-cake.html" class="sub-card card-new"><span class="s-icon">🎂</span><span class="s-name">Pat-A-Cake</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/hush-little-baby.html" class="sub-card card-new"><span class="s-icon">🌙</span><span class="s-name">Hush Little Baby</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/mulberry-bush.html" class="sub-card card-new"><span class="s-icon">🌳</span><span class="s-name">Mulberry Bush</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/skidamarink.html" class="sub-card card-new"><span class="s-icon">💕</span><span class="s-name">Skidamarink</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/silent-night.html" class="sub-card card-new"><span class="s-icon">⭐</span><span class="s-name">Silent Night</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/three-blind-mice.html" class="sub-card card-new"><span class="s-icon">🐭</span><span class="s-name">Three Blind Mice</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/hickory-dickory.html" class="sub-card card-new"><span class="s-icon">🕰️</span><span class="s-name">Hickory Dickory</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/rain-go-away.html" class="sub-card card-new"><span class="s-icon">🌧️</span><span class="s-name">Rain Go Away</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/baa-baa-black-sheep.html" class="sub-card card-new"><span class="s-icon">🐑</span><span class="s-name">Baa Baa Black Sheep</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/cat-and-fiddle.html" class="sub-card card-new"><span class="s-icon">🎻</span><span class="s-name">Cat and Fiddle</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/yankee-doodle.html" class="sub-card card-new"><span class="s-icon">🎩</span><span class="s-name">Yankee Doodle</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/ring-around-rosy.html" class="sub-card card-new"><span class="s-icon">🌸</span><span class="s-name">Ring Around Rosy</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>
<a href="courseware/jack-be-nimble.html" class="sub-card card-new"><span class="s-icon">🕯️</span><span class="s-name">Jack Be Nimble</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🎵 童谣</span></a>

</div>
</div>

<!-- ===== 英语子卡片 ===== -->
<div class="sub-container" id="sub-english">
<div class="sub-grid">

<a href="courseware/phonics-fat-cat.html" class="sub-card"><span class="s-icon">🐱</span><span class="s-name">Fat Cat Phonics</span><span class="s-tag" style="background:#E8F5E9;color:#2E7D32">🔤 英语</span></a>
<a href="courseware/sight-word-tales-come-to-the-party.html" class="sub-card"><span class="s-icon">🎉</span><span class="s-name">Come to Party</span><span class="s-tag" style="background:#FFF3E0;color:#E65100">🔤 英语</span></a>
<a href="courseware/sight-word-tales-can-we-get-a-pet.html" class="sub-card"><span class="s-icon">🐱</span><span class="s-name">Can We Get Pet</span><span class="s-tag" style="background:#F3E5F5;color:#7B1FA2">🔤 英语</span></a>
<a href="courseware/elephant-piggie-surprise.html" class="sub-card"><span class="s-icon">🐘</span><span class="s-name">Elephant &amp; Piggie</span><span class="s-tag" style="background:#FCE4EC;color:#AD1457">🔤 英语</span></a>
<a href="courseware/i-am-an-apple.html" class="sub-card"><span class="s-icon">🍎</span><span class="s-name">I Am an Apple</span><span class="s-tag" style="background:#FFEBEE;color:#C62828">🔤 英语</span></a>

</div>
</div>

<!-- ===== 科学子卡片 ===== -->
<div class="sub-container" id="sub-science">
<div class="sub-grid">

<a href="courseware/gears-transmission.html" class="sub-card"><span class="s-icon">⚙️</span><span class="s-name">齿轮传动</span><span class="s-tag" style="background:#FFF3E0;color:#E65100">🌱 科学</span></a>
<a href="courseware/rainforest-adventure.html" class="sub-card"><span class="s-icon">🌴</span><span class="s-name">雨林大冒险</span><span class="s-tag" style="background:#E8F5E9;color:#2E7D32">🌱 科学</span></a>
<a href="courseware/nature-lesson-4.html" class="sub-card"><span class="s-icon">🌿</span><span class="s-name">大自然识字</span><span class="s-tag" style="background:#E3F2FD;color:#1565C0">🌱 科学</span></a>

</div>
</div>

<!-- ===== 语文子卡片 ===== -->
<div class="sub-container" id="sub-chinese">
<div class="sub-grid">

<a href="courseware/nature-lesson-4.html" class="sub-card"><span class="s-icon">🌿</span><span class="s-name">大自然识字</span><span class="s-tag" style="background:#E3F2FD;color:#1565C0">🀄 语文</span></a>

</div>
</div>

<div style="text-align:center;margin:16px 0">
  <a href="courseware/" style="display:inline-flex;align-items:center;gap:6px;padding:8px 22px;border-radius:30px;background:linear-gradient(135deg,#FFB347,#FF8C42);color:white;font-size:14px;font-weight:700;text-decoration:none;box-shadow:0 4px 14px rgba(255,179,71,0.4);">📚 查看全部课件 →</a>
</div>
