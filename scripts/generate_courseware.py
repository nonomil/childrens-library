#!/usr/bin/env python3
"""批量生成幼儿英语童谣互动课件 - 对齐 Old MacDonald 模板"""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "courseware")

def make_scene_svg(element, colors):
    c0, c1 = colors.split(",")
    svgs = {
        "bus": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect x="80" y="80" width="280" height="100" rx="20" fill="#FFD54F" stroke="#FF8F00" stroke-width="3"/><rect x="100" y="100" width="120" height="50" rx="8" fill="#81D4FA" stroke="#4FC3F7" stroke-width="2"/><rect x="230" y="100" width="100" height="50" rx="8" fill="#81D4FA" stroke="#4FC3F7" stroke-width="2"/><circle cx="130" cy="190" r="22" fill="#424242"/><circle cx="130" cy="190" r="14" fill="#9E9E9E"/><circle cx="310" cy="190" r="22" fill="#424242"/><circle cx="310" cy="190" r="14" fill="#9E9E9E"/><rect x="250" y="90" width="8" height="40" rx="4" fill="#FF8A65"/><ellipse cx="360" cy="60" rx="30" ry="15" fill="#FFF" opacity="0.3"/><ellipse cx="80" cy="50" rx="25" ry="12" fill="#FFF" opacity="0.2"/><rect x="148" y="108" width="60" height="34" rx="4" fill="#FFF" opacity="0.5"/></svg>',
        "boat": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect y="160" width="460" height="60" fill="#4FC3F7" opacity="0.4"/><path d="M100 160 L120 130 L340 130 L360 160 Z" fill="#8D6E63" stroke="#5D4037" stroke-width="3"/><rect x="200" y="90" width="20" height="40" rx="3" fill="#795548"/><polygon points="220,95 300,120 220,140" fill="#FFF" opacity="0.8" stroke="#90CAF9" stroke-width="2"/><ellipse cx="80" cy="50" rx="30" ry="12" fill="#FFF" opacity="0.3"/><ellipse cx="350" cy="60" rx="25" ry="10" fill="#FFF" opacity="0.2"/></svg>',
        "spider": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect x="210" y="40" width="40" height="140" rx="20" fill="#8D6E63"/><ellipse cx="230" cy="40" rx="30" ry="15" fill="#FFF9C4"/><circle cx="230" cy="80" r="10" fill="#5D4037"/><circle cx="226" cy="78" r="2" fill="#FFF"/><circle cx="234" cy="78" r="2" fill="#FFF"/><ellipse cx="230" cy="95" rx="8" ry="6" fill="#5D4037"/><path d="M210 85 Q195 75 200 65" fill="none" stroke="#5D4037" stroke-width="2"/><path d="M220 88 Q205 85 205 75" fill="none" stroke="#5D4037" stroke-width="2"/><path d="M250 85 Q265 75 260 65" fill="none" stroke="#5D4037" stroke-width="2"/><path d="M240 88 Q255 85 255 75" fill="none" stroke="#5D4037" stroke-width="2"/><ellipse cx="80" cy="40" rx="50" ry="20" fill="#FFF" opacity="0.3"/></svg>',
        "dog": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect y="160" width="460" height="60" fill="#81C784" opacity="0.3"/><ellipse cx="200" cy="80" rx="40" ry="30" fill="#FFCC80"/><ellipse cx="200" cy="95" rx="25" ry="20" fill="#FFE0B2"/><ellipse cx="230" cy="55" rx="28" ry="25" fill="#FFCC80" transform="rotate(15,230,55)"/><circle cx="240" cy="50" r="4" fill="#5D4037"/><circle cx="238" cy="48" r="1.5" fill="#FFF"/><ellipse cx="255" cy="60" rx="10" ry="6" fill="#5D4037"/><circle cx="220" cy="95" r="3" fill="#5D4037"/><ellipse cx="190" cy="80" rx="15" ry="10" fill="#A1887F"/><ellipse cx="260" cy="58" rx="8" ry="4" fill="#FFAB91"/><ellipse cx="80" cy="50" rx="30" ry="12" fill="#FFF" opacity="0.3"/></svg>',
        "abc": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><ellipse cx="80" cy="40" rx="40" ry="15" fill="#FFF" opacity="0.3"/><ellipse cx="380" cy="50" rx="35" ry="12" fill="#FFF" opacity="0.2"/><rect y="170" width="460" height="50" fill="#81C784" opacity="0.3"/><text x="60" y="120" font-size="40" font-weight="bold" fill="#FF5252" font-family="sans-serif">A</text><text x="120" y="110" font-size="32" font-weight="bold" fill="#FFB347" font-family="sans-serif">B</text><text x="180" y="120" font-size="40" font-weight="bold" fill="#4CAF50" font-family="sans-serif">C</text><text x="240" y="105" font-size="28" font-weight="bold" fill="#2196F3" font-family="sans-serif">D</text><text x="300" y="115" font-size="36" font-weight="bold" fill="#9C27B0" font-family="sans-serif">E</text><text x="360" y="108" font-size="30" font-weight="bold" fill="#E91E63" font-family="sans-serif">F</text><ellipse cx="130" cy="55" rx="5" ry="5" fill="#FF5252" opacity="0.4"/><ellipse cx="230" cy="40" rx="4" ry="4" fill="#4CAF50" opacity="0.4"/><ellipse cx="330" cy="50" rx="5" ry="5" fill="#9C27B0" opacity="0.4"/></svg>',
        "star": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect y="180" width="460" height="40" fill="#1B5E20" opacity="0.15"/><ellipse cx="80" cy="35" rx="50" ry="15" fill="#FFF" opacity="0.3"/><text x="80" y="110" font-size="28" font-weight="bold" fill="#FFD700" font-family="sans-serif">★</text><text x="160" y="95" font-size="22" font-weight="bold" fill="#FFF" font-family="sans-serif">★</text><text x="230" y="110" font-size="32" font-weight="bold" fill="#FFD700" font-family="sans-serif">★</text><text x="310" y="90" font-size="20" font-weight="bold" fill="#FFF" font-family="sans-serif">★</text><text x="370" y="105" font-size="26" font-weight="bold" fill="#FFD700" font-family="sans-serif">★</text><ellipse cx="130" cy="45" rx="4" ry="4" fill="#FFF" opacity="0.5"/><ellipse cx="300" cy="50" rx="3" ry="3" fill="#FFF" opacity="0.4"/><rect x="210" y="140" width="40" height="45" rx="3" fill="#A1887F"/></svg>',
        "egg": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect y="170" width="460" height="50" fill="#81C784" opacity="0.3"/><ellipse cx="80" cy="35" rx="40" ry="12" fill="#FFF" opacity="0.3"/><rect x="220" y="30" width="20" height="140" rx="4" fill="#A1887F"/><ellipse cx="230" cy="30" rx="30" ry="12" fill="#8D6E63"/><ellipse cx="230" cy="95" rx="28" ry="35" fill="#FFCC80"/><ellipse cx="230" cy="95" rx="24" ry="30" fill="#FFE0B2"/><circle cx="222" cy="88" r="2.5" fill="#5D4037"/><circle cx="238" cy="88" r="2.5" fill="#5D4037"/><path d="M222,95 Q230,102 238,95" fill="none" stroke="#5D4037" stroke-width="1.5"/></svg>',
        "happy": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><ellipse cx="80" cy="40" rx="50" ry="15" fill="#FFF" opacity="0.3"/><ellipse cx="380" cy="55" rx="40" ry="12" fill="#FFF" opacity="0.2"/><rect y="175" width="460" height="45" fill="#66BB6A" opacity="0.25"/><circle cx="150" cy="100" r="45" fill="#FFCC80"/><circle cx="135" cy="90" r="4" fill="#5D4037"/><circle cx="165" cy="90" r="4" fill="#5D4037"/><circle cx="148" cy="98" r="1.5" fill="#FFF"/><circle cx="162" cy="98" r="1.5" fill="#FFF"/><path d="M133,108 Q145,120 158,110" fill="none" stroke="#5D4037" stroke-width="2" stroke-linecap="round"/><circle cx="148" cy="108" r="4" fill="#E91E63"/><path d="M135,105 L130,80" stroke="#5D4037" stroke-width="2.5" stroke-linecap="round"/><path d="M165,105 L170,80" stroke="#5D4037" stroke-width="2.5" stroke-linecap="round"/><circle cx="130" cy="80" r="6" fill="#FFCC80"/><circle cx="170" cy="80" r="6" fill="#FFCC80"/><circle cx="130" cy="78" r="2" fill="#5D4037"/><circle cx="170" cy="78" r="2" fill="#5D4037"/><circle cx="300" cy="100" r="35" fill="#FFCC80"/><circle cx="290" cy="93" r="3" fill="#5D4037"/><circle cx="310" cy="93" r="3" fill="#5D4037"/><path d="M290,103 Q300,112 310,103" fill="none" stroke="#5D4037" stroke-width="2" stroke-linecap="round"/></svg>',
        "bridge": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><ellipse cx="80" cy="40" rx="45" ry="15" fill="#FFF" opacity="0.3"/><ellipse cx="380" cy="50" rx="35" ry="12" fill="#FFF" opacity="0.2"/><rect y="170" width="460" height="50" fill="#4FC3F7" opacity="0.3"/><path d="M0 120 Q115 60 230 80 Q345 60 460 120" fill="none" stroke="#8D6E63" stroke-width="8" stroke-linecap="round"/><path d="M0 140 Q115 80 230 100 Q345 80 460 140" fill="none" stroke="#A1887F" stroke-width="6" stroke-linecap="round"/><rect x="105" y="70" width="8" height="50" fill="#795548"/><rect x="345" y="70" width="8" height="50" fill="#795548"/><rect x="225" y="80" width="10" height="40" fill="#795548"/><ellipse cx="230" cy="160" rx="12" ry="8" fill="#FFF" opacity="0.5"/></svg>',
        "lamb": f'<svg viewBox="0 0 460 220"><rect width="460" height="220" fill="url(#s)"/><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{c0}"/><stop offset="100%" stop-color="{c1}"/></linearGradient></defs><rect y="170" width="460" height="50" fill="#81C784" opacity="0.3"/><ellipse cx="80" cy="35" rx="40" ry="12" fill="#FFF" opacity="0.3"/><ellipse cx="380" cy="45" rx="35" ry="10" fill="#FFF" opacity="0.2"/><ellipse cx="230" cy="95" rx="40" ry="28" fill="#FFF"/><ellipse cx="230" cy="100" rx="28" ry="22" fill="#FAFAFA"/><ellipse cx="215" cy="88" rx="12" ry="10" fill="#E0E0E0"/><ellipse cx="245" cy="88" rx="12" ry="10" fill="#E0E0E0"/><ellipse cx="230" cy="80" rx="10" ry="8" fill="#E0E0E0"/><circle cx="235" cy="78" r="2.5" fill="#5D4037"/><circle cx="243" cy="78" r="2.5" fill="#5D4037"/><ellipse cx="225" cy="76" rx="2" ry="1.5" fill="#FFF"/><ellipse cx="241" cy="76" rx="2" ry="1.5" fill="#FFF"/><ellipse cx="238" cy="83" rx="4" ry="2" fill="#F48FB1"/><rect x="215" y="118" width="8" height="12" rx="2" fill="#E0E0E0"/><rect x="237" y="118" width="8" height="12" rx="2" fill="#E0E0E0"/><ellipse cx="200" cy="95" rx="4" ry="6" fill="#E0E0E0"/><ellipse cx="260" cy="95" rx="4" ry="6" fill="#E0E0E0"/></svg>',
    }
    return svgs.get(element, svgs["bus"])

