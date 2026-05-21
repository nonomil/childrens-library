# 🎪 小朋友的互动学习乐园

<style>
  /* ===== 乐园主题 ===== */
  .play-header {
    text-align: center;
    padding: 20px 0 8px;
  }
  .play-header h1 {
    font-size: 2.8rem;
    color: #FF8C42;
    margin: 0;
    text-shadow: 0 3px 8px rgba(255,140,66,0.2);
  }
  .play-header .subtitle {
    font-size: 1.1rem;
    color: #8D6E63;
    margin: 6px 0 0;
  }
  .play-header .stats {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 12px 0;
    flex-wrap: wrap;
  }
  .play-header .stat-item {
    background: #FFFCF5;
    border-radius: 30px;
    padding: 6px 18px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #5D4037;
    border: 2px solid #FFE0B2;
  }
  .back-home {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 6px 16px;
    border-radius: 30px;
    background: #FFFCF5;
    color: #E8751A;
    text-decoration: none;
    font-size: 14px;
    font-weight: 700;
    margin: 0 0 12px;
    border: 2px solid #FFE0B2;
    transition: 0.2s;
  }
  .back-home:hover {
    background: #FFE0B2;
    transform: translateX(-3px);
  }

  /* ===== 分类标题 ===== */
  .cat-section { margin: 28px 0 12px; }
  .cat-title {
    font-size: 1.6rem;
    font-weight: 800;
    padding: 6px 16px;
    border-radius: 20px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
  }
  .cat-title .en { font-size: 0.9rem; font-weight: 400; opacity: 0.7; }

  /* ===== 卡片网格 ===== */
  .course-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 18px;
    margin: 0 0 8px;
  }
  .course-card {
    background: #FFFCF5;
    border-radius: 24px;
    padding: 22px 18px 18px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.07);
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.25s;
    border: 3px solid transparent;
    position: relative;
  }
  .course-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 14px 40px rgba(0,0,0,0.13);
  }
  .course-card .icon { font-size: 56px; line-height: 1.2; margin-bottom: 6px; }
  .course-card h3 { font-size: 19px; margin: 4px 0 5px; color: #333; font-weight: 700; }
  .course-card .tags { margin: 4px 0; }
  .course-card .tag {
    display: inline-block; padding: 2px 10px; border-radius: 16px;
    font-size: 11px; font-weight: 600; margin: 2px;
  }
  .course-card p { font-size: 13px; color: #888; margin: 6px 0 10px; line-height: 1.5; }
  .course-card .btn-start {
    display: inline-block; padding: 8px 20px; border-radius: 30px;
    font-size: 14px; font-weight: 700; color: white;
    text-decoration: none; transition: transform 0.15s;
  }
  .course-card .btn-start:hover { transform: scale(1.08); }

  /* ===== 颜色主题 ===== */
  .card-red { border-color: #FF6B6B; }
  .card-red .btn-start { background: #FF6B6B; }
  .card-red h3 { color: #D94F4F; }
  .card-orange { border-color: #FFB347; }
  .card-orange .btn-start { background: #FFB347; }
  .card-orange h3 { color: #E07C00; }
  .card-green { border-color: #4ECDC4; }
  .card-green .btn-start { background: #4ECDC4; }
  .card-green h3 { color: #2E9E95; }
  .card-purple { border-color: #A78BFA; }
  .card-purple .btn-start { background: #A78BFA; }
  .card-purple h3 { color: #7C5CFC; }
  .card-blue { border-color: #667eea; }
  .card-blue .btn-start { background: #667eea; }
  .card-blue h3 { color: #4C63D4; }
  .card-pink { border-color: #FF9FF3; }
  .card-pink .btn-start { background: #FF9FF3; }
  .card-pink h3 { color: #D96FC4; }
  .card-yellow { border-color: #FFD93D; }
  .card-yellow .btn-start { background: #FFD93D; }
  .card-yellow h3 { color: #C79500; }

  /* ===== 标签 ===== */
  .tag-red { background: #FFE0E0; color: #D94F4F; }
  .tag-orange { background: #FFF0E0; color: #E07C00; }
  .tag-green { background: #E0F5F0; color: #2E9E95; }
  .tag-purple { background: #EEE0FF; color: #7C5CFC; }
  .tag-blue { background: #E0E8FF; color: #4C63D4; }
  .tag-pink { background: #FFE0F0; color: #D96FC4; }
  .tag-yellow { background: #FFF8E0; color: #C79500; }

  /* ===== NEW 徽章 ===== */
  .card-new::after {
    content: '🆕'; position: absolute; top: -8px; right: -8px;
    font-size: 20px;
    animation: badge-pop 1.5s ease-in-out infinite;
  }
  @keyframes badge-pop {
    0%,100% { transform: scale(1); }
    50% { transform: scale(1.2); }
  }

  /* ===== 分隔装饰 ===== */
  .section-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #FFE0B2, #FFB347, #FFE0B2, transparent);
    margin: 6px 0 10px;
  }

  /* ===== 群星闪烁 ===== */
  @keyframes twinkle {
    0%,100% { opacity: 0.3; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
  }
  .sparkle-star {
    display: inline-block;
    animation: twinkle 2s ease-in-out infinite;
  }
  .sparkle-star:nth-child(2) { animation-delay: 0.7s; }
  .sparkle-star:nth-child(3) { animation-delay: 1.4s; }

  @media (max-width: 600px) {
    .play-header h1 { font-size: 2rem; }
    .course-grid { grid-template-columns: 1fr; }
    .course-card .icon { font-size: 44px; }
    .course-card h3 { font-size: 17px; }
    .cat-title { font-size: 1.3rem; }
    .play-header .stats { gap: 8px; }
    .play-header .stat-item { font-size: 0.8rem; padding: 4px 12px; }
  }
</style>

<div class="play-header">
  <a href="../" class="back-home">🏠 回到主页</a>

  <h1>🎪 小朋友的互动学习乐园</h1>
  <p class="subtitle">✨ 点卡片开始玩！每堂课都有互动游戏和语音朗读 🎧</p>

  <div class="stats">
    <span class="stat-item">📚 共 <strong>11</strong> 堂课</span>
    <span class="stat-item">🎵 <strong>3</strong> 首童谣</span>
    <span class="stat-item">🔤 <strong>5</strong> 个英语课</span>
    <span class="stat-item">🌱 <strong>3</strong> 个科学课</span>
  </div>
</div>

---

## 🎵 童谣 Nursery Rhymes <span class="sparkle-star">⭐</span><span class="sparkle-star">⭐</span><span class="sparkle-star">⭐</span>

<div class="section-divider"></div>

<div class="course-grid">

  <a href="twinkle-twinkle.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-purple card-new">
      <div class="icon">🌟</div>
      <h3>Twinkle Twinkle Little Star</h3>
      <div class="tags">
        <span class="tag tag-purple">🎵 童谣</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>一闪一闪亮晶晶！拼单词+找星星游戏<br>🎵 用钢琴声弹奏完整旋律</p>
      <span class="btn-start">🎵 听儿歌</span>
    </div>
  </a>

  <a href="old-macdonald.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-orange card-new">
      <div class="icon">🚜</div>
      <h3>Old MacDonald Had a Farm</h3>
      <div class="tags">
        <span class="tag tag-orange">🎵 童谣</span>
        <span class="tag tag-green">🐮 动物</span>
      </div>
      <p>E-I-E-I-O！听声音配对动物<br>🎵 认识 cow/pig/duck 和它们的叫声</p>
      <span class="btn-start">🎵 听儿歌</span>
    </div>
  </a>

  <a href="five-little-monkeys.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-yellow">
      <div class="icon">🐵</div>
      <h3>Five Little Monkeys</h3>
      <div class="tags">
        <span class="tag tag-yellow">🎵 童谣</span>
        <span class="tag tag-orange">🔢 数数</span>
      </div>
      <p>5只小猴跳床咯！点击小猴学数字<br>🎵 一边唱一边从5倒数到0</p>
      <span class="btn-start">🎵 听儿歌</span>
    </div>
  </a>

</div>

## 🔤 英语 Phonics & Reading

<div class="section-divider"></div>

<div class="course-grid">

  <a href="phonics-fat-cat.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-green">
      <div class="icon">🐱</div>
      <h3>Fat Cat on a Mat</h3>
      <div class="tags">
        <span class="tag tag-green">🔤 自然拼读</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>Usborne风格拼读故事<br>每页拼词互动，点一点学发音</p>
      <span class="btn-start">🔤 学拼读</span>
    </div>
  </a>

  <a href="sight-word-tales-come-to-the-party.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-blue">
      <div class="icon">🎉</div>
      <h3>Come to the Party!</h3>
      <div class="tags">
        <span class="tag tag-blue">📖 高频词</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>学习高频词 "come" "to"<br>互动绘本 + 找词游戏</p>
      <span class="btn-start">📖 开始读</span>
    </div>
  </a>

  <a href="sight-word-tales-can-we-get-a-pet.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-pink">
      <div class="icon">🐱</div>
      <h3>Can We Get a Pet?</h3>
      <div class="tags">
        <span class="tag tag-pink">📖 高频词</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>学习高频词 "can" "we"<br>互动绘本 + 找词游戏</p>
      <span class="btn-start">📖 开始读</span>
    </div>
  </a>

  <a href="elephant-piggie-surprise.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-purple">
      <div class="icon">🐘🐷</div>
      <h3>I Will Surprise My Friend!</h3>
      <div class="tags">
        <span class="tag tag-purple">💬 对话故事</span>
        <span class="tag tag-red">😊 情绪</span>
      </div>
      <p>Elephant & Piggie 风格故事<br>角色对话 + 情绪选择游戏</p>
      <span class="btn-start">💬 读故事</span>
    </div>
  </a>

</div>

## 🌱 科学探索 Science

<div class="section-divider"></div>

<div class="course-grid">

  <a href="i-am-an-apple.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-green">
      <div class="icon">🍎</div>
      <h3>I Am an Apple</h3>
      <div class="tags">
        <span class="tag tag-green">🌱 科学</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>认识苹果的生命周期！<br>从种子到果实，互动小测验</p>
      <span class="btn-start">🌱 学科学</span>
    </div>
  </a>

  <a href="gears-transmission.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-red">
      <div class="icon">⚙️</div>
      <h3>齿轮传动小世界</h3>
      <div class="tags">
        <span class="tag tag-red">🔧 机械</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>点齿轮、转链条、修机器人！<br>在玩中认识神奇的传动世界</p>
      <span class="btn-start">⚙️ 开始玩</span>
    </div>
  </a>

  <a href="rainforest-adventure.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-orange">
      <div class="icon">🌴</div>
      <h3>雨林大冒险</h3>
      <div class="tags">
        <span class="tag tag-orange">🌴 自然</span>
        <span class="tag tag-orange">🧒 3-6岁</span>
      </div>
      <p>点一点探索雨林！<br>认识树懒、鹦鹉、蝴蝶等6种雨林生物</p>
      <span class="btn-start">🌴 去探险</span>
    </div>
  </a>

</div>

## 🀄 语文识字 Chinese

<div class="section-divider"></div>

<div class="course-grid">

  <a href="nature-lesson-4.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-red">
      <div class="icon">🌿</div>
      <h3>大自然</h3>
      <div class="tags">
        <span class="tag tag-red">🀄 识字</span>
        <span class="tag tag-orange">🧒 4-8岁</span>
      </div>
      <p>和Steve & Alex一起认识大自然<br>云雨风雪星花草虫鸟，9个字全掌握</p>
      <span class="btn-start">🀄 学汉字</span>
    </div>
  </a>

</div>

---

> 🎪 **一起玩吧！** — 每堂课都有语音朗读 🔊 和互动游戏 🎮，小朋友可以自己点着玩。
> 新课件持续更新中，记得常回来看看哦！ <span class="sparkle-star">⭐</span><span class="sparkle-star">⭐</span><span class="sparkle-star">⭐</span>
