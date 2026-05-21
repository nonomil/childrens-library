#!/usr/bin/env python3
"""批量生成幼儿英语童谣互动课件，完全对标 Old MacDonald 格式"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "docs/courseware")
AUDIO = os.path.join(OUT, "audio")

TEMPLATE = open(os.path.join(OUT, "old-macdonald.html"), encoding="utf-8").read()

SONGS = [
    {
        "id": "wheels-on-bus",
        "title": "🚌 The Wheels on the Bus",
        "mp3": "wheels.mp3",
        "cover_subtitle": "✏️ 公车的轮子转啊转！",
        "pages": [
            {"sentence": 'The <span class="hl" data-word="wheels">wheels</span> on the <span class="hl" data-word="bus">bus</span> go <span class="hl" data-word="round">round</span> and <span class="hl" data-word="round">round</span>', "desc": "公车的轮子转啊转", "game": "wheels"},
            {"sentence": 'The <span class="hl" data-word="people">people</span> on the bus go <span class="hl" data-word="up">up</span> and <span class="hl" data-word="down">down</span>', "desc": "公车的人们上上下下", "game": "people"},
            {"sentence": 'The <span class="hl" data-word="wipers">wipers</span> on the bus go <span class="hl" data-word="swish">swish</span>, swish, swish', "desc": "公车的雨刷刷刷刷", "game": "wipers"},
            {"sentence": 'The <span class="hl" data-word="horn">horn</span> on the bus goes <span class="hl" data-word="beep">beep</span>, beep, beep', "desc": "公车的喇叭哔哔哔", "game": "horn"},
            {"sentence": 'The <span class="hl" data-word="door">door</span> on the bus goes <span class="hl" data-word="open">open</span> and <span class="hl" data-word="shut">shut</span>', "desc": "公车的门开了关", "game": "door"},
        ],
        "core_words": ["wheels", "bus", "round", "up", "down", "open", "shut"],
        "svg_bg": "#87CEEB,#E0F7FA",
        "svg_element": "bus",
    },
    {
        "id": "row-your-boat",
        "title": "🚣 Row Row Row Your Boat",
        "mp3": "rowyourboat.mp3",
        "cover_subtitle": "✏️ 划呀划呀划小船！",
        "pages": [
            {"sentence": '<span class="hl" data-word="Row">Row</span>, <span class="hl" data-word="row">row</span>, <span class="hl" data-word="row">row</span> your <span class="hl" data-word="boat">boat</span>', "desc": "划呀划呀划你的船", "game": "row"},
            {"sentence": '<span class="hl" data-word="Gently">Gently</span> down the <span class="hl" data-word="stream">stream</span>', "desc": "轻轻顺着溪流而下", "game": "gently"},
            {"sentence": '<span class="hl" data-word="Merrily">Merrily</span>, merrily, merrily, merrily', "desc": "快快乐乐地划呀划", "game": "merrily"},
            {"sentence": '<span class="hl" data-word="Life">Life</span> is but a <span class="hl" data-word="dream">dream</span>', "desc": "人生不过是一场梦", "game": "dream"},
        ],
        "core_words": ["row", "boat", "stream", "merrily", "dream"],
        "svg_bg": "#81D4FA,#B3E5FC",
        "svg_element": "boat",
    },
    {
        "id": "itsy-bitsy-spider",
        "title": "🕷️ Itsy Bitsy Spider",
        "mp3": "itsybitsy.mp3",
        "cover_subtitle": "✏️ 小蜘蛛爬水管！",
        "pages": [
            {"sentence": 'The <span class="hl" data-word="itsy">itsy</span> <span class="hl" data-word="bitsy">bitsy</span> <span class="hl" data-word="spider">spider</span> went up the water <span class="hl" data-word="spout">spout</span>', "desc": "小蜘蛛爬上了水管", "game": "spider"},
            {"sentence": 'Down came the <span class="hl" data-word="rain">rain</span> and washed the spider <span class="hl" data-word="out">out</span>', "desc": "下雨了把蜘蛛冲出来", "game": "rain"},
            {"sentence": 'Out came the <span class="hl" data-word="sun">sun</span> and dried up all the <span class="hl" data-word="rain">rain</span>', "desc": "太阳出来晒干了雨水", "game": "sun"},
            {"sentence": 'And the itsy bitsy spider went up the spout <span class="hl" data-word="again">again</span>', "desc": "小蜘蛛又爬上了水管", "game": "again"},
        ],
        "core_words": ["spider", "rain", "sun", "out", "again"],
        "svg_bg": "#A5D6A7,#C8E6C9",
        "svg_element": "spider",
    },
    {
        "id": "bingo",
        "title": "🐶 BINGO",
        "mp3": "bingo.mp3",
        "cover_subtitle": "✏️ 农夫有一只小狗叫BINGO！",
        "pages": [
            {"sentence": 'There was a <span class="hl" data-word="farmer">farmer</span> had a <span class="hl" data-word="dog">dog</span>', "desc": "农夫有一只小狗", "game": "farmer"},
            {"sentence": 'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o', "desc": "Bingo是它的名字", "game": "bingo"},
            {"sentence": 'B-I-N-G-O, B-I-N-G-O, B-I-N-G-O', "desc": "拼出BINGO的名字", "game": "bingo2"},
            {"sentence": 'And Bingo was his name-o!', "desc": "Bingo就是它的名字！", "game": "bingo3"},
        ],
        "core_words": ["farmer", "dog", "Bingo", "name"],
        "svg_bg": "#FFE0B2,#FFF3E0",
        "svg_element": "dog",
    },
]

def make_scene(song_data, page_idx):
    """Generate appropriate SVG scene based on song"""
    e = song_data["svg_element"]
    bg = song_data["svg_bg"]
    colors = bg.split(",")
    
    svgs = {
        "bus": f'''<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#sky)"/><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{colors[0]}"/><stop offset="100%" stop-color="{colors[1]}"/></linearGradient></defs><rect x="80" y="80" width="280" height="100" rx="20" fill="#FFD54F" stroke="#FF8F00" stroke-width="3"/><rect x="100" y="100" width="120" height="50" rx="8" fill="#81D4FA" stroke="#4FC3F7" stroke-width="2"/><rect x="230" y="100" width="100" height="50" rx="8" fill="#81D4FA" stroke="#4FC3F7" stroke-width="2"/><circle cx="130" cy="190" r="22" fill="#424242"/><circle cx="130" cy="190" r="14" fill="#9E9E9E"/><circle cx="310" cy="190" r="22" fill="#424242"/><circle cx="310" cy="190" r="14" fill="#9E9E9E"/><rect x="250" y="90" width="8" height="40" rx="4" fill="#FF8A65"/><ellipse cx="360" cy="60" rx="30" ry="15" fill="#FFF" opacity="0.3"/><ellipse cx="80" cy="50" rx="25" ry="12" fill="#FFF" opacity="0.2"/><rect x="148" y="108" width="60" height="34" rx="4" fill="#FFF" opacity="0.5"/></svg>''',
        "boat": f'''<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#sky)"/><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{colors[0]}"/><stop offset="100%" stop-color="{colors[1]}"/></linearGradient></defs><rect y="160" width="460" height="60" fill="#4FC3F7" opacity="0.4"/><path d="M100 160 L120 130 L340 130 L360 160 Z" fill="#8D6E63" stroke="#5D4037" stroke-width="3"/><rect x="200" y="90" width="20" height="40" rx="3" fill="#795548"/><polygon points="220,95 300,120 220,140" fill="#FFF" opacity="0.8" stroke="#90CAF9" stroke-width="2"/><ellipse cx="80" cy="50" rx="30" ry="12" fill="#FFF" opacity="0.3"/><ellipse cx="350" cy="60" rx="25" ry="10" fill="#FFF" opacity="0.2"/></svg>''',
        "spider": f'''<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#sky)"/><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{colors[0]}"/><stop offset="100%" stop-color="{colors[1]}"/></linearGradient></defs><rect x="210" y="40" width="40" height="140" rx="20" fill="#8D6E63"/><ellipse cx="230" cy="40" rx="30" ry="15" fill="#FFF9C4"/><circle cx="230" cy="80" r="10" fill="#5D4037"/><circle cx="226" cy="78" r="2" fill="#FFF"/><circle cx="234" cy="78" r="2" fill="#FFF"/><ellipse cx="230" cy="95" rx="8" ry="6" fill="#5D4037"/><path d="M210 85 Q195 75 200 65" stroke="#5D4037" stroke-width="2" fill="none"/><path d="M220 88 Q205 85 205 75" stroke="#5D4037" stroke-width="2" fill="none"/><path d="M250 85 Q265 75 260 65" stroke="#5D4037" stroke-width="2" fill="none"/><path d="M240 88 Q255 85 255 75" stroke="#5D4037" stroke-width="2" fill="none"/><ellipse cx="80" cy="40" rx="50" ry="20" fill="#FFF" opacity="0.3"/></svg>''',
        "dog": f'''<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#sky)"/><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{colors[0]}"/><stop offset="100%" stop-color="{colors[1]}"/></linearGradient></defs><rect y="160" width="460" height="60" fill="#81C784" opacity="0.3"/><ellipse cx="200" cy="80" rx="40" ry="30" fill="#FFCC80"/><ellipse cx="200" cy="95" rx="25" ry="20" fill="#FFE0B2"/><ellipse cx="230" cy="55" rx="28" ry="25" fill="#FFCC80" transform="rotate(15,230,55)"/><circle cx="240" cy="50" r="4" fill="#5D4037"/><circle cx="238" cy="48" r="1.5" fill="#FFF"/><ellipse cx="255" cy="60" rx="10" ry="6" fill="#5D4037"/><circle cx="220" cy="95" r="3" fill="#5D4037"/><ellipse cx="190" cy="80" rx="15" ry="10" fill="#A1887F"/><ellipse cx="260" cy="58" rx="8" ry="4" fill="#FFAB91"/><ellipse cx="80" cy="50" rx="30" ry="12" fill="#FFF" opacity="0.3"/></svg>''',
    }
    return svgs.get(e, svgs["bus"])

def generate(song):
    """Generate one courseware HTML file"""
    song_id = song["id"]
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>{song["title"]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; -webkit-touch-callout:none; -webkit-user-select:none; user-select:none; }}
body {{
  font-family:'Fredoka One','Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
  background:linear-gradient(145deg,#FFF8E7 0%,#FFE8C8 100%);
  min-height:100vh; display:flex; justify-content:center; align-items:center; padding:12px;
}}
.book {{
  width:100%; max-width:840px; min-height:92vh;
  background:#FFFCF5; border-radius:40px;
  box-shadow:0 20px 60px rgba(0,0,0,0.15),0 0 0 4px #FFF,0 0 0 8px #FFB347;
  padding:24px 20px; position:relative;
  font-family:'Fredoka One','Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
}}
.page-area {{ min-height:420px; }}
.page {{ display:none; flex-direction:column; align-items:center; animation:fadeIn .4s ease; width:100%; }}
.page.active {{ display:flex; }}
@keyframes fadeIn {{ from{{opacity:0;transform:translateY(12px)}} to{{opacity:1;transform:translateY(0)}} }}
@keyframes noteFloat {{ 0%{{opacity:0;transform:translateY(20px) scale(0.5)}} 30%{{opacity:1;transform:translateY(-10px) scale(1.2)}} 100%{{opacity:0;transform:translateY(-60px) scale(0.8)}} }}
@keyframes bounce {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-12px)}} }}
@keyframes shake {{ 0%,100%{{transform:translateX(0)}} 20%{{transform:translateX(-6px)}} 40%{{transform:translateX(6px)}} 60%{{transform:translateX(-4px)}} 80%{{transform:translateX(4px)}} }}
@keyframes popIn {{ 0%{{opacity:0;transform:scale(0.3)}} 100%{{opacity:1;transform:scale(1)}} }}
@keyframes confetti-fall {{ 0%{{opacity:1;transform:translateY(0)rotate(0deg)}} 100%{{opacity:0;transform:translateY(500px)rotate(720deg)}} }}
@keyframes float {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-8px)}} }}
.page-title {{ font-size:30px; color:#E8751A; text-align:center; margin-bottom:8px; font-weight:bold; }}
.page-desc {{ font-size:18px; color:#6B4F3A; text-align:center; line-height:1.5; margin-bottom:10px; }}
.scene-wrap {{ width:100%; max-width:460px; height:auto; margin:0 auto 10px; border-radius:20px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.08); }}
.scene-wrap svg {{ display:block; width:100%; height:auto; }}
.lyrics {{ font-size:26px; color:#E8751A; text-align:center; padding:12px 16px; background:#FFF8E7; border-radius:16px; width:100%; margin-bottom:8px; line-height:1.5; font-weight:bold; }}
.lyrics .hl {{ color:#F44336; cursor:pointer; transition:all .2s; display:inline-block; }}
.lyrics .hl:active {{ transform:scale(1.2); }}
.lyrics .hl::after {{ content:'🔊'; font-size:14px; opacity:0.5; margin-left:4px; }}
.word-game {{ width:100%; padding:14px; background:#FFF8E7; border-radius:18px; text-align:center; margin:6px 0; border:2px solid #FFE8C8; }}
.word-game h3 {{ font-size:16px; color:#E8751A; margin-bottom:8px; display:flex; align-items:center; justify-content:center; gap:6px; }}
.word-slots {{ display:flex; gap:6px; justify-content:center; margin-bottom:8px; }}
.word-slot {{ width:48px; height:48px; border-bottom:4px solid #FFB347; display:flex; align-items:center; justify-content:center; font-size:28px; font-weight:bold; color:#E8751A; border-radius:8px 8px 0 0; background:rgba(255,248,231,0.5); transition:all .2s; }}
.word-slot.filled {{ border-bottom-color:#4CAF50; background:rgba(232,245,233,0.5); animation:popIn .2s ease; }}
.word-slot.drag-over {{ border-bottom-color:#66BB6A; border-bottom-width:6px; background:rgba(102,187,106,0.15); transform:scale(1.05); }}
.letter-tiles {{ display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }}
.letter-tile {{ width:48px; height:48px; border-radius:12px; border:3px solid #E0D5C7; background:white; font-size:24px; font-weight:bold; cursor:grab; display:flex; align-items:center; justify-content:center; transition:all .15s; user-select:none; touch-action:none; }}
.letter-tile:hover {{ border-color:#FFB347; background:#FFF8E7; }}
.letter-tile:active {{ cursor:grabbing; }}
.letter-tile.correct {{ border-color:#4CAF50; background:#E8F5E9; animation:popIn .3s ease; }}
.letter-tile.wrong {{ border-color:#F44336; background:#FFEBEE; animation:shake .3s; }}
.letter-tile.used {{ opacity:0.35; pointer-events:none; }}
.letter-tile.dragging {{ opacity:0.5; }}
.speech-bubble {{ position:fixed; bottom:120px; left:50%; transform:translateX(-50%) scale(0.5); border-radius:20px; background:rgba(255,255,255,0.96); border:3px solid #FFB347; padding:14px 22px; font-size:20px; font-weight:600; max-width:80%; text-align:center; z-index:10000; opacity:0; pointer-events:none; box-shadow:0 8px 30px rgba(255,179,71,0.3); transition:opacity .35s,transform .35s cubic-bezier(0.34,1.56,0.64,1); color:#5A3E2B; line-height:1.5; }}
.speech-bubble.show {{ opacity:1; transform:translateX(-50%) scale(1); }}
.speech-bubble::before {{ content:'🔊'; display:block; font-size:22px; margin-bottom:4px; }}
.controls {{ display:flex; align-items:center; justify-content:space-between; margin-top:10px; gap:8px; position:sticky; bottom:0; background:#FFFCF5; padding:8px 0; z-index:100; }}
.nav-btn {{ background:#FFB347; border:none; color:#FFF; font-size:28px; width:60px; height:60px; border-radius:50%; cursor:pointer; box-shadow:0 4px 12px rgba(255,179,71,0.4); transition:all .15s; display:flex; align-items:center; justify-content:center; flex-shrink:0; touch-action:manipulation; }}
.nav-btn:hover {{ transform:scale(1.1); background:#FF9F1C; }}
.nav-btn:disabled {{ opacity:0.3; cursor:default; transform:none; }}
.nav-btn.small {{ width:48px; height:48px; font-size:22px; }}
.read-btn {{ background:#6BCB77; border:none; color:#FFF; font-size:16px; padding:10px 18px; border-radius:30px; cursor:pointer; box-shadow:0 4px 12px rgba(107,203,119,0.4); font-family:inherit; font-weight:bold; display:flex; align-items:center; gap:5px; transition:all .15s; touch-action:manipulation; }}
.read-btn:hover {{ transform:scale(1.06); }}
.read-btn.pink {{ background:#FF8A80; }}
.page-dots {{ display:flex; gap:6px; }}
.page-dots .dot {{ width:10px; height:10px; border-radius:50%; background:#E0D5C7; cursor:pointer; transition:all .2s; }}
.page-dots .dot.active {{ background:#FFB347; transform:scale(1.3); }}
.page-dots .dot.done {{ background:#4CAF50; }}
.page-counter {{ font-size:13px; color:#999; text-align:center; margin-top:6px; }}
.big-start-btn {{ width:120px; height:120px; border-radius:50%; background:linear-gradient(145deg,#FFB347,#FF9F1C); border:6px solid #FFF; color:#FFF; font-size:32px; cursor:pointer; box-shadow:0 8px 30px rgba(255,179,71,0.5); transition:all .15s; margin:10px auto; display:flex; align-items:center; justify-content:center; animation:bounce 2s ease-in-out infinite; }}
.big-start-btn:active {{ transform:scale(0.95); }}
.big-start-btn.smaller {{ width:90px; height:90px; font-size:28px; }}
.cover-svg {{ width:100%; max-width:400px; margin:0 auto; }}
.home-link {{ color:#FFB347; text-decoration:none; font-size:18px; font-weight:bold; margin-top:10px; display:inline-block; }}
.home-link:hover {{ text-decoration:underline; }}
.celebration {{ position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9999; }}
@media (max-width:500px) {{
  .book {{ padding:16px 12px; }}
  .page-title {{ font-size:24px; }}
  .lyrics {{ font-size:20px; padding:10px 12px; }}
  .letter-tile {{ width:40px; height:40px; font-size:20px; }}
  .word-slot {{ width:40px; height:40px; font-size:22px; }}
  .nav-btn {{ width:50px; height:50px; font-size:24px; }}
  .nav-btn.small {{ width:40px; height:40px; font-size:18px; }}
  .read-btn {{ font-size:14px; padding:8px 14px; }}
  .big-start-btn {{ width:90px; height:90px; font-size:26px; }}
  .big-start-btn.smaller {{ width:70px; height:70px; font-size:22px; }}
}}
</style>
</head>
<body>
<div class="book">
  <div class="page-area" id="pageArea"></div>
  <div class="controls" id="controlsBar">
    <button class="nav-btn" id="prevBtn" onclick="prevPage()" disabled>◀</button>
    <button class="nav-btn small" onclick="playSong();showMusicNotes()" style="animation:float 2s ease-in-out infinite">🎵</button>
    <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center">
      <button class="read-btn" onclick="speakPage()">🔊 读</button>
      <button class="read-btn pink" onclick="playSong();showMusicNotes()">🎵 唱</button>
    </div>
    <button class="nav-btn" id="nextBtn" onclick="nextPage()">▶</button>
  </div>
  <div class="page-dots" id="progressDots"></div>
  <div class="page-counter" id="pageCounter"></div>
</div>
<div class="speech-bubble" id="speechBubble"></div>

<script>
// ====== PAGE DATA ======
var pages = [
  {{ cover:true, title:'{song["title"]}', subtitle:'{song["cover_subtitle"]}' }},
'''

    for i, p in enumerate(song["pages"]):
        comma = "," if i < len(song["pages"]) - 1 else ""
        html += f'''  {{ sentence:'{p["sentence"]}', desc:'{p["desc"]}', game:'{p["game"]}', svg:'{i}' }}{comma}
'''

    html += '''];

var currentPage = 0;
var gameDone = new Array(pages.length).fill(false);
var buildingWord = [];
var currentAudio = null;
var songAudio = null;

// ====== SVG SCENES ======
function getSVG(idx) {
  var scenes = [
'''
    for i, p in enumerate(song["pages"]):
        scene = make_scene(song, i)
        comma = "," if i < len(song["pages"]) - 1 else ""
        html += f'    `{scene}`{comma}\n'

    html += '''  ];
  return scenes[idx] || scenes[0];
}
function svgCoverScene() { return `'''
    html += make_scene(song, 0)
    html += '''`; }

// ====== MELODY ENGINE ======
const NOTE = { C4:261.63, D4:293.66, E4:329.63, F4:349.23, G4:392.00, A4:440.00, B4:493.88, C5:523.25 };

// ===== PLAY FULL SONG MP3 =====
function playSong() {
  if(songAudio) { songAudio.pause(); songAudio.currentTime = 0; }
  songAudio = new Audio('audio/''' + song["mp3"] + '''');
  songAudio.volume = 0.8;
  songAudio.play().catch(function(){});
}
function showMusicNotes() {
  var scene = document.querySelector('.scene-wrap');
  if(!scene) return;
  var notes = ['♪','♫','♩','♬'];
  for(var i=0;i<8;i++){
    var n=document.createElement('div');
    n.textContent=notes[i%notes.length];
    n.style.cssText='position:absolute;font-size:'+(14+Math.random()*18)+'px;color:#FFB347;opacity:0;pointer-events:none;z-index:10;left:'+(Math.random()*80+10)+'%;top:'+(Math.random()*50+10)+'%;animation:noteFloat '+(1+Math.random())+'s ease-out forwards;animation-delay:'+(i*0.15)+'s;';
    scene.appendChild(n);
    setTimeout(function(e){e.remove()},3000,n);
  }
}
function speakText(text) {
  if('speechSynthesis' in window){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text.replace(/<[^>]+>/g,''));u.lang='en-US';u.rate=0.75;u.pitch=1.0;window.speechSynthesis.speak(u);}
}
function showBubble(text) {
  var b=document.getElementById('speechBubble');b.textContent=text;b.classList.add('show');
  setTimeout(function(){b.classList.remove('show')},3000);
}
function speakPage() {
  var p=pages[currentPage];
  if(p.cover) { showBubble('''' + song["title"] + '''!'); speakText('''' + song["title"].replace(/[^a-zA-Z\s]/g,'').trim() + '''); return; }
  if(p.final) { showBubble('You did it! Super English Star! 🌟'); speakText('You did it! Super English Star!'); return; }
  var txt=p.sentence.replace(/<[^>]+>/g,'');
  showBubble('🔊 '+txt);
  speakText(txt);
}

// ====== RENDER ======
function renderPage(idx) {
  var area=document.getElementById('pageArea');
  var p=pages[idx];

  if(p.cover) {
    area.innerHTML =
      '<div class="page active">'+
      '<div class="cover-svg">'+svgCoverScene()+'</div>'+
      '<div class="page-title">'+p.title+'</div>'+
      '<div class="page-desc">'+p.subtitle+'</div>'+
      '<div style="display:flex;gap:16px;justify-content:center;align-items:center;margin-top:4px">'+
        '<button class="big-start-btn smaller" onclick="playSong();showMusicNotes()" style="animation:float 2s ease-in-out infinite">🎵</button>'+
        '<button class="big-start-btn" onclick="nextPage()">▶</button>'+
      '</div>'+
      '<div style="font-size:14px;color:#8D6E63;text-align:center;margin-top:6px">点击 ▶ 开始 · 🎵 听歌曲</div>'+
      '</div>';
    updateUI(idx); return;
  }
  if(p.final) {
    var starsHtml = '';
    for(var i=0;i<10;i++) starsHtml += '<div class="final-star-cell'+(i<7?' lit':'')+'">⭐</div>';
    area.innerHTML =
      '<div class="page active" style="text-align:center;padding:20px 10px">'+
      '<div class="completion-title">🌟 超级英语小明星！</div>'+
      '<div class="completion-sub">Great job! You sang the whole song! 🎉</div>'+
      '<div style="font-size:60px;margin:10px 0">🎉🎊⭐</div>'+
      '<div class="star-final-grid">'+starsHtml+'</div>'+
      '<button class="big-start-btn smaller" onclick="goToPage(0)" style="animation:bounce 2s ease-in-out infinite">🏠 再唱一次</button>'+
      '</div>';
    updateUI(idx); launchConfetti(); return;
  }

  var sceneIdx = p.svg !== undefined ? parseInt(p.svg) : idx-1;
  var svgHtml = getSVG(sceneIdx);
  var gameWord = p.game || '';

  var slotsHtml = '';
  for(var s=0;s<gameWord.length;s++) slotsHtml += '<div class="word-slot" id="ws-'+idx+'-'+s+'"></div>';

  var shuffled = gameWord.split('').sort(function(){return Math.random()-0.5}).join('');
  var tilesHtml = '';
  for(var t=0;t<shuffled.length;t++) {
    var letter = shuffled[t];
    tilesHtml += '<div class="letter-tile" draggable="true" onclick="pickLetter('+idx+',\\''+letter+'\\',this)" ondragstart="onDragStart(event,\\''+letter+'\\','+idx+')" ondragend="onDragEnd(event)">'+letter+'</div>';
  }

  area.innerHTML =
    '<div class="page active">'+
    '<div class="scene-wrap" style="position:relative">'+svgHtml+'</div>'+
    '<div class="lyrics">'+p.sentence+'</div>'+
    '<div class="page-desc">'+p.desc+'</div>'+
    '<div class="word-game">'+
      '<h3>✏️ 拼单词 <span class="speak-btn" onclick="event.stopPropagation();speakText(\\''+gameWord+'\\')" style="background:#FFB347;border:none;color:#FFF;font-size:12px;width:24px;height:24px;border-radius:50%;cursor:pointer;display:inline-flex;align-items:center;justify-content:center">🔊</span></h3>'+
      '<div class="word-slots" id="ws-area-'+idx+'">'+slotsHtml+'</div>'+
      '<div class="letter-tiles" id="tiles-'+idx+'">'+tilesHtml+'</div>'+
      '<div style="font-size:13px;color:#8D6E63;margin-top:6px" id="status-'+idx+'">点击或拖拽字母拼出单词</div>'+
    '</div>'+
    '<div style="font-size:12px;color:#AAA;text-align:center">第'+(idx+1)+'页 / 共'+pages.length+'页</div>'+
    '</div>';

  buildingWord = [];
  updateUI(idx);
}

function updateUI(idx) {
  document.getElementById('prevBtn').disabled = idx===0;
  document.getElementById('nextBtn').disabled = idx===pages.length-1;
  var dots = document.getElementById('progressDots');
  dots.innerHTML = '';
  for(var i=0;i<pages.length;i++) {
    var d = document.createElement('span'); d.className = 'dot';
    if(i===idx) d.classList.add('active');
    if(gameDone[i]) d.classList.add('done');
    d.onclick = function(n){return function(){goToPage(n)}}(i);
    dots.appendChild(d);
  }
  document.getElementById('pageCounter').textContent = '第'+(idx+1)+'页 / 共'+pages.length+'页';
}

// ====== WORD GAME ======
var dragData = null;
function onDragStart(e,letter,idx) {
  dragData = {letter:letter, idx:idx};
  e.dataTransfer.effectAllowed = 'move';
  setTimeout(function(){e.target.classList.add('dragging');},0);
}
function onDragEnd(e) { e.target.classList.remove('dragging'); dragData=null; }

function pickLetter(idx,letter,el) {
  if(gameDone[idx]||el.classList.contains('used')) return;
  var p=pages[idx]; var word=p.game;
  var slot = buildingWord.length;
  if(slot>=word.length) return;
  var slots = document.querySelectorAll('#ws-area-'+idx+' .word-slot');
  if(word[slot]===letter) {
    slots[slot].textContent = letter; slots[slot].classList.add('filled');
    buildingWord.push(letter); el.classList.add('used');
    document.getElementById('status-'+idx).textContent = '✅ 对了！继续拼下一个字母';
    speakText(letter);
    if(buildingWord.length===word.length) {
      gameDone[idx]=true;
      document.getElementById('status-'+idx).textContent = '🎉 太棒了！单词拼好了！';
      document.querySelector('#tiles-'+idx).style.display='none';
      updateUI(idx);
      if(idx===pages.length-2) setTimeout(function(){nextPage()},800);
    }
  } else {
    el.classList.add('wrong');
    document.getElementById('status-'+idx).textContent = '💪 再试试这个字母';
    setTimeout(function(){el.classList.remove('wrong');},400);
  }
}

// ====== NAVIGATION ======
function prevPage(){if(currentPage>0)goToPage(currentPage-1);}
function nextPage(){if(currentPage<pages.length-1)goToPage(currentPage+1);}
function goToPage(idx){currentPage=idx;renderPage(idx);}

// ====== CONFETTI ======
function launchConfetti() {
  var c=document.createElement('div');c.className='celebration';
  var colors=['#FF6B6B','#FFB347','#4ECDC4','#A78BFA','#FFD93D','#FF9FF3'];
  for(var i=0;i<60;i++) {
    var p=document.createElement('div');
    p.style.cssText='position:absolute;top:-10px;left:'+Math.random()*100+'%;width:'+(6+Math.random()*6)+'px;height:'+(6+Math.random()*6)+'px;background:'+colors[Math.floor(Math.random()*colors.length)]+';border-radius:'+(Math.random()>.5?'50%':'2px')+';animation:confetti-fall '+(2+Math.random()*2)+'s ease-out forwards;animation-delay:'+(Math.random()*0.5)+'s;';
    c.appendChild(p);
  }
  document.body.appendChild(c);
  setTimeout(function(){c.remove()},5000);
}

// ====== INIT ======
document.addEventListener('click', function(e) {
  var hl = e.target.closest ? e.target.closest('.hl') : null;
  if(hl && hl.getAttribute('data-word')) {
    speakText(hl.getAttribute('data-word'));
    hl.style.transform='scale(1.3)';
    setTimeout(function(){hl.style.transform='scale(1)';},300);
  }
});
goToPage(0);
</script>
</body>
</html>'''
    
    outpath = os.path.join(OUT, f"{song_id}.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {song_id}.html ({len(html)} bytes)")

# Generate all
for s in SONGS:
    generate(s)

print(f"\n🎉 生成了 {len(SONGS)} 个课件")
