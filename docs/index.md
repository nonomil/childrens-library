<style>
/* ===== 全局重置 ===== */
*{box-sizing:border-box;margin:0;padding:0}

/* ===== 像素字体 ===== */
@font-face{font-family:'Pixel';src:local('Press Start 2P'),local('Courier New');font-display:swap}
.pixel-font{font-family:'Pixel','Courier New',monospace}

/* ===== 村庄场景容器 ===== */
.village-scene{
  position:relative;
  width:100%;min-height:100vh;
  overflow:hidden;
  background:linear-gradient(180deg,
    #1a0a2e 0%,
    #2d1b69 5%,
    #4a3f8a 10%,
    #6b5bb5 15%,
    #897dd4 20%,
    #a89de8 25%,
    #7ec8e3 35%,
    #67bcd9 42%,
    #f4a460 60%,
    #f5923e 70%,
    #e8751a 80%,
    #cc5500 100%
  );
}

/* ===== 太阳 ===== */
.sun{
  position:absolute;top:8%;right:12%;
  width:60px;height:60px;
  background:radial-gradient(circle,#fff7a0 20%,#ffd700 50%,transparent 70%);
  border-radius:50%;
  box-shadow:0 0 40px 15px rgba(255,215,0,0.3),0 0 80px 30px rgba(255,165,0,0.15);
  animation:sun-pulse 4s ease-in-out infinite;
}
@keyframes sun-pulse{0%,100%{transform:scale(1);opacity:0.95}50%{transform:scale(1.05);opacity:1}}

/* ===== 星星 ===== */
.stars{position:absolute;top:0;left:0;width:100%;height:30%}
.star{
  position:absolute;width:3px;height:3px;background:#fff;border-radius:50%;
  animation:twinkle 2s ease-in-out infinite;
}
.star:nth-child(odd){animation-delay:1s}
@keyframes twinkle{0%,100%{opacity:0.3;transform:scale(0.8)}50%{opacity:1;transform:scale(1.2)}}

/* ===== 云 ===== */
.cloud{
  position:absolute;
  background:#fff;
  border-radius:50px;
  opacity:0.85;
  animation:cloud-drift linear infinite;
}
.cloud::before,.cloud::after{
  content:'';position:absolute;background:inherit;border-radius:50%;
}
.cloud-1{width:80px;height:28px;top:15%;left:-120px;animation-duration:45s}
.cloud-1::before{width:40px;height:32px;top:-16px;left:12px}
.cloud-1::after{width:50px;height:28px;top:-10px;left:35px}

.cloud-2{width:100px;height:32px;top:22%;left:-160px;animation-duration:55s;animation-delay:8s}
.cloud-2::before{width:50px;height:36px;top:-18px;left:15px}
.cloud-2::after{width:60px;height:30px;top:-12px;left:40px}

.cloud-3{width:70px;height:24px;top:10%;left:-100px;animation-duration:50s;animation-delay:15s;opacity:0.6}
.cloud-3::before{width:35px;height:28px;top:-14px;left:10px}
.cloud-3::after{width:42px;height:24px;top:-8px;left:30px}

.cloud-4{width:90px;height:26px;top:18%;left:-140px;animation-duration:60s;animation-delay:20s;opacity:0.7}
.cloud-4::before{width:45px;height:30px;top:-15px;left:14px}
.cloud-4::after{width:52px;height:26px;top:-10px;left:38px}

@keyframes cloud-drift{0%{transform:translateX(0)}100%{transform:translateX(calc(100vw + 200px))}}

/* ===== 飞鸟 ===== */
.bird{
  position:absolute;
  width:0;height:0;
  border-top:3px solid transparent;
  border-bottom:3px solid transparent;
  animation:bird-fly linear infinite,bird-flap 0.6s ease-in-out infinite;
}
.bird::before,.bird::after{
  content:'';position:absolute;
  border-top:3px solid #333;
  border-left:6px solid transparent;
}
.bird::before{right:5px;transform-origin:right}
.bird::after{left:5px;transform-origin:left;border-left:none;border-right:6px solid transparent}

.bird-1{top:12%;left:-30px;animation-duration:18s,0.6s}
.bird-2{top:8%;left:-50px;animation-duration:22s,0.5s;animation-delay:5s}
.bird-3{top:16%;left:-40px;animation-duration:20s,0.7s;animation-delay:10s}
.bird-4{top:6%;left:-60px;animation-duration:25s,0.55s;animation-delay:14s}
.bird-5{top:20%;left:-35px;animation-duration:19s,0.65s;animation-delay:20s}

@keyframes bird-fly{0%{transform:translateX(0) translateY(0)}25%{transform:translateX(25vw) translateY(-15px)}50%{transform:translateX(50vw) translateY(5px)}75%{transform:translateX(75vw) translateY(-10px)}100%{transform:translateX(105vw) translateY(0)}}
@keyframes bird-flap{0%,100%{border-top-width:5px;border-bottom-width:1px}50%{border-top-width:1px;border-bottom-width:5px}}

/* ===== 山丘 ===== */
.hills{
  position:absolute;bottom:0;left:0;width:100%;height:40%;
  pointer-events:none;
}
.hill{
  position:absolute;bottom:0;
  border-radius:50% 50% 0 0;
}
.hill-1{width:400px;height:180px;background:#2d8a4e;bottom:22%;left:-30px}
.hill-2{width:500px;height:220px;background:#248b3e;bottom:18%;left:15%}
.hill-3{width:350px;height:160px;background:#33994d;bottom:20%;left:55%}
.hill-4{width:450px;height:200px;background:#2a7d42;bottom:16%;right:-40px}
.hill-5{width:300px;height:140px;background:#2e9250;bottom:24%;left:35%}

/* ===== 草地 ===== */
.ground{
  position:absolute;bottom:0;left:0;width:100%;height:28%;
  background:
    repeating-linear-gradient(90deg,#3a9e5c 0px,#3a9e5c 8px,#359050 8px,#359050 16px),
    linear-gradient(180deg,#43b064 0%,#3a8e54 40%,#5a4a35 40%,#4a3a28 100%);
  background-size:16px 100%,100% 100%;
}
.ground::before{
  content:'';position:absolute;top:-8px;left:0;width:100%;height:16px;
  background:repeating-linear-gradient(90deg,
    #43b064 0px,#43b064 6px,
    #3aa058 6px,#3aa058 12px
  );
  border-radius:0 0 4px 4px;
}

/* ===== 像素草地装饰 ===== */
.grass-deco{
  position:absolute;bottom:28%;left:0;width:100%;height:20px;pointer-events:none;
}
.grass-blade{
  position:absolute;bottom:0;width:4px;background:#5cb870;border-radius:2px 2px 0 0;
  transform-origin:bottom;
}
.grass-blade:nth-child(odd){animation:grass-sway 3s ease-in-out infinite}
.grass-blade:nth-child(even){animation:grass-sway 3.5s ease-in-out infinite reverse}
@keyframes grass-sway{0%,100%{transform:rotate(-3deg)}50%{transform:rotate(3deg)}}

/* ===== 像素小人 ===== */
.pixel-boy{
  position:absolute;
  bottom:30%;left:50%;transform:translateX(-50%);
  width:48px;height:64px;
  image-rendering:pixelated;
  z-index:10;
  animation:boy-idle 1.5s ease-in-out infinite;
}
.pixel-boy .head{
  position:absolute;top:0;left:8px;
  width:32px;height:24px;
  background:#f5c6a0;
  border:3px solid #d4956a;
  border-radius:4px;
}
.pixel-boy .eye-l,.pixel-boy .eye-r{
  position:absolute;top:10px;width:6px;height:6px;background:#2d1b00;border-radius:1px;
}
.pixel-boy .eye-l{left:10px}
.pixel-boy .eye-r{right:10px}
.pixel-boy .mouth{
  position:absolute;bottom:6px;left:50%;transform:translateX(-50%);
  width:8px;height:4px;border-bottom:3px solid #c47a5a;border-radius:0 0 4px 4px;
}
.pixel-boy .hair{
  position:absolute;top:-6px;left:4px;
  width:40px;height:14px;
  background:#5a3a1a;
  border-radius:8px 8px 2px 2px;
}
.pixel-boy .body{
  position:absolute;top:24px;left:8px;
  width:32px;height:20px;
  background:#42a5f5;
  border:3px solid #1e88e5;
  border-radius:3px;
}
.pixel-boy .arm-l,.pixel-boy .arm-r{
  position:absolute;top:26px;width:8px;height:18px;
  background:#42a5f5;border:2px solid #1e88e5;border-radius:3px;
}
.pixel-boy .arm-l{left:0}
.pixel-boy .arm-r{right:0}
.pixel-boy .leg-l,.pixel-boy .leg-r{
  position:absolute;top:44px;width:12px;height:20px;
  background:#5d4037;border:2px solid #3e2723;border-radius:2px;
}
.pixel-boy .leg-l{left:8px}
.pixel-boy .leg-r{right:8px}
.pixel-boy .shoe-l,.pixel-boy .shoe-r{
  position:absolute;top:60px;width:14px;height:6px;
  background:#3e2723;border-radius:2px;
}
.pixel-boy .shoe-l{left:6px}
.pixel-boy .shoe-r{right:6px}
@keyframes boy-idle{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(-4px)}}

/* ===== 泥土小路 SVG ===== */
.dirt-path{
  position:absolute;bottom:0;left:0;width:100%;height:100%;
  pointer-events:none;z-index:1;
}

/* ===== 建筑 ===== */
.village-buildings{
  position:absolute;bottom:16%;left:0;width:100%;height:42%;
  display:flex;justify-content:space-around;align-items:flex-end;
  padding:0 3%;z-index:5;
}
.building{
  display:flex;flex-direction:column;align-items:center;
  text-decoration:none;color:inherit;
  cursor:pointer;
  transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
  position:relative;
  padding-bottom:8px;
}
.building:hover{
  transform:translateY(-12px) scale(1.08);
}
.building:hover .building-bounce{animation:bounce 0.5s ease}
@keyframes bounce{0%,100%{transform:translateY(0)}30%{transform:translateY(-8px)}60%{transform:translateY(-3px)}}

.building-bounce{
  display:flex;flex-direction:column;align-items:center;
}

.building-label{
  font-family:'Pixel','Courier New',monospace;
  font-size:11px;font-weight:700;
  background:rgba(0,0,0,0.6);color:#fff;
  padding:3px 8px;border-radius:4px;
  margin-top:6px;white-space:nowrap;
  border:2px solid rgba(255,255,255,0.2);
  letter-spacing:0.5px;
}
.building-count{
  font-size:9px;color:#aaa;margin-top:2px;
  font-family:'Pixel','Courier New',monospace;
}

/* -- 音乐喷泉 -- */
.fountain{width:90px;height:80px}
.fountain-base{
  width:80px;height:30px;background:#7a7a7a;
  border:3px solid #555;border-radius:0 0 10px 10px;
  position:relative;margin:0 auto;
}
.fountain-base::before{
  content:'';position:absolute;top:-5px;left:50%;transform:translateX(-50%);
  width:12px;height:12px;background:#87ceeb;border-radius:50%;
  box-shadow:0 0 6px 2px rgba(135,206,235,0.5);
  animation:fountain-glow 2s ease-in-out infinite;
}
.fountain-pillar{
  width:10px;height:35px;background:#888;
  margin:0 auto;border-radius:3px;
  position:relative;
}
.fountain-pillar::before{
  content:'';position:absolute;top:-8px;left:50%;transform:translateX(-50%);
  width:24px;height:14px;background:#6ab7d4;
  border-radius:50%;border:2px solid #5599aa;
  animation:fountain-water 1.5s ease-in-out infinite;
}
.fountain-pillar::after{
  content:'🎵';position:absolute;top:-20px;left:50%;transform:translateX(-50%);
  font-size:18px;animation:note-float 2s ease-in-out infinite;
}
@keyframes fountain-glow{0%,100%{box-shadow:0 0 6px 2px rgba(135,206,235,0.5)}50%{box-shadow:0 0 12px 4px rgba(135,206,235,0.8)}}
@keyframes fountain-water{0%,100%{transform:translateX(-50%) scaleY(1)}50%{transform:translateX(-50%) scaleY(1.2)}}
@keyframes note-float{0%{transform:translateX(-50%) translateY(0);opacity:1}100%{transform:translateX(-50%) translateY(-20px);opacity:0}}

/* -- 铁匠铺 -- */
.blacksmith{width:80px;height:80px}
.smith-roof{
  width:0;height:0;
  border-left:45px solid transparent;
  border-right:45px solid transparent;
  border-bottom:25px solid #8b4513;
  position:relative;
}
.smith-roof::before{
  content:'';position:absolute;top:10px;left:-30px;
  width:60px;height:18px;
  background:repeating-linear-gradient(90deg,#8b4513 0px,#8b4513 10px,#7a3b10 10px,#7a3b10 20px);
}
.smith-wall{
  width:70px;height:40px;background:#d2b48c;
  border:3px solid #8b6914;margin:0 auto;
  position:relative;
}
.smith-door{
  width:16px;height:24px;background:#5a3a1a;
  border:2px solid #3e2723;
  border-radius:8px 8px 0 0;
  position:absolute;bottom:0;left:50%;transform:translateX(-50%);
}
.smith-chimney{
  position:absolute;top:-20px;right:5px;
  width:14px;height:20px;background:#666;
  border:2px solid #444;
}
.smith-chimney::after{
  content:'';position:absolute;top:-12px;left:2px;
  width:10px;height:12px;
  background:radial-gradient(circle,rgba(100,100,100,0.6),transparent);
  border-radius:50%;
  animation:smoke 2s ease-in-out infinite;
}
@keyframes smoke{0%{transform:translateY(0) scale(1);opacity:0.6}100%{transform:translateY(-15px) scale(2);opacity:0}}

/* -- 图书馆 -- */
.library{width:80px;height:85px}
.lib-roof{
  width:80px;height:18px;background:#1565c0;
  border:3px solid #0d47a1;
  border-radius:4px 4px 0 0;
  position:relative;
}
.lib-roof::before{
  content:'📚';position:absolute;top:-16px;left:50%;transform:translateX(-50%);
  font-size:16px;
}
.lib-wall{
  width:70px;height:45px;background:#bbdefb;
  border:3px solid #90caf9;margin:0 auto;
  position:relative;
}
.lib-window{
  position:absolute;top:8px;width:16px;height:18px;
  background:#e3f2fd;border:2px solid #64b5f6;
  border-radius:2px;
}
.lib-window::before{
  content:'';position:absolute;top:50%;left:0;width:100%;height:2px;background:#64b5f6;
}
.lib-window::after{
  content:'';position:absolute;left:50%;top:0;width:2px;height:100%;background:#64b5f6;
}
.lib-window-l{left:8px}
.lib-window-r{right:8px}
.lib-door{
  width:14px;height:22px;background:#1565c0;
  border:2px solid #0d47a1;
  border-radius:6px 6px 0 0;
  position:absolute;bottom:0;left:50%;transform:translateX(-50%);
}

/* -- 面包房 -- */
.bakery{width:85px;height:80px}
.bakery-roof{
  width:90px;height:22px;
  background:repeating-linear-gradient(90deg,#ff6b6b 0px,#ff6b6b 15px,#fff 15px,#fff 30px);
  border:3px solid #e74c3c;
  border-radius:6px 6px 0 0;
  position:relative;
  margin-left:-2px;
}
.bakery-roof::before{
  content:'🍞';position:absolute;top:-14px;left:50%;transform:translateX(-50%);
  font-size:18px;
}
.bakery-wall{
  width:76px;height:42px;background:#fff3e0;
  border:3px solid #ffcc80;margin:0 auto;
  position:relative;
}
.bakery-window{
  position:absolute;top:8px;left:50%;transform:translateX(-50%);
  width:28px;height:16px;background:#ffe0b2;
  border:2px solid #ffb74d;border-radius:3px;
  display:flex;align-items:center;justify-content:center;font-size:12px;
}
.bakery-door{
  width:14px;height:20px;background:#8d6e63;
  border:2px solid #5d4037;
  border-radius:6px 6px 0 0;
  position:absolute;bottom:0;right:8px;
}

/* -- 神社 -- */
.shrine{width:75px;height:85px}
.shrine-torii{
  width:70px;height:8px;background:#c62828;
  position:relative;margin:0 auto;
  border-radius:3px;
}
.shrine-torii::before{
  content:'';position:absolute;top:-5px;left:-8px;
  width:86px;height:6px;background:#b71c1c;border-radius:3px;
}
.shrine-torii::after{
  content:'';position:absolute;top:8px;left:5px;
  width:6px;height:16px;background:#c62828;
  box-shadow:54px 0 0 0 #c62828;
}
.shrine-body{
  width:50px;height:40px;background:#d7ccc8;
  border:3px solid #8d6e63;margin:20px auto 0;
  position:relative;border-radius:2px 2px 0 0;
}
.shrine-door{
  width:18px;height:28px;background:#fff8e1;
  border:2px solid #bcaaa4;
  position:absolute;bottom:0;left:50%;transform:translateX(-50%);
  border-radius:10px 10px 0 0;
}
.shrine-lantern{
  position:absolute;top:-10px;right:-10px;
  width:10px;height:14px;background:#ff9800;
  border:2px solid #e65100;border-radius:3px;
  animation:lantern-glow 2s ease-in-out infinite;
}
@keyframes lantern-glow{0%,100%{box-shadow:0 0 4px #ff9800}50%{box-shadow:0 0 10px #ff9800}}

/* ===== 小男孩下方对话气泡 ===== */
.dialog-bubble{
  position:absolute;bottom:calc(30% + 72px);left:50%;transform:translateX(-50%);
  background:#fff;border:3px solid #333;border-radius:12px;
  padding:8px 14px;font-family:'Pixel','Courier New',monospace;
  font-size:11px;color:#333;white-space:nowrap;z-index:15;
  box-shadow:3px 3px 0 #333;
}
.dialog-bubble::after{
  content:'';position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);
  border-left:8px solid transparent;border-right:8px solid transparent;
  border-top:10px solid #fff;
  filter:drop-shadow(0 2px 0 #333);
}

/* ===== 下方内容区 ===== */
.content-area{
  background:linear-gradient(180deg,#4a3a28 0%,#3a2a1a 100%);
  padding:16px 0 24px;
  position:relative;
}
.content-area::before{
  content:'';position:absolute;top:0;left:0;width:100%;height:4px;
  background:repeating-linear-gradient(90deg,#5a4a38 0px,#5a4a38 8px,#4a3a28 8px,#4a3a28 16px);
}

/* ===== 统计条 ===== */
.stats-bar{
  display:flex;justify-content:center;gap:6px;flex-wrap:wrap;
  padding:10px 12px;margin:0 auto 12px;max-width:700px;
}
.stat-pill{
  background:#2a2a2a;border:2px solid #555;
  padding:4px 12px;border-radius:4px;
  font-family:'Pixel','Courier New',monospace;
  font-size:10px;color:#aaa;
  display:flex;align-items:center;gap:4px;
}
.stat-pill strong{color:#4caf50;font-size:11px}

/* ===== 横向滚动行 ===== */
.section{margin:16px 0}
.section-header{
  display:flex;align-items:center;gap:8px;
  margin-bottom:6px;padding:0 12px;
}
.section-header .sh-icon{font-size:20px}
.section-header .sh-name{
  font-family:'Pixel','Courier New',monospace;
  font-size:14px;font-weight:700;color:#c8b88a;
  text-shadow:2px 2px 0 #333;
}
.section-header .sh-count{
  font-size:11px;color:#888;
  font-family:'Pixel','Courier New',monospace;
}
.section-header .sh-arrow{
  font-size:11px;color:#4caf50;font-weight:700;
  margin-left:auto;text-decoration:none;
  font-family:'Pixel','Courier New',monospace;
}
.section-header .sh-arrow:hover{text-decoration:underline;color:#66bb6a}

.scroll-row{
  display:flex;gap:10px;overflow-x:auto;overflow-y:hidden;
  padding:8px 12px 12px;scroll-behavior:smooth;
  -webkit-overflow-scrolling:touch;
  scrollbar-width:thin;scrollbar-color:#4a3a28 transparent;
}
.scroll-row::-webkit-scrollbar{height:6px}
.scroll-row::-webkit-scrollbar-thumb{background:#5a4a38;border-radius:0}
.scroll-row::-webkit-scrollbar-track{background:transparent}

/* ===== 像素卡片 ===== */
.scroll-card{
  flex:0 0 130px;
  background:#1a1a1a;
  border:3px solid #555;
  padding:12px 8px;text-align:center;
  text-decoration:none;color:inherit;
  display:flex;flex-direction:column;align-items:center;
  position:relative;touch-action:manipulation;
  transition:all .2s cubic-bezier(0.34,1.56,0.64,1);
  image-rendering:pixelated;
}
.scroll-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:var(--accent,#4caf50);
}
.scroll-card:hover{
  transform:translateY(-4px) scale(1.04);
  border-color:var(--accent,#4caf50);
  box-shadow:0 0 12px rgba(76,175,80,0.3);
}
.scroll-card:active{transform:scale(0.95)}
.scroll-card .sc-icon{font-size:28px;line-height:1.2;margin-bottom:4px}
.scroll-card .sc-name{
  font-family:'Pixel','Courier New',monospace;
  font-size:10px;font-weight:600;
  color:#ccc;line-height:1.3;word-break:break-word;
}
.scroll-card.card-new::after{
  content:'NEW';position:absolute;top:-1px;right:-1px;
  background:#4caf50;color:#fff;
  font-family:'Pixel','Courier New',monospace;
  font-size:7px;padding:1px 4px;
}

/* 像素卡片颜色 */
.scroll-card.card-blue{--accent:#42a5f5;border-color:#42a5f5}
.scroll-card.card-red{--accent:#ef5350;border-color:#ef5350}
.scroll-card.card-green{--accent:#66bb6a;border-color:#66bb6a}
.scroll-card.card-orange{--accent:#ffb347;border-color:#ffb347}
.scroll-card.card-purple{--accent:#a78bfa;border-color:#a78bfa}
.scroll-card.card-yellow{--accent:#ffd93d;border-color:#ffd93d}
.scroll-card.card-pink{--accent:#ff9ff3;border-color:#ff9ff3}
.scroll-card.card-brown{--accent:#8d6e63;border-color:#8d6e63}

/* ===== 底部按钮 ===== */
.bottom-btn{
  display:flex;justify-content:center;margin:20px 0 8px;
}
.bottom-btn a{
  display:inline-flex;align-items:center;gap:6px;
  padding:10px 24px;
  background:#4caf50;border:3px solid #388e3c;
  color:#fff;font-family:'Pixel','Courier New',monospace;
  font-size:12px;font-weight:700;text-decoration:none;
  transition:all 0.2s;box-shadow:4px 4px 0 #2e7d32;
}
.bottom-btn a:hover{
  background:#66bb6a;transform:translate(-2px,-2px);
  box-shadow:6px 6px 0 #2e7d32;
}
.bottom-btn a:active{transform:translate(2px,2px);box-shadow:2px 2px 0 #2e7d32}

/* ===== 移动端适配 ===== */
@media(max-width:600px){
  .village-scene{min-height:80vh}
  .sun{width:40px;height:40px;top:6%;right:8%}
  .village-buildings{
    flex-wrap:wrap;gap:8px;
    justify-content:center;
    bottom:22%;height:auto;
    padding:0 8px;
  }
  .building{flex:0 0 30%}
  .building-label{font-size:9px;padding:2px 5px}
  .building-count{font-size:8px}
  .pixel-boy{width:36px;height:48px;bottom:34%}
  .pixel-boy .head{width:24px;height:18px;left:6px}
  .pixel-boy .body{width:24px;height:16px;left:6px;top:18px}
  .pixel-boy .hair{width:30px;height:10px;left:3px;top:-4px}
  .pixel-boy .eye-l,.pixel-boy .eye-r{top:7px;width:4px;height:4px}
  .pixel-boy .mouth{bottom:4px}
  .pixel-boy .arm-l,.pixel-boy .arm-r{top:20px;width:6px;height:14px}
  .pixel-boy .leg-l,.pixel-boy .leg-r{top:34px;width:9px;height:16px}
  .pixel-boy .shoe-l,.pixel-boy .shoe-r{top:48px;width:11px;height:5px}
  .dialog-bubble{font-size:9px;padding:5px 10px;bottom:calc(34% + 56px)}
  .fountain{width:60px;height:55px}
  .fountain-pillar{height:25px}
  .fountain-base{width:55px;height:22px}
  .blacksmith{width:55px;height:58px}
  .smith-roof{border-left-width:32px;border-right-width:32px;border-bottom-width:18px}
  .smith-roof::before{width:44px;height:14px;left:-22px}
  .smith-wall{width:50px;height:30px}
  .library{width:55px;height:60px}
  .lib-roof{width:55px;height:14px}
  .lib-wall{width:48px;height:32px}
  .bakery{width:60px;height:58px}
  .bakery-roof{width:65px;height:16px}
  .bakery-wall{width:54px;height:30px}
  .shrine{width:52px;height:62px}
  .shrine-torii{width:50px;height:6px}
  .shrine-torii::before{width:62px;height:5px}
  .shrine-body{width:36px;height:30px;margin-top:14px}

  .section-header .sh-name{font-size:12px}
  .scroll-card{flex:0 0 110px;padding:10px 6px}
  .scroll-card .sc-icon{font-size:24px}
  .scroll-card .sc-name{font-size:9px}
  .stats-bar{gap:4px}
  .stat-pill{font-size:9px;padding:3px 8px}
}

@media(max-width:380px){
  .building{flex:0 0 45%}
  .village-buildings{gap:4px}
}

/* ===== 显示全部课件入口 ===== */
.show-all{
  position:absolute;top:10px;right:10px;z-index:20;
}
.show-all a{
  font-family:'Pixel','Courier New',monospace;
  font-size:9px;color:#4caf50;text-decoration:none;
  border:2px solid #4caf50;padding:3px 8px;
  background:rgba(0,0,0,0.5);
}
.show-all a:hover{background:#4caf50;color:#fff}

/* ===== 粒子效果（草籽） ===== */
.particle{
  position:absolute;width:3px;height:3px;
  background:rgba(255,255,255,0.6);border-radius:50%;
  animation:float-up 4s linear infinite;
  pointer-events:none;
}
@keyframes float-up{
  0%{transform:translateY(0) translateX(0);opacity:0.8}
  50%{opacity:0.4}
  100%{transform:translateY(-60px) translateX(20px);opacity:0}
}

/* ===== 矿石装饰 ===== */
.ore{
  position:absolute;width:8px;height:8px;
  border:2px solid #888;border-radius:2px;
  background:#666;
  image-rendering:pixelated;
}
.ore-diamond{background:#4dd0e1;border-color:#00acc1;box-shadow:0 0 4px #4dd0e1}
.ore-gold{background:#ffd54f;border-color:#ffb300;box-shadow:0 0 4px #ffd54f}
</style>

<!-- ===== 村庄场景 ===== -->
<div class="village-scene">
  <!-- 太阳 -->
  <div class="sun"></div>

  <!-- 星星 -->
  <div class="stars">
    <div class="star" style="top:5%;left:10%"></div>
    <div class="star" style="top:8%;left:25%"></div>
    <div class="star" style="top:3%;left:40%"></div>
    <div class="star" style="top:12%;left:55%"></div>
    <div class="star" style="top:6%;left:70%"></div>
    <div class="star" style="top:15%;left:85%"></div>
    <div class="star" style="top:10%;left:5%"></div>
    <div class="star" style="top:2%;left:60%"></div>
  </div>

  <!-- 云 -->
  <div class="cloud cloud-1"></div>
  <div class="cloud cloud-2"></div>
  <div class="cloud cloud-3"></div>
  <div class="cloud cloud-4"></div>

  <!-- 飞鸟 -->
  <div class="bird bird-1"></div>
  <div class="bird bird-2"></div>
  <div class="bird bird-3"></div>
  <div class="bird bird-4"></div>
  <div class="bird bird-5"></div>

  <!-- 山丘 -->
  <div class="hills">
    <div class="hill hill-1"></div>
    <div class="hill hill-2"></div>
    <div class="hill hill-3"></div>
    <div class="hill hill-4"></div>
    <div class="hill hill-5"></div>
  </div>

  <!-- 矿石装饰 -->
  <div class="ore ore-diamond" style="bottom:30%;left:8%"></div>
  <div class="ore ore-gold" style="bottom:32%;right:12%"></div>

  <!-- 蜿蜒泥土小路 SVG -->
  <svg class="dirt-path" viewBox="0 0 1000 600" preserveAspectRatio="none">
    <defs>
      <pattern id="dirt" patternUnits="userSpaceOnUse" width="8" height="8">
        <rect width="8" height="8" fill="#8B7355"/>
        <rect x="0" y="0" width="4" height="4" fill="#7A6548" opacity="0.5"/>
        <rect x="4" y="4" width="4" height="4" fill="#9C8565" opacity="0.5"/>
      </pattern>
    </defs>
    <path d="M 100,580 C 150,520 200,500 280,480 S 380,440 440,420 S 500,380 500,350 C 500,320 480,300 420,280 S 340,250 280,240 S 200,220 150,210"
          stroke="url(#dirt)" stroke-width="28" fill="none" stroke-linecap="round" opacity="0.8"/>
    <path d="M 500,350 C 520,320 560,280 620,260 S 720,230 800,240 S 900,260 950,280"
          stroke="url(#dirt)" stroke-width="28" fill="none" stroke-linecap="round" opacity="0.8"/>
    <path d="M 500,350 C 510,380 530,420 560,440 S 640,480 720,490 S 850,500 950,480"
          stroke="url(#dirt)" stroke-width="28" fill="none" stroke-linecap="round" opacity="0.8"/>
    <!-- 小路边缘阴影 -->
    <path d="M 100,582 C 150,522 200,502 280,482 S 380,442 440,422 S 500,382 500,352 C 500,322 480,302 420,282 S 340,252 280,242 S 200,222 150,212"
          stroke="rgba(0,0,0,0.15)" stroke-width="32" fill="none" stroke-linecap="round"/>
    <path d="M 500,352 C 520,322 560,282 620,262 S 720,232 800,242 S 900,262 950,282"
          stroke="rgba(0,0,0,0.15)" stroke-width="32" fill="none" stroke-linecap="round"/>
    <path d="M 500,352 C 510,382 530,422 560,442 S 640,482 720,492 S 850,502 950,482"
          stroke="rgba(0,0,0,0.15)" stroke-width="32" fill="none" stroke-linecap="round"/>
  </svg>

  <!-- 对话气泡 -->
  <div class="dialog-bubble">欢迎来到学习村庄!</div>

  <!-- 像素小人 -->
  <div class="pixel-boy">
    <div class="hair"></div>
    <div class="head">
      <div class="eye-l"></div>
      <div class="eye-r"></div>
      <div class="mouth"></div>
    </div>
    <div class="body"></div>
    <div class="arm-l"></div>
    <div class="arm-r"></div>
    <div class="leg-l"></div>
    <div class="leg-r"></div>
    <div class="shoe-l"></div>
    <div class="shoe-r"></div>
  </div>

  <!-- 五个建筑 -->
  <div class="village-buildings">
    <!-- 音乐喷泉 - 童谣 -->
    <a href="#section-nursery" class="building">
      <div class="building-bounce">
        <div class="fountain">
          <div class="fountain-pillar"></div>
          <div class="fountain-base"></div>
        </div>
      </div>
      <span class="building-label">🎵 音乐喷泉</span>
      <span class="building-count">童谣 27首</span>
    </a>

    <!-- 铁匠铺 - 数学 -->
    <a href="#section-math" class="building">
      <div class="building-bounce">
        <div class="blacksmith">
          <div class="smith-roof"></div>
          <div class="smith-wall">
            <div class="smith-chimney"></div>
            <div class="smith-door"></div>
          </div>
        </div>
      </div>
      <span class="building-label">🔨 铁匠铺</span>
      <span class="building-count">数学 24课</span>
    </a>

    <!-- 图书馆 - 英语 -->
    <a href="#section-english" class="building">
      <div class="building-bounce">
        <div class="library">
          <div class="lib-roof"></div>
          <div class="lib-wall">
            <div class="lib-window lib-window-l"></div>
            <div class="lib-window lib-window-r"></div>
            <div class="lib-door"></div>
          </div>
        </div>
      </div>
      <span class="building-label">📚 图书馆</span>
      <span class="building-count">英语 24课</span>
    </a>

    <!-- 面包房 - 故事 -->
    <a href="#section-stories" class="building">
      <div class="building-bounce">
        <div class="bakery">
          <div class="bakery-roof"></div>
          <div class="bakery-wall">
            <div class="bakery-window">🍞</div>
            <div class="bakery-door"></div>
          </div>
        </div>
      </div>
      <span class="building-label">🍞 面包房</span>
      <span class="building-count">故事 18个</span>
    </a>

    <!-- 神社 - 古诗 -->
    <a href="#section-poems" class="building">
      <div class="building-bounce">
        <div class="shrine">
          <div class="shrine-torii"></div>
          <div class="shrine-body">
            <div class="shrine-door"></div>
            <div class="shrine-lantern"></div>
          </div>
        </div>
      </div>
      <span class="building-label">⛩️ 神社</span>
      <span class="building-count">古诗 20个</span>
    </a>
  </div>

  <!-- 全部课件入口 -->
  <div class="show-all">
    <a href="courseware/">全部课件 →</a>
  </div>
</div>

<!-- ===== 下方内容区 ===== -->
<div class="content-area">

  <!-- 统计条 -->
  <div class="stats-bar">
    <span class="stat-pill">📚 共 <strong>123</strong> 堂课</span>
    <span class="stat-pill">🎵 <strong>27</strong> 首童谣</span>
    <span class="stat-pill">🔤 <strong>24</strong> 个英语课</span>
    <span class="stat-pill">🀄 <strong>24</strong> 个语文课</span>
    <span class="stat-pill">🧮 <strong>24</strong> 个数学课</span>
    <span class="stat-pill">📖 <strong>8</strong> 本绘本</span>
    <span class="stat-pill">📚 <strong>10</strong> 个中文故事</span>
    <span class="stat-pill">📖 <strong>10</strong> 个英文故事</span>
    <span class="stat-pill">🎓 <strong>10</strong> 个教案</span>
    <span class="stat-pill">🏯 <strong>20</strong> 个古诗</span>
  </div>

  <!-- ===== 🎵 童谣 ===== -->
  <div class="section" id="section-nursery">
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

  <!-- ===== 🧮 数学-Minecraft ===== -->
  <div class="section" id="section-math">
  <div class="section-header">
    <span class="sh-icon">🧮</span>
    <span class="sh-name">数学 Minecraft</span>
    <span class="sh-count">24 课</span>
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
    <span class="sh-count">24 课</span>
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
  <div class="section" id="section-english">
  <div class="section-header">
    <span class="sh-icon">🇬🇧</span>
    <span class="sh-name">英语 Minecraft</span>
    <span class="sh-count">24 课</span>
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

  <!-- ===== 📖 英语绘本 ===== -->
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

  <!-- ===== 📚 绘本阅读 ===== -->
  <div class="section">
  <div class="section-header">
    <span class="sh-icon">📚</span>
    <span class="sh-name">绘本阅读</span>
    <span class="sh-count">8 本</span>
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

  <!-- ===== 📚 中文绘本故事 ===== -->
  <div class="section" id="section-stories">
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

  <!-- ===== 📖 英文故事 ===== -->
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

  <!-- ===== 🎓 教案活动 ===== -->
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

  <!-- ===== 🏯 古诗讲解 ===== -->
  <div class="section" id="section-poems">
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

  <!-- 底部按钮 -->
  <div class="bottom-btn">
    <a href="courseware/">📚 查看全部课件 →</a>
  </div>
</div>
