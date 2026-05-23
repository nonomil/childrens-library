#!/usr/bin/env python3
"""批量生成幼儿英语童谣互动课件 v3 - 新增拖拽互动游戏"""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "docs/courseware")

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

# ====== PER-SONG INTERACTIVE GAMES ======
# Each song gets custom drag/click/interact game data
INTERACT_GAMES = {
    "wheels-on-bus": {
        "title": "🚌 组装公车",
        "inst": "把零件拖到公车上！",
        "items": [
            {"id":"wheel","emoji":"⬤","label":"Wheels","zone":"车底","target":'130,190,310,190'},
            {"id":"wiper","emoji":"📐","label":"Wipers","zone":"车窗","target":'260,100'},
            {"id":"horn","emoji":"📯","label":"Horn","zone":"车顶","target":'330,80'},
            {"id":"door","emoji":"🚪","label":"Door","zone":"车身","target":'170,120'},
        ]
    },
    "itsy-bitsy-spider": {
        "title": "🕷️ 帮蜘蛛爬上去",
        "inst": "把蜘蛛拖到水管顶上！",
        "items": [
            {"id":"spider","emoji":"🕷️","label":"Spider","zone":"水管顶","target":'230,45'},
            {"id":"sun","emoji":"☀️","label":"Sun","zone":"天空","target":'380,40'},
            {"id":"rain","emoji":"🌧️","label":"Rain","zone":"水管上","target":'230,100'},
        ]
    },
    "bingo": {
        "title": "🐶 BINGO的项圈",
        "inst": "把B-I-N-G-O字母拖到项圈上！",
        "items": [
            {"id":"B","emoji":"B","label":"B","zone":"位置1","target":'185,55'},
            {"id":"I","emoji":"I","label":"I","zone":"位置2","target":'207,55'},
            {"id":"N","emoji":"N","label":"N","zone":"位置3","target":'229,55'},
            {"id":"G","emoji":"G","label":"G","zone":"位置4","target":'251,55'},
            {"id":"O","emoji":"O","label":"O","zone":"位置5","target":'273,55'},
        ]
    },
    "abc-song": {
        "title": "🔤 字母拼图",
        "inst": "把字母拖到正确位置！",
        "items": [
            {"id":"A","emoji":"A","label":"A","zone":"1","target":'60,120'},
            {"id":"B","emoji":"B","label":"B","zone":"2","target":'120,110'},
            {"id":"C","emoji":"C","label":"C","zone":"3","target":'180,120'},
        ]
    },
    "head-shoulders": {
        "title": "🧍 组装小朋友",
        "inst": "把身体部位拖到正确位置！",
        "items": [
            {"id":"head","emoji":"👶","label":"Head","zone":"头顶","target":'230,60'},
            {"id":"hand","emoji":"✋","label":"Hands","zone":"身体两侧","target":'180,110'},
            {"id":"foot","emoji":"🦶","label":"Feet","zone":"脚底","target":'220,170'},
        ]
    },
    "humpty-dumpty": {
        "title": "🥚 拼好蛋头先生",
        "inst": "把蛋的碎片拖回去！",
        "items": [
            {"id":"top","emoji":"🥚","label":"头顶","zone":"上方","target":'230,65'},
            {"id":"body","emoji":"🥚","label":"身体","zone":"中间","target":'230,100'},
            {"id":"base","emoji":"🥚","label":"底座","zone":"下方","target":'230,135'},
        ]
    },
    "if-youre-happy": {
        "title": "😊 动作配对",
        "inst": "把动作拖到对应位置！",
        "items": [
            {"id":"clap","emoji":"👏","label":"Clap","zone":"手","target":'130,80'},
            {"id":"stomp","emoji":"🦶","label":"Stomp","zone":"脚","target":'170,160'},
            {"id":"shout","emoji":"📣","label":"Shout","zone":"嘴巴","target":'230,60'},
        ]
    },
    "london-bridge": {
        "title": "🌉 修伦敦桥",
        "inst": "把桥的零件拖上去！",
        "items": [
            {"id":"arch","emoji":"🌉","label":"拱桥","zone":"中间","target":'230,80'},
            {"id":"bar","emoji":"🔩","label":"铁棍","zone":"桥面","target":'160,110'},
            {"id":"pillar","emoji":"🏛️","label":"桥墩","zone":"桥底","target":'105,100'},
        ]
    },
    "mary-lamb": {
        "title": "🐑 小羊找玛丽",
        "inst": "帮小羊找到玛丽！",
        "items": [
            {"id":"lamb","emoji":"🐑","label":"Lamb","zone":"玛丽身边","target":'200,130'},
            {"id":"mary","emoji":"👧","label":"Mary","zone":"前面","target":'270,100'},
            {"id":"school","emoji":"🏫","label":"School","zone":"后面","target":'380,80'},
        ]
    }
}

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