QUIZ_DATA = {
    "wheels-on-bus": [
        {"q":"公车的什么在转啊转？", "opts":["🚌 Wheels","🚪 Door","📯 Horn"], "ans":0, "feedback":"对！轮子 round and round!"},
        {"q":"公车上的人们怎么动？", "opts":["⬆️⬇️ Up&Down","↔️ Side to Side","🔁 Round&Round"], "ans":0, "feedback":"没错！People go up and down!"},
        {"q":"雨刷发出什么声音？", "opts":["🔔 Ding Ding","💦 Swish Swish","📯 Beep Beep"], "ans":1, "feedback":"Swish swish swish! 雨刷把雨水刷走!"},
    ],
    "itsy-bitsy-spider": [
        {"q":"小蜘蛛爬上了什么？", "opts":["🧱 Wall","🌧️ Rain","💧 Water Spout"], "ans":2, "feedback":"对！爬上了水管 water spout!"},
        {"q":"什么把蜘蛛冲下来了？", "opts":["☀️ Sun","🌧️ Rain","🌬️ Wind"], "ans":1, "feedback":"下雨了！Down came the rain!"},
        {"q":"太阳出来后雨水怎样了？", "opts":["❄️ 结冰","💨 吹走","☀️ 晒干"], "ans":2, "feedback":"Dried up all the rain! 太阳晒干了雨水!"},
    ],
    "bingo": [
        {"q":"农夫养了什么动物？", "opts":["🐱 Cat","🐶 Dog","🐤 Duck"], "ans":1, "feedback":"Bingo is a dog! 🐶"},
        {"q":"小狗叫什么名字？", "opts":["🐕 Bingo","🐕 Rover","🐕 Spot"], "ans":0, "feedback":"B-I-N-G-O! 名字叫 Bingo!"},
        {"q":"Bingo的名字有几个字母？", "opts":["3个","5个","6个"], "ans":1, "feedback":"B-I-N-G-O 是5个字母哦!"},
    ],
    "abc-song": [
        {"q":"字母歌里第一个字母是？", "opts":["B","A","C"], "ans":1, "feedback":"A is the first letter! 🅰️"},
        {"q":"字母歌里有多少个字母？", "opts":["24","26","28"], "ans":1, "feedback":"26个字母 from A to Z!"},
        {"q":"Z后面是什么字母？", "opts":["A","没有","Y"], "ans":1, "feedback":"Z是最后一个字母! Now I know my ABCs!"},
    ],
    "head-shoulders": [
        {"q":"Head 是哪个部位？", "opts":["👋 手","👂 耳朵","👶 头"], "ans":2, "feedback":"Head is your head! 头!"},
        {"q":"Ears 是哪个部位？", "opts":["👀 眼睛","👂 耳朵","👃 鼻子"], "ans":1, "feedback":"Ears! 耳朵用来听声音!"},
        {"q":"身体部位一共有几个？", "opts":["3个","6个","8个"], "ans":2, "feedback":"Head, shoulders, knees, toes, eyes, ears, mouth, nose~ 一共8个!"},
    ],
    "humpty-dumpty": [
        {"q":"Humpty Dumpty 是什么？", "opts":["🥚 蛋","🍎 苹果","🧱 砖头"], "ans":0, "feedback":"Humpty Dumpty 是蛋头先生!"},
        {"q":"Humpty 坐在哪里？", "opts":["🧱 墙上","🪑 椅子上","🌳 树上"], "ans":0, "feedback":"Sat on a wall! 坐在墙头!"},
        {"q":"谁能把Humpty拼回去？", "opts":["🤴 国王","👨 没人能","🐴 马"], "ans":1, "feedback":"All the king horses couldn't put him together!"},
    ],
    "if-youre-happy": [
        {"q":"开心的时候要做什么？", "opts":["😢 哭","👏 拍手","😴 睡觉"], "ans":1, "feedback":"Clap your hands! 开心就拍拍手!"},
        {"q":"Stomp your feet 是什么意思？", "opts":["🤲 搓手","🦶 跺脚","🤸 翻跟头"], "ans":1, "feedback":"Stomp your feet! 跺跺脚!"},
        {"q":"开心的时候喊什么？", "opts":["😡 Hurray","😢 Boohoo","😴 Zzz"], "ans":0, "feedback":"SHOUT HURRAY! 🎉"},
    ],
    "london-bridge": [
        {"q":"London Bridge 怎么了？", "opts":["🌉 正在倒","🏗️ 在建","✅ 好好的"], "ans":0, "feedback":"London Bridge is falling down!"},
        {"q":"用什么修桥？", "opts":["🧱 石头","🔩 铁棍","🪵 木头"], "ans":1, "feedback":"Build it up with iron bars! 铁棍!"},
        {"q":"My fair lady 指的是？", "opts":["👸 淑女","🧙 女巫","👩 妈妈"], "ans":0, "feedback":"My fair lady! 我美丽的淑女!"},
    ],
    "mary-lamb": [
        {"q":"Mary 养了什么动物？", "opts":["🐱 猫","🐑 小羊","🐶 狗"], "ans":1, "feedback":"Mary had a little lamb! 小羊羔!"},
        {"q":"羊毛像什么一样白？", "opts":["☁️ 云","❄️ 雪","🦷 牙齿"], "ans":1, "feedback":"White as snow! 像雪一样白!"},
        {"q":"小羊跟着Mary去了哪？", "opts":["🏫 学校","🏪 商店","🏠 家"], "ans":0, "feedback":"Followed her to school! 跟着去了学校!"},
    ],
}

