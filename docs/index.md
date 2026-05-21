# 🎪 小朋友的互动学习乐园

<style>
  .course-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin: 24px 0;
  }
  .course-card {
    background: #FFFCF5;
    border-radius: 24px;
    padding: 24px 20px 20px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 3px solid transparent;
    cursor: pointer;
  }
  .course-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.12);
  }
  .course-card .icon {
    font-size: 64px;
    line-height: 1.2;
    margin-bottom: 8px;
  }
  .course-card h3 {
    font-size: 20px;
    margin: 4px 0 6px;
    color: #333;
  }
  .course-card .tag {
    display: inline-block;
    padding: 2px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
  }
  .course-card p {
    font-size: 14px;
    color: #888;
    margin: 8px 0 12px;
    line-height: 1.5;
  }
  .course-card .btn-start {
    display: inline-block;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 16px;
    font-weight: 700;
    color: white;
    text-decoration: none;
    transition: transform 0.15s;
  }
  .course-card .btn-start:hover { transform: scale(1.05); }
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

  @media (max-width: 600px) {
    .course-grid { grid-template-columns: 1fr; }
    .course-card .icon { font-size: 48px; }
    .course-card h3 { font-size: 18px; }
  }
</style>

<div class="course-grid">
  <a href="courseware/gears-transmission.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-red">
      <div class="icon">⚙️</div>
      <h3>齿轮传动小世界</h3>
      <span class="tag" style="background:#FFE0E0;color:#D94F4F">🔧 机械</span>
      <span class="tag" style="background:#FFF0E0;color:#E07C00">🧒 3-6岁</span>
      <p>点齿轮、转链条、修机器人！<br>在玩中认识神奇的传动世界</p>
      <span class="btn-start">▶ 开始玩</span>
    </div>
  </a>

  <a href="courseware/phonics-fat-cat.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-green">
      <div class="icon">🐱</div>
      <h3>Fat Cat on a Mat</h3>
      <span class="tag" style="background:#E0F5F0;color:#2E9E95">🔤 自然拼读</span>
      <span class="tag" style="background:#FFF0E0;color:#E07C00">🧒 3-6岁</span>
      <p>Usborne风格拼读故事<br>每页拼词互动，点一点学发音</p>
      <span class="btn-start">▶ 开始学</span>
    </div>
  </a>

  <a href="courseware/five-little-monkeys.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-orange">
      <div class="icon">🐵</div>
      <h3>Five Little Monkeys</h3>
      <span class="tag" style="background:#FFF0E0;color:#E07C00">🎵 韵律</span>
      <span class="tag" style="background:#E0F5F0;color:#2E9E95">🔢 数数</span>
      <p>经典童谣互动版！<br>点击小猴跳床，一边唱一边数</p>
      <span class="btn-start">▶ 开始唱</span>
    </div>
  </a>

  <a href="courseware/elephant-piggie-surprise.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-purple">
      <div class="icon">🐘🐷</div>
      <h3>I Will Surprise My Friend!</h3>
      <span class="tag" style="background:#EEE0FF;color:#7C5CFC">💬 对话</span>
      <span class="tag" style="background:#FFE0E0;color:#D94F4F">😊 情绪</span>
      <p>Elephant & Piggie 风格故事<br>角色对话 + 情绪选择</p>
      <span class="btn-start">▶ 开始读</span>
    </div>
  </a>

  <a href="courseware/i-am-an-apple.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-green">
      <div class="icon">🍎</div>
      <h3>I Am an Apple</h3>
      <span class="tag" style="background:#E0F5F0;color:#2E9E95">🌱 科学</span>
      <span class="tag" style="background:#FFF0E0;color:#E07C00">🧒 3-6岁</span>
      <p>认识苹果的生命周期！<br>从种子到果实，互动小测验</p>
      <span class="btn-start">▶ 开始学</span>
    </div>
  </a>

  <a href="courseware/sight-word-tales-come-to-the-party.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-blue">
      <div class="icon">🎉</div>
      <h3>Come to the Party!</h3>
      <span class="tag" style="background:#E0E8FF;color:#4C63D4">📖 Sight Words</span>
      <span class="tag" style="background:#FFF0E0;color:#E07C00">🧒 3-6岁</span>
      <p>高频词 "come" "to"<br>互动绘本 + 找词游戏</p>
      <span class="btn-start">▶ 开始读</span>
    </div>
  </a>

  <a href="courseware/sight-word-tales-can-we-get-a-pet.html" style="text-decoration:none;color:inherit">
    <div class="course-card card-pink">
      <div class="icon">🐱</div>
      <h3>Can We Get a Pet?</h3>
      <span class="tag" style="background:#FFE0F0;color:#D96FC4">📖 Sight Words</span>
      <span class="tag" style="background:#FFF0E0;color:#E07C00">🧒 3-6岁</span>
      <p>高频词 "can" "we"<br>互动绘本 + 找词游戏</p>
      <span class="btn-start">▶ 开始读</span>
    </div>
  </a>
</div>

---

> 👆 点击任意卡片开始学习之旅！每堂课都有语音朗读，小朋友可以自己玩哦 📚✨

[→ 查看全部课件，按科目分类浏览](courseware/)