MELODIES = {
    "wheels-on-bus": "function playMelody(){const m=[[NOTE.G4,0.3],[NOTE.G4,0.3],[NOTE.G4,0.3],[NOTE.E4,0.3],[NOTE.G4,0.3],[NOTE.G4,0.3],[NOTE.G4,0.6],[NOTE.D4,0.3],[NOTE.D4,0.3],[NOTE.D4,0.3],[NOTE.G4,0.3],[NOTE.E4,0.6]];m.forEach(function(n){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},200);});}",
    "itsy-bitsy-spider": "function playMelody(){const m=[[NOTE.C4,0.3],[NOTE.E4,0.3],[NOTE.G4,0.3],[NOTE.C5,0.5],[NOTE.B4,0.3],[NOTE.G4,0.3],[NOTE.E4,0.3],[NOTE.C4,0.5]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
    "bingo": "function playMelody(){const m=[[NOTE.G4,0.25],[NOTE.G4,0.25],[NOTE.G4,0.25],[NOTE.D4,0.25],[NOTE.E4,0.25],[NOTE.E4,0.25],[NOTE.D4,0.5]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*180);});}",
    "abc-song": "function playMelody(){const m=[[NOTE.C4,0.3],[NOTE.D4,0.3],[NOTE.E4,0.3],[NOTE.F4,0.3],[NOTE.G4,0.3],[NOTE.A4,0.3],[NOTE.B4,0.3],[NOTE.C5,0.6]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
    "head-shoulders": "function playMelody(){const m=[[NOTE.E4,0.3],[NOTE.G4,0.3],[NOTE.A4,0.3],[NOTE.B4,0.3],[NOTE.C5,0.5],[NOTE.B4,0.3],[NOTE.A4,0.3],[NOTE.G4,0.5]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
    "humpty-dumpty": "function playMelody(){const m=[[NOTE.G4,0.3],[NOTE.E4,0.3],[NOTE.G4,0.3],[NOTE.D4,0.3],[NOTE.C4,0.3],[NOTE.D4,0.3],[NOTE.E4,0.3],[NOTE.C4,0.5]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
    "if-youre-happy": "function playMelody(){const m=[[NOTE.C4,0.3],[NOTE.C4,0.3],[NOTE.D4,0.3],[NOTE.C4,0.3],[NOTE.F4,0.3],[NOTE.E4,0.6],[NOTE.C4,0.3],[NOTE.C4,0.3],[NOTE.D4,0.3],[NOTE.C4,0.3],[NOTE.G4,0.3],[NOTE.F4,0.6]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
    "london-bridge": "function playMelody(){const m=[[NOTE.G4,0.3],[NOTE.A4,0.3],[NOTE.G4,0.3],[NOTE.F4,0.3],[NOTE.E4,0.3],[NOTE.F4,0.3],[NOTE.G4,0.6],[NOTE.C5,0.3],[NOTE.B4,0.3],[NOTE.A4,0.3],[NOTE.G4,0.3],[NOTE.F4,0.3],[NOTE.E4,0.6]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
    "mary-lamb": "function playMelody(){const m=[[NOTE.E4,0.3],[NOTE.D4,0.3],[NOTE.C4,0.3],[NOTE.D4,0.3],[NOTE.E4,0.3],[NOTE.E4,0.3],[NOTE.E4,0.5],[NOTE.D4,0.3],[NOTE.D4,0.3],[NOTE.D4,0.5],[NOTE.E4,0.3],[NOTE.G4,0.3],[NOTE.G4,0.5]];m.forEach(function(n,i){setTimeout(function(){playNote(n[0],n[1],'triangle',0.2);},i*200);});}",
}

TEMPLATE_HTML = open(os.path.join(os.path.dirname(__file__), "template_nursery.html"), "r", encoding="utf-8").read()

SONGS = [
    {"id":"wheels-on-bus","title":"The Wheels on the Bus","emoji":"🚌","mp3":"wheels.mp3","cover_subtitle":"✏️ 公车的轮子转啊转！",
     "pages":[
        {"sentence":'The <span class="hl" data-word="wheels">wheels</span> on the bus go <span class="hl" data-word="round">round</span> and <span class="hl" data-word="round">round</span>',"desc":"公车的轮子转啊转","game":"wheels"},
        {"sentence":'The <span class="hl" data-word="people">people</span> on the bus go <span class="hl" data-word="up">up</span> and <span class="hl" data-word="down">down</span>',"desc":"公车的人们上上下下","game":"people"},
        {"sentence":'The <span class="hl" data-word="wipers">wipers</span> on the bus go <span class="hl" data-word="swish">swish</span> swish swish',"desc":"公车的雨刷刷刷刷","game":"wipers"},
        {"sentence":'The <span class="hl" data-word="horn">horn</span> on the bus goes <span class="hl" data-word="beep">beep</span> beep beep',"desc":"公车的喇叭哔哔哔","game":"horn"},
        {"sentence":'The <span class="hl" data-word="door">door</span> on the bus goes <span class="hl" data-word="open">open</span> and <span class="hl" data-word="shut">shut</span>',"desc":"公车的门开了关","game":"door"},
     ],"svg_bg":"#87CEEB,#E0F7FA","svg_element":"bus","melody_key":"wheels-on-bus","quiz_key":"wheels-on-bus"},
    {"id":"itsy-bitsy-spider","title":"Itsy Bitsy Spider","emoji":"🕷️","mp3":"itsybitsy.mp3","cover_subtitle":"✏️ 小蜘蛛爬水管！",
     "pages":[
        {"sentence":'The <span class="hl" data-word="itsy">itsy</span> <span class="hl" data-word="bitsy">bitsy</span> <span class="hl" data-word="spider">spider</span> went up the water <span class="hl" data-word="spout">spout</span>',"desc":"小蜘蛛爬上了水管","game":"spider"},
        {"sentence":'Down came the <span class="hl" data-word="rain">rain</span> and washed the spider <span class="hl" data-word="out">out</span>',"desc":"下雨了把蜘蛛冲出来","game":"rain"},
        {"sentence":'Out came the <span class="hl" data-word="sun">sun</span> and dried up all the <span class="hl" data-word="rain">rain</span>',"desc":"太阳出来晒干了雨水","game":"sun"},
        {"sentence":'And the itsy bitsy spider went up the spout <span class="hl" data-word="again">again</span>',"desc":"小蜘蛛又爬上了水管","game":"again"},
     ],"svg_bg":"#A5D6A7,#C8E6C9","svg_element":"spider","melody_key":"itsy-bitsy-spider","quiz_key":"itsy-bitsy-spider"},
    {"id":"bingo","title":"BINGO","emoji":"🐶","mp3":"bingo.mp3","cover_subtitle":"✏️ 农夫有一只小狗叫BINGO！",
     "pages":[
        {"sentence":'There was a <span class="hl" data-word="farmer">farmer</span> had a <span class="hl" data-word="dog">dog</span>',"desc":"农夫有一只小狗","game":"farmer"},
        {"sentence":'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o',"desc":"Bingo是它的名字","game":"bingo"},
        {"sentence":'B-I-N-G-O, <span class="hl" data-word="B">B</span>-<span class="hl" data-word="I">I</span>-<span class="hl" data-word="N">N</span>-<span class="hl" data-word="G">G</span>-<span class="hl" data-word="O">O</span>',"desc":"拼出BINGO的名字","game":"bingo"},
        {"sentence":'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o!',"desc":"Bingo就是它的名字！","game":"name"},
     ],"svg_bg":"#FFE0B2,#FFF3E0","svg_element":"dog","melody_key":"bingo","quiz_key":"bingo"},
    {"id":"abc-song","title":"ABC Song","emoji":"🔤","mp3":"abcsong.mp3","cover_subtitle":"✏️ 一起来学英文字母歌！",
     "pages":[
        {"sentence":'<span class="hl" data-word="A">A</span>-<span class="hl" data-word="B">B</span>-<span class="hl" data-word="C">C</span>-<span class="hl" data-word="D">D</span>-<span class="hl" data-word="E">E</span>-<span class="hl" data-word="F">F</span>-<span class="hl" data-word="G">G</span>',"desc":"字母ABCDEFG","game":"abcdefg"},
        {"sentence":'<span class="hl" data-word="H">H</span>-<span class="hl" data-word="I">I</span>-<span class="hl" data-word="J">J</span>-<span class="hl" data-word="K">K</span>-<span class="hl" data-word="L">L</span>-<span class="hl" data-word="M">M</span>-<span class="hl" data-word="N">N</span>-<span class="hl" data-word="O">O</span>-<span class="hl" data-word="P">P</span>',"desc":"字母HIJKLMNOP","game":"hijklmnop"},
        {"sentence":'<span class="hl" data-word="Q">Q</span>-<span class="hl" data-word="R">R</span>-<span class="hl" data-word="S">S</span>-<span class="hl" data-word="T">T</span>-<span class="hl" data-word="U">U</span>-<span class="hl" data-word="V">V</span>',"desc":"字母QRSTUV","game":"qrstuv"},
        {"sentence":'<span class="hl" data-word="W">W</span>-<span class="hl" data-word="X">X</span>-<span class="hl" data-word="Y">Y</span>-<span class="hl" data-word="Z">Z</span>',"desc":"字母WXYZ","game":"wxyz"},
        {"sentence":'Now I know my <span class="hl" data-word="ABC">ABC</span>s, sing with <span class="hl" data-word="me">me</span>!',"desc":"我会唱字母歌了！","game":"abcs"},
     ],"svg_bg":"#E8EAF6,#C5CAE9","svg_element":"abc","melody_key":"abc-song","quiz_key":"abc-song"},
    {"id":"head-shoulders","title":"Head Shoulders Knees &amp; Toes","emoji":"🧍","mp3":"headshoulders.mp3","cover_subtitle":"✏️ 一起来认识身体部位！",
     "pages":[
        {"sentence":'<span class="hl" data-word="Head">Head</span>, <span class="hl" data-word="shoulders">shoulders</span>, <span class="hl" data-word="knees">knees</span> and <span class="hl" data-word="toes">toes</span>',"desc":"头肩膀膝盖和脚趾","game":"head"},
        {"sentence":'<span class="hl" data-word="Eyes">Eyes</span> and <span class="hl" data-word="ears">ears</span> and <span class="hl" data-word="mouth">mouth</span> and <span class="hl" data-word="nose">nose</span>',"desc":"眼睛耳朵嘴巴和鼻子","game":"eyes"},
        {"sentence":'<span class="hl" data-word="Head">Head</span>, <span class="hl" data-word="shoulders">shoulders</span>, <span class="hl" data-word="knees">knees</span> and <span class="hl" data-word="toes">toes</span>',"desc":"我们再来一遍！","game":"knees"},
        {"sentence":'<span class="hl" data-word="Eyes">Eyes</span> and <span class="hl" data-word="ears">ears</span> and <span class="hl" data-word="mouth">mouth</span> and <span class="hl" data-word="nose">nose</span>',"desc":"我们都认识身体部位啦！","game":"mouth"},
     ],"svg_bg":"#FFF8E1,#FFECB3","svg_element":"star","melody_key":"head-shoulders","quiz_key":"head-shoulders"},
    {"id":"humpty-dumpty","title":"Humpty Dumpty","emoji":"🥚","mp3":"humptydumpty.mp3","cover_subtitle":"✏️ 蛋头先生坐在墙头上！",
     "pages":[
        {"sentence":'<span class="hl" data-word="Humpty">Humpty</span> <span class="hl" data-word="Dumpty">Dumpty</span> sat on a <span class="hl" data-word="wall">wall</span>',"desc":"蛋头先生坐在墙头上","game":"humpty"},
        {"sentence":'Humpty Dumpty had a <span class="hl" data-word="great">great</span> <span class="hl" data-word="fall">fall</span>',"desc":"蛋头先生摔了一大跤","game":"great"},
        {"sentence":'All the <span class="hl" data-word="king">king</span> horses and all the king men',"desc":"国王所有的马和士兵","game":"king"},
        {"sentence":'Couldn put Humpty together <span class="hl" data-word="again">again</span>',"desc":"都没法把蛋头拼回去","game":"again"},
     ],"svg_bg":"#E3F2FD,#BBDEFB","svg_element":"egg","melody_key":"humpty-dumpty","quiz_key":"humpty-dumpty"},
    {"id":"if-youre-happy","title":"If You're Happy","emoji":"😊","mp3":"if_happy.mp3","cover_subtitle":"✏️ 如果你开心你就拍拍手！",
     "pages":[
        {"sentence":'If you happy and you <span class="hl" data-word="know">know</span> it, <span class="hl" data-word="clap">clap</span> your <span class="hl" data-word="hands">hands</span>!',"desc":"如果你开心就拍拍手","game":"happy"},
        {"sentence":'If you happy and you know it, <span class="hl" data-word="stomp">stomp</span> your <span class="hl" data-word="feet">feet</span>!',"desc":"如果你开心就跺跺脚","game":"stomp"},
        {"sentence":'If you happy and you know it, <span class="hl" data-word="shout">shout</span> Hurray!',"desc":"如果你开心就喊Hurray","game":"shout"},
        {"sentence":'If you happy and you know it, do <span class="hl" data-word="all">all</span> <span class="hl" data-word="three">three</span>!',"desc":"如果你开心就全做一遍","game":"three"},
     ],"svg_bg":"#FFF9C4,#FFF59D","svg_element":"happy","melody_key":"if-youre-happy","quiz_key":"if-youre-happy"},
    {"id":"london-bridge","title":"London Bridge","emoji":"🌉","mp3":"london_bridge.mp3","cover_subtitle":"✏️ 伦敦桥要倒啦！",
     "pages":[
        {"sentence":'<span class="hl" data-word="London">London</span> <span class="hl" data-word="Bridge">Bridge</span> is <span class="hl" data-word="falling">falling</span> <span class="hl" data-word="down">down</span>',"desc":"伦敦桥要倒了","game":"london"},
        {"sentence":'London Bridge is falling down, my <span class="hl" data-word="fair">fair</span> <span class="hl" data-word="lady">lady</span>',"desc":"伦敦桥要倒了，我美丽的淑女","game":"fair"},
        {"sentence":'<span class="hl" data-word="Build">Build</span> it <span class="hl" data-word="up">up</span> with <span class="hl" data-word="iron">iron</span> <span class="hl" data-word="bars">bars</span>',"desc":"用铁棍把桥修好","game":"build"},
        {"sentence":'Iron bars will <span class="hl" data-word="bend">bend</span> and <span class="hl" data-word="break">break</span>',"desc":"铁棍也会弯会断","game":"break"},
     ],"svg_bg":"#E0F7FA,#B2EBF2","svg_element":"bridge","melody_key":"london-bridge","quiz_key":"london-bridge"},
    {"id":"mary-lamb","title":"Mary Had a Little Lamb","emoji":"🐑","mp3":"mary_lamb.mp3","cover_subtitle":"✏️ 玛丽有一只小羊羔！",
     "pages":[
        {"sentence":'<span class="hl" data-word="Mary">Mary</span> had a <span class="hl" data-word="little">little</span> <span class="hl" data-word="lamb">lamb</span>',"desc":"玛丽有只小羊羔","game":"mary"},
        {"sentence":'Mary had a little lamb, its <span class="hl" data-word="fleece">fleece</span> was white as <span class="hl" data-word="snow">snow</span>',"desc":"羊毛白如雪","game":"fleece"},
        {"sentence":'And everywhere that Mary went, the <span class="hl" data-word="lamb">lamb</span> was sure to <span class="hl" data-word="go">go</span>',"desc":"玛莉走到哪羊羔就跟到哪","game":"lamb"},
        {"sentence":'It <span class="hl" data-word="followed">followed</span> her to school one day',"desc":"有一天它跟着去了学校","game":"followed"},
     ],"svg_bg":"#F3E5F5,#E1BEE7","svg_element":"lamb","melody_key":"mary-lamb","quiz_key":"mary-lamb"},
]

def generate(song):
    song_id = song["id"]
    pages = song["pages"]
    emoji = song.get("emoji", "🎵")
    display_title = f"{emoji} {song['title']}".replace("'", "\\'")
    title_clean = re.sub(r'[^a-zA-Z\\s]', '', song['title']).strip()
    sub_escaped = song["cover_subtitle"].replace("'", "\\'")
    n_pages = len(pages) + 4  # cover + pages + match + quiz + final

    cover_svg = make_scene_svg(song["svg_element"], song["svg_bg"])

    # Build pages JS entries
    pages_js = []
    for p in pages:
        s = p["sentence"].replace("'", "\\'")
        d = p["desc"]
        g = p["game"] or ""
        pages_js.append(f"  {{ sentence:'{s}', desc:'{d}', game:'{g}', svg:'0' }},")
    pages_js_str = "\\n".join(pages_js)

    scene_svgs = [make_scene_svg(song["svg_element"], song["svg_bg"]) for _ in pages]
    scenes_str = ",\\n    ".join(f"`{s}`" for s in scene_svgs)

    seen = set()
    for p in pages:
        if p["game"] and p["game"] not in seen:
            seen.add(p["game"])
    match_words = ",".join(f'"{w}"' for w in seen)

    melody_key = song.get("melody_key", song_id)
    melody_func = MELODIES.get(melody_key, "function playMelody(){playNote(440,0.5);}")
    melody_func = melody_func.replace("function", "function")  # already correct

    quiz_key = song.get("quiz_key", song_id)
    quiz_data_list = QUIZ_DATA.get(quiz_key, [{"q":"Is this fun?","opts":["Yes!","No"],"ans":0,"feedback":"Learning is fun!"}])
    quiz_data_json = json.dumps(quiz_data_list, ensure_ascii=False)

    html = TEMPLATE_HTML
    html = html.replace("__DISPLAY_TITLE__", display_title)
    html = html.replace("__TITLE__", f"{emoji} {song['title']}")
    html = html.replace("__COVER_SUBTITLE__", sub_escaped)
    html = html.replace("__PAGES_JS__", pages_js_str)
    html = html.replace("__SCENES__", scenes_str)
    html = html.replace("__MATCH_WORDS__", match_words)
    html = html.replace("__MP3FILE__", song["mp3"])
    html = html.replace("__COVER_SVG__", cover_svg)
    html = html.replace("__SPEAK_TITLE__", display_title)
    html = html.replace("__SPEAK_TEXT__", title_clean)
    html = html.replace("__SONG_MELODY__", melody_func)
    html = html.replace("__QUIZ_DATA__", quiz_data_json)
    html = html.replace("__TOTAL__", str(n_pages))

    outpath = os.path.join(OUT, f"{song_id}.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {song_id}.html ({len(html)} bytes)")

if __name__ == "__main__":
    print("🎵 生成童谣互动课件...")
    for s in SONGS:
        generate(s)
    print(f"\\n🎉 生成了 {len(SONGS)} 个课件")
