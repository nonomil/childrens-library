#!/usr/bin/env python3
"""批量生成幼儿英语童谣互动课件，完全对标 Old MacDonald 格式"""

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


SONGS = [
    {"id":"bingo","title":"BINGO","emoji":"🐶","mp3":"bingo.mp3","cover_subtitle":"✏️ 农夫有一只小狗叫BINGO！",
     "pages":[
        {"sentence":'There was a <span class="hl" data-word="farmer">farmer</span> had a <span class="hl" data-word="dog">dog</span>',"desc":"农夫有一只小狗","game":"farmer"},
        {"sentence":'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o',"desc":"Bingo是它的名字","game":"bingo"},
        {"sentence":'B-I-N-G-O, <span class="hl" data-word="B">B</span>-<span class="hl" data-word="I">I</span>-<span class="hl" data-word="N">N</span>-<span class="hl" data-word="G">G</span>-<span class="hl" data-word="O">O</span>',"desc":"拼出BINGO的名字","game":"bingo"},
        {"sentence":'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o!',"desc":"Bingo就是它的名字！","game":"name"},
     ],"svg_bg":"#FFE0B2,#FFF3E0","svg_element":"dog"},
    {"id":"abc-song","title":"ABC Song","emoji":"🔤","mp3":"abcsong.mp3","cover_subtitle":"✏️ 一起来学英文字母歌！",
     "pages":[
        {"sentence":'<span class="hl" data-word="A">A</span>-<span class="hl" data-word="B">B</span>-<span class="hl" data-word="C">C</span>-<span class="hl" data-word="D">D</span>-<span class="hl" data-word="E">E</span>-<span class="hl" data-word="F">F</span>-<span class="hl" data-word="G">G</span>',"desc":"字母ABCDEFG","game":"abcdefg"},
        {"sentence":'<span class="hl" data-word="H">H</span>-<span class="hl" data-word="I">I</span>-<span class="hl" data-word="J">J</span>-<span class="hl" data-word="K">K</span>-<span class="hl" data-word="L">L</span>-<span class="hl" data-word="M">M</span>-<span class="hl" data-word="N">N</span>-<span class="hl" data-word="O">O</span>-<span class="hl" data-word="P">P</span>',"desc":"字母HIJKLMNOP","game":"hijklmnop"},
        {"sentence":'<span class="hl" data-word="Q">Q</span>-<span class="hl" data-word="R">R</span>-<span class="hl" data-word="S">S</span>-<span class="hl" data-word="T">T</span>-<span class="hl" data-word="U">U</span>-<span class="hl" data-word="V">V</span>',"desc":"字母QRSTUV","game":"qrstuv"},
        {"sentence":'<span class="hl" data-word="W">W</span>-<span class="hl" data-word="X">X</span>-<span class="hl" data-word="Y">Y</span>-<span class="hl" data-word="Z">Z</span>',"desc":"字母WXYZ","game":"wxyz"},
        {"sentence":'Now I know my <span class="hl" data-word="ABC">ABC</span>s, sing with <span class="hl" data-word="me">me</span>!',"desc":"我会唱字母歌了！","game":"abcs"},
     ],"svg_bg":"#E8EAF6,#C5CAE9","svg_element":"abc"},
    {"id":"head-shoulders","title":"Head Shoulders Knees &amp; Toes","emoji":"🧍","mp3":"headshoulders.mp3","cover_subtitle":"✏️ 一起来认识身体部位！",
     "pages":[
        {"sentence":'<span class="hl" data-word="Head">Head</span>, <span class="hl" data-word="shoulders">shoulders</span>, <span class="hl" data-word="knees">knees</span> and <span class="hl" data-word="toes">toes</span>',"desc":"头肩膀膝盖和脚趾","game":"head"},
        {"sentence":'<span class="hl" data-word="Eyes">Eyes</span> and <span class="hl" data-word="ears">ears</span> and <span class="hl" data-word="mouth">mouth</span> and <span class="hl" data-word="nose">nose</span>',"desc":"眼睛耳朵嘴巴和鼻子","game":"eyes"},
        {"sentence":'<span class="hl" data-word="Head">Head</span>, <span class="hl" data-word="shoulders">shoulders</span>, <span class="hl" data-word="knees">knees</span> and <span class="hl" data-word="toes">toes</span>',"desc":"我们再来一遍！","game":"knees"},
        {"sentence":'<span class="hl" data-word="Eyes">Eyes</span> and <span class="hl" data-word="ears">ears</span> and <span class="hl" data-word="mouth">mouth</span> and <span class="hl" data-word="nose">nose</span>',"desc":"我们都认识身体部位啦！","game":"mouth"},
     ],"svg_bg":"#FFF8E1,#FFECB3","svg_element":"star"},
    {"id":"humpty-dumpty","title":"Humpty Dumpty","emoji":"🥚","mp3":"humptydumpty.mp3","cover_subtitle":"✏️ 蛋头先生坐在墙头上！",
     "pages":[
        {"sentence":'<span class="hl" data-word="Humpty">Humpty</span> <span class="hl" data-word="Dumpty">Dumpty</span> sat on a <span class="hl" data-word="wall">wall</span>',"desc":"蛋头先生坐在墙头上","game":"humpty"},
        {"sentence":'Humpty Dumpty had a <span class="hl" data-word="great">great</span> <span class="hl" data-word="fall">fall</span>',"desc":"蛋头先生摔了一大跤","game":"great"},
        {"sentence":'All the <span class="hl" data-word="king">king</span> horses and all the king men',"desc":"国王所有的马和士兵","game":"king"},
        {"sentence":'Couldn put Humpty together <span class="hl" data-word="again">again</span>',"desc":"都没法把蛋头拼回去","game":"again"},
     ],"svg_bg":"#E3F2FD,#BBDEFB","svg_element":"egg"},
    {"id":"if-youre-happy","title":"If You're Happy","emoji":"😊","mp3":"if_happy.mp3","cover_subtitle":"✏️ 如果你开心你就拍拍手！",
     "pages":[
        {"sentence":'If you happy and you <span class="hl" data-word="know">know</span> it, <span class="hl" data-word="clap">clap</span> your <span class="hl" data-word="hands">hands</span>!',"desc":"如果你开心就拍拍手","game":"happy"},
        {"sentence":'If you happy and you know it, <span class="hl" data-word="stomp">stomp</span> your <span class="hl" data-word="feet">feet</span>!',"desc":"如果你开心就跺跺脚","game":"stomp"},
        {"sentence":'If you happy and you know it, <span class="hl" data-word="shout">shout</span> Hurray!',"desc":"如果你开心就喊Hurray","game":"shout"},
        {"sentence":'If you happy and you know it, do <span class="hl" data-word="all">all</span> <span class="hl" data-word="three">three</span>!',"desc":"如果你开心就全做一遍","game":"three"},
     ],"svg_bg":"#FFF9C4,#FFF59D","svg_element":"happy"},
    {"id":"london-bridge","title":"London Bridge","emoji":"🌉","mp3":"london_bridge.mp3","cover_subtitle":"✏️ 伦敦桥要倒啦！",
     "pages":[
        {"sentence":'<span class="hl" data-word="London">London</span> <span class="hl" data-word="Bridge">Bridge</span> is <span class="hl" data-word="falling">falling</span> <span class="hl" data-word="down">down</span>',"desc":"伦敦桥要倒了","game":"london"},
        {"sentence":'London Bridge is falling down, my <span class="hl" data-word="fair">fair</span> <span class="hl" data-word="lady">lady</span>',"desc":"伦敦桥要倒了，我美丽的淑女","game":"fair"},
        {"sentence":'<span class="hl" data-word="Build">Build</span> it <span class="hl" data-word="up">up</span> with <span class="hl" data-word="iron">iron</span> <span class="hl" data-word="bars">bars</span>',"desc":"用铁棍把桥修好","game":"build"},
        {"sentence":'Iron bars will <span class="hl" data-word="bend">bend</span> and <span class="hl" data-word="break">break</span>',"desc":"铁棍也会弯会断","game":"break"},
     ],"svg_bg":"#E0F7FA,#B2EBF2","svg_element":"bridge"},
    {"id":"mary-lamb","title":"Mary Had a Little Lamb","emoji":"🐑","mp3":"mary_lamb.mp3","cover_subtitle":"✏️ 玛丽有一只小羊羔！",
     "pages":[
        {"sentence":'<span class="hl" data-word="Mary">Mary</span> had a <span class="hl" data-word="little">little</span> <span class="hl" data-word="lamb">lamb</span>',"desc":"玛丽有只小羊羔","game":"mary"},
        {"sentence":'Mary had a little lamb, its <span class="hl" data-word="fleece">fleece</span> was white as <span class="hl" data-word="snow">snow</span>',"desc":"羊毛白如雪","game":"fleece"},
        {"sentence":'And everywhere that Mary went, the <span class="hl" data-word="lamb">lamb</span> was sure to <span class="hl" data-word="go">go</span>',"desc":"玛莉走到哪羊羔就跟到哪","game":"lamb"},
        {"sentence":'It <span class="hl" data-word="followed">followed</span> her to school one day',"desc":"有一天它跟着去了学校","game":"followed"},
     ],"svg_bg":"#F3E5F5,#E1BEE7","svg_element":"lamb"},
]

TEMPLATE_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>__TITLE__ - 互动课件</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; -webkit-touch-callout:none; -webkit-user-select:none; user-select:none; }
body {
  font-family:'Fredoka One','Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
  background:linear-gradient(145deg,#FFF8E7 0%,#FFE8C8 100%);
  min-height:100vh; display:flex; justify-content:center; align-items:center; padding:12px;
}
.book {
  width:100%; max-width:840px; min-height:92vh;
  background:#FFFCF5; border-radius:40px;
  box-shadow:0 20px 60px rgba(0,0,0,0.15),0 0 0 4px #FFF,0 0 0 8px #FFB347;
  padding:24px 20px; position:relative;
  font-family:'Fredoka One','Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
}
.page-area { min-height:420px; }
.page { display:none; flex-direction:column; align-items:center; animation:fadeIn .4s ease; width:100%; }
.page.active { display:flex; }
@keyframes fadeIn { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
@keyframes noteFloat { 0%{opacity:0;transform:translateY(20px) scale(0.5)} 30%{opacity:1;transform:translateY(-10px) scale(1.2)} 100%{opacity:0;transform:translateY(-60px) scale(0.8)} }
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
@keyframes shake { 0%,100%{transform:translateX(0)} 20%{transform:translateX(-6px)} 40%{transform:translateX(6px)} 60%{transform:translateX(-4px)} 80%{transform:translateX(4px)} }
@keyframes popIn { 0%{opacity:0;transform:scale(0.3)} 100%{opacity:1;transform:scale(1)} }
@keyframes confetti-fall { 0%{opacity:1;transform:translateY(0)rotate(0deg)} 100%{opacity:0;transform:translateY(500px)rotate(720deg)} }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.page-title { font-size:30px; color:#E8751A; text-align:center; margin-bottom:8px; font-weight:bold; }
.page-desc { font-size:18px; color:#6B4F3A; text-align:center; line-height:1.5; margin-bottom:10px; }
.scene-wrap { width:100%; max-width:460px; height:auto; margin:0 auto 10px; border-radius:20px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.08); }
.scene-wrap svg { display:block; width:100%; height:auto; }
.lyrics { font-size:26px; color:#E8751A; text-align:center; padding:12px 16px; background:#FFF8E7; border-radius:16px; width:100%; margin-bottom:8px; line-height:1.5; font-weight:bold; }
.lyrics .hl { color:#F44336; cursor:pointer; transition:all .2s; display:inline-block; }
.lyrics .hl:active { transform:scale(1.2); }
.lyrics .hl::after { content:'\U0001f50a'; font-size:14px; opacity:0.5; margin-left:4px; }
.word-game { width:100%; padding:14px; background:#FFF8E7; border-radius:18px; text-align:center; margin:6px 0; border:2px solid #FFE8C8; }
.word-game h3 { font-size:16px; color:#E8751A; margin-bottom:8px; display:flex; align-items:center; justify-content:center; gap:6px; }
.word-slots { display:flex; gap:6px; justify-content:center; margin-bottom:8px; }
.word-slot { width:48px; height:48px; border-bottom:4px solid #FFB347; display:flex; align-items:center; justify-content:center; font-size:28px; font-weight:bold; color:#E8751A; border-radius:8px 8px 0 0; background:rgba(255,248,231,0.5); transition:all .2s; }
.word-slot.filled { border-bottom-color:#4CAF50; background:rgba(232,245,233,0.5); animation:popIn .2s ease; }
.word-slot.drag-over { border-bottom-color:#66BB6A; border-bottom-width:6px; background:rgba(102,187,106,0.15); transform:scale(1.05); }
.letter-tiles { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }
.letter-tile { width:48px; height:48px; border-radius:12px; border:3px solid #E0D5C7; background:white; font-size:24px; font-weight:bold; cursor:grab; display:flex; align-items:center; justify-content:center; transition:all .15s; user-select:none; touch-action:none; }
.letter-tile:hover { border-color:#FFB347; background:#FFF8E7; }
.letter-tile:active { cursor:grabbing; }
.letter-tile.correct { border-color:#4CAF50; background:#E8F5E9; animation:popIn .3s ease; }
.letter-tile.wrong { border-color:#F44336; background:#FFEBEE; animation:shake .3s; }
.letter-tile.used { opacity:0.35; pointer-events:none; }
.letter-tile.dragging { opacity:0.5; }
.match-game { width:100%; padding:16px; background:#F1F8E9; border-radius:20px; text-align:center; margin:6px 0; border:2px solid #C8E6C9; }
.match-game h3 { font-size:18px; color:#2E7D32; margin-bottom:12px; }
.sound-btn { width:100px; height:100px; border-radius:50%; border:4px solid #FFB347; background:#FFF; font-size:36px; cursor:pointer; transition:all .15s; margin:0 auto 12px; display:flex; align-items:center; justify-content:center; }
.sound-btn:active { transform:scale(1.1); background:#FFF8E7; }
.word-choices { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; }
.word-choice { padding:10px 20px; border-radius:20px; border:3px solid #E0D5C7; background:white; cursor:pointer; transition:all .15s; font-size:18px; font-weight:bold; color:#6B4F3A; font-family:inherit; }
.word-choice:hover { border-color:#FFB347; background:#FFF8E7; transform:scale(1.05); }
.word-choice.correct { border-color:#4CAF50; background:#E8F5E9; animation:popIn .3s ease; }
.word-choice.wrong { border-color:#F44336; background:#FFEBEE; animation:shake .3s; }
.speech-bubble { position:fixed; bottom:120px; left:50%; transform:translateX(-50%) scale(0.5); border-radius:20px; background:rgba(255,255,255,0.96); border:3px solid #FFB347; padding:14px 22px; font-size:20px; font-weight:600; max-width:80%; text-align:center; z-index:10000; opacity:0; pointer-events:none; box-shadow:0 8px 30px rgba(255,179,71,0.3); transition:opacity .35s,transform .35s cubic-bezier(0.34,1.56,0.64,1); color:#5A3E2B; line-height:1.5; }
.speech-bubble.show { opacity:1; transform:translateX(-50%) scale(1); }
.speech-bubble::before { content:'\U0001f50a'; display:block; font-size:22px; margin-bottom:4px; }
.controls { display:flex; align-items:center; justify-content:space-between; margin-top:10px; gap:8px; position:sticky; bottom:0; background:#FFFCF5; padding:8px 0; z-index:100; }
.nav-btn { background:#FFB347; border:none; color:#FFF; font-size:28px; width:60px; height:60px; border-radius:50%; cursor:pointer; box-shadow:0 4px 12px rgba(255,179,71,0.4); transition:all .15s; display:flex; align-items:center; justify-content:center; flex-shrink:0; touch-action:manipulation; }
.nav-btn:hover { transform:scale(1.1); background:#FF9F1C; }
.nav-btn:disabled { opacity:0.3; cursor:default; transform:none; }
.nav-btn.small { width:48px; height:48px; font-size:22px; }
.read-btn { background:#6BCB77; border:none; color:#FFF; font-size:16px; padding:10px 18px; border-radius:30px; cursor:pointer; box-shadow:0 4px 12px rgba(107,203,119,0.4); font-family:inherit; font-weight:bold; display:flex; align-items:center; gap:5px; transition:all .15s; touch-action:manipulation; }
.read-btn:hover { transform:scale(1.06); }
.read-btn.pink { background:#FF8A80; }
.page-dots { display:flex; gap:6px; }
.page-dots .dot { width:10px; height:10px; border-radius:50%; background:#E0D5C7; cursor:pointer; transition:all .2s; }
.page-dots .dot.active { background:#FFB347; transform:scale(1.3); }
.page-dots .dot.done { background:#4CAF50; }
.page-counter { font-size:13px; color:#999; text-align:center; margin-top:6px; }
.big-start-btn { width:120px; height:120px; border-radius:50%; background:linear-gradient(145deg,#FFB347,#FF9F1C); border:6px solid #FFF; color:#FFF; font-size:32px; cursor:pointer; box-shadow:0 8px 30px rgba(255,179,71,0.5); transition:all .15s; margin:10px auto; display:flex; align-items:center; justify-content:center; animation:bounce 2s ease-in-out infinite; }
.big-start-btn:active { transform:scale(0.95); }
.big-start-btn.smaller { width:90px; height:90px; font-size:28px; }
.cover-svg { width:100%; max-width:400px; margin:0 auto; }
.final-grid { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; margin:10px 0; }
.final-word { padding:8px 16px; border-radius:16px; background:#FFF8E7; border:2px solid #FFE8C8; font-size:18px; font-weight:bold; color:#E8751A; }
.home-link { color:#FFB347; text-decoration:none; font-size:18px; font-weight:bold; margin-top:10px; display:inline-block; }
.home-link:hover { text-decoration:underline; }
.celebration { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9999; }
@media (max-width:500px) {
  .book { padding:16px 12px; }
  .page-title { font-size:24px; }
  .lyrics { font-size:20px; padding:10px 12px; }
  .letter-tile { width:40px; height:40px; font-size:20px; }
  .word-slot { width:40px; height:40px; font-size:22px; }
  .nav-btn { width:50px; height:50px; font-size:24px; }
  .nav-btn.small { width:40px; height:40px; font-size:18px; }
  .read-btn { font-size:14px; padding:8px 14px; }
  .sound-btn { width:80px; height:80px; font-size:28px; }
  .word-choice { font-size:16px; padding:8px 14px; }
  .big-start-btn { width:90px; height:90px; font-size:26px; }
}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
<div class="book">
  <div class="page-area" id="pageArea"></div>
  <div class="controls" id="controlsBar">
    <button class="nav-btn" id="prevBtn" onclick="prevPage()" disabled>&#x25C0;</button>
    <button class="nav-btn small" onclick="playSong();showMusicNotes()" style="animation:float 2s ease-in-out infinite">&#x1F3B5;</button>
    <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center">
      <button class="read-btn" onclick="speakPage()">&#x1F50A; 读</button>
      <button class="read-btn pink" onclick="playSong();showMusicNotes()">&#x1F3B5; 唱</button>
    </div>
    <button class="nav-btn" id="nextBtn" onclick="nextPage()">&#x25B6;</button>
  </div>
  <div class="page-dots" id="progressDots"></div>
  <div class="page-counter" id="pageCounter">第__CURRENT__页 / 共__TOTAL__页</div>
</div>
<div class="speech-bubble" id="speechBubble"></div>

<script>
// ====== PAGE DATA ======
const pages = [
  { cover:true, title:'__DISPLAY_TITLE__', subtitle:'__COVER_SUBTITLE__' },
__PAGES_JS__
  { match:true, title:'\U0001f50a 听声音找单词' },
  { final:true, title:'\U0001f389 太棒了!' }
];

let currentPage = 0;
let gameDone = new Array(pages.length).fill(false);
let buildingWord = [];
let dragData = null;

const NOTE = { C4:261.63, D4:293.66, E4:329.63, F4:349.23, G4:392.00, A4:440.00, B4:493.88, C5:523.25 };

var songAudio = null;
function playSong() {
  if(songAudio) { songAudio.pause(); songAudio.currentTime = 0; }
  songAudio = new Audio('audio/__MP3FILE__');
  songAudio.volume = 0.8;
  songAudio.play().catch(function(){});
}
function showMusicNotes() {
  var scene=document.querySelector('.scene-wrap'); if(!scene) return;
  var notes=['\u266a','\u266b','\u2669','\u266c'];
  for(var i=0;i<8;i++){var n=document.createElement('div');n.textContent=notes[i%4];n.style.cssText='position:absolute;font-size:'+(14+Math.random()*18)+'px;color:#FFB347;opacity:0;pointer-events:none;z-index:10;left:'+(Math.random()*80+10)+'%;top:'+(Math.random()*50+10)+'%;animation:noteFloat '+(1+Math.random())+'s ease-out forwards;animation-delay:'+(i*0.15)+'s;';scene.appendChild(n);setTimeout(function(e){e.remove()},3000,n);}
}
function speakText(text) {
  if('speechSynthesis' in window){window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text.replace(/<[^>]+>/g,''));u.lang='en-US';u.rate=0.75;u.pitch=1.0;window.speechSynthesis.speak(u);}
}
function showBubble(text) {
  var b=document.getElementById('speechBubble');b.textContent=text;b.classList.add('show');
  clearTimeout(b._t);b._t=setTimeout(function(){b.classList.remove('show')},3000);
}

// ====== SVG ======
var COVER_SVG = `__COVER_SVG__`;

function svgCoverScene() { return COVER_SVG; }

function getSVG(idx) {
  if(idx===0) return svgCoverScene();
  var p=pages[idx];
  var scenes = [__SCENES__];
  if(p.match) return COVER_SVG;
  if(p.final) return COVER_SVG.replace('height="220"','height="180"');
  return scenes[parseInt(p.svg)] || scenes[0];
}

// ====== WORD GAME ======
function startWordGame(idx,word) {
  if(gameDone[idx]) return '<div class="word-game" style="background:#E8F5E9"><h3>\u2705 完成!</h3></div>';
  var letters=word.split('').sort(function(){return Math.random()-0.5});
  buildingWord=[];
  var slots=word.split('').map(function(_,i){return '<div class="word-slot" id="slot-'+idx+'-'+i+'"></div>';}).join('');
  var tiles=letters.map(function(l){return '<div class="letter-tile" draggable="true" onclick="pickLetter('+idx+',\''+l+'\',this)" ondragstart="onDragStart(event,'+idx+',\''+l+'\')" ondragend="onDragEnd(event)">'+l+'</div>';}).join('');
  return '<div class="word-game"><h3>\u2699\uFE0F 拼单词: <strong>"'+word+'"</strong> \U0001f50a</h3><div class="word-slots" id="ws-'+idx+'">'+slots+'</div><div class="letter-tiles" id="tiles-'+idx+'">'+tiles+'</div></div>';
}

function pickLetter(idx,letter,el) {
  if(gameDone[idx]||el.classList.contains('used')) return;
  var word=pages[idx].game;
  var slot=buildingWord.length;
  if(slot>=word.length) return;
  var slots=document.querySelectorAll('#ws-'+idx+' .word-slot');
  if(letter===word[slot]){
    buildingWord.push(letter); slots[slot].textContent=letter; slots[slot].classList.add('filled');
    el.classList.add('correct','used');
    if(buildingWord.length===word.length){gameDone[idx]=true;setTimeout(function(){showBubble('Great! \U0001f389');launchConfetti();renderPage(idx);},500);}
  } else { el.classList.add('wrong'); setTimeout(function(){el.classList.remove('wrong');},400); }
}

function onDragStart(e,idx,letter){dragData={idx:idx,letter:letter,el:e.target};e.target.classList.add('dragging');e.dataTransfer.effectAllowed='move';}
function onDragEnd(e){e.target.classList.remove('dragging');var all=document.querySelectorAll('.word-slot.drag-over');for(var i=0;i<all.length;i++)all[i].classList.remove('drag-over');}
function onDragOver(e,idx){e.preventDefault();e.dataTransfer.dropEffect='move';var all=document.querySelectorAll('#ws-'+idx+' .word-slot:not(.filled)');for(var i=0;i<all.length;i++)all[i].classList.add('drag-over');}
function onDragLeave(e,idx){var all=document.querySelectorAll('#ws-'+idx+' .word-slot');for(var i=0;i<all.length;i++)all[i].classList.remove('drag-over');}
function onDrop(e,idx){
  e.preventDefault();var all=document.querySelectorAll('#ws-'+idx+' .word-slot');for(var i=0;i<all.length;i++)all[i].classList.remove('drag-over');
  if(!dragData||dragData.idx!==idx||gameDone[idx]) return;
  pickLetter(idx,dragData.letter,dragData.el);dragData=null;
}

// ====== MATCH GAME ======
const MATCH_WORDS = [__MATCH_WORDS__];
var matchRound = 0;
var matchDone = [];

function renderMatchGame() {
  if(matchDone.length>=MATCH_WORDS.length) return '<div class="match-game" style="background:#E8F5E9"><h3>\U0001f389 全部找到! 太棒了!</h3></div>';
  var word=MATCH_WORDS[matchRound];
  var shuffled=MATCH_WORDS.slice().sort(function(){return Math.random()-0.5});
  var opts=shuffled.map(function(w){var d=matchDone.indexOf(w)>=0?'style="opacity:0.5"':'';return '<div class="word-choice" data-word="'+w+'" onclick="checkMatch(\''+w+'\',this)" '+d+'>'+w+'</div>';}).join('');
  return '<div class="match-game"><h3>\U0001f50a 听单词: <strong>"'+word+'"</strong></h3><button class="sound-btn" onclick="speakMatchWord()">\U0001f50a</button><p style="font-size:14px;color:#6B4F3A;margin-bottom:8px;font-weight:bold">'+(matchRound+1)+'/'+MATCH_WORDS.length+'</p><div class="word-choices">'+opts+'</div></div>';
}

function speakMatchWord() {
  if(matchRound>=MATCH_WORDS.length) return;
  speakText(MATCH_WORDS[matchRound]);
  showBubble('\U0001f50a '+MATCH_WORDS[matchRound]);
}

function checkMatch(word,el) {
  if(matchRound>=MATCH_WORDS.length||matchDone.indexOf(word)>=0) return;
  if(word===MATCH_WORDS[matchRound]){
    el.classList.add('correct'); matchDone.push(word);
    showBubble('Great! Wonderful! \U0001f389');
    matchRound++;
    setTimeout(function(){renderPage(pages.length-2)},600);
  } else {
    el.classList.add('wrong');
    setTimeout(function(){el.classList.remove('wrong')},400);
    showBubble('\u518D\u8BD5\u8BD5~ Try again!');
  }
}

// ====== RENDER ======
function renderPage(idx) {
  var area=document.getElementById('pageArea');
  var p=pages[idx];

  if(p.cover){
    area.innerHTML='<div class="page active cover-page"><div class="cover-svg">'+getSVG(0)+'</div><div class="page-title">'+p.title+'</div><div class="page-desc">'+p.subtitle+'</div><div style="display:flex;gap:16px;justify-content:center;align-items:center;margin-top:4px"><button class="big-start-btn smaller" onclick="playSong();showMusicNotes()" style="animation:float 2s ease-in-out infinite">\U0001f3b5</button><button class="big-start-btn" onclick="nextPage()">\u25b6</button></div></div>';
    updateUI(idx); return;
  }

  if(p.final){
    var fw=MATCH_WORDS.map(function(w){return '<div class="final-word">\u2705 '+w+'</div>';}).join('');
    area.innerHTML='<div class="page active" style="text-align:center;padding:20px 10px"><div class="page-title">'+p.title+'</div><div class="scene-wrap" style="position:relative">'+getSVG(idx)+'</div><div style="font-size:24px;margin:10px 0">\U0001f389 \u2b50 \u2b50 \u2b50 \U0001f389</div><div class="final-grid">'+fw+'</div><a class="home-link" href="https://nonomil.github.io/childrens-library/courseware/">\U0001f3e0 \u56DE\u8BFE\u4EF6\u5217\u8868</a></div>';
    launchConfetti(); updateUI(idx); return;
  }

  if(p.match){
    area.innerHTML='<div class="page active"><div class="scene-wrap" style="position:relative">'+getSVG(idx)+'</div>'+renderMatchGame()+'</div>';
    updateUI(idx); return;
  }

  var gh='';
  if(p.game){gh=startWordGame(idx,p.game);buildingWord=[];}

  area.innerHTML='<div class="page active"><div class="scene-wrap" style="position:relative">'+getSVG(idx)+'</div><div class="lyrics">'+p.sentence+'</div><div class="page-desc">'+p.desc+'</div>'+gh+'</div>';

  var hls=area.querySelectorAll('.hl[data-word]');
  for(var hi=0;hi<hls.length;hi++){
    (function(el){el.addEventListener('click',function(e){e.stopPropagation();speakText(el.getAttribute('data-word'));showBubble('\U0001f50a '+el.getAttribute('data-word'));});})(hls[hi]);
  }

  updateUI(idx);
}

function updateUI(idx) {
  var dots=document.getElementById('progressDots');
  var dhtml='';
  for(var i=0;i<pages.length;i++){dhtml+='<div class="dot'+(i===idx?' active':'')+(gameDone[i]?' done':'')+'" onclick="goToPage('+i+')"></div>';}
  dots.innerHTML=dhtml;
  document.getElementById('prevBtn').disabled=(idx===0);
  document.getElementById('nextBtn').disabled=(idx===pages.length-1);
  document.getElementById('pageCounter').textContent='\u7B2C'+(idx+1)+'\u9875 / \u5171'+pages.length+'\u9875';
  document.getElementById('nextBtn').style.display=(idx===pages.length-1)?'none':'';
  currentPage=idx;
}

function prevPage(){if(currentPage>0)goToPage(currentPage-1);}
function nextPage(){if(currentPage<pages.length-1)goToPage(currentPage+1);}
function goToPage(idx){renderPage(idx);}

function speakPage() {
  var p=pages[currentPage];
  if(p.cover){showBubble('__SPEAK_TITLE__!');speakText('__SPEAK_TEXT__');return;}
  if(p.final){showBubble('You did it! Super English Star! \U0001f31f');speakText('You did it! Super English Star!');return;}
  if(p.match){showBubble('Listen to the words!');speakText('Listen to the words!');return;}
  var t=p.sentence.replace(/<[^>]+>/g,'');
  showBubble('\U0001f50a '+t);
  speakText(t);
}

function launchConfetti() {
  var d=document.createElement('div');d.className='celebration';
  var colors=['#FF6B6B','#FFB347','#4ECDC4','#FFE66D','#A78BFA','#FF9FF3'];
  for(var i=0;i<40;i++){var c=document.createElement('div');c.style.cssText='position:absolute;width:'+(6+Math.random()*8)+'px;height:'+(6+Math.random()*8)+'px;border-radius:50%;left:'+(Math.random()*100)+'%;top:10%;background:'+colors[i%6]+';animation:confetti-fall '+(1.5+Math.random())+'s ease-out forwards;animation-delay:'+(Math.random()*0.5)+'s;';d.appendChild(c);}
  document.body.appendChild(d);setTimeout(function(){d.remove()},3000);
}

document.addEventListener('keydown',function(e){
  if(e.key==='ArrowLeft') prevPage();
  if(e.key==='ArrowRight') nextPage();
});

renderPage(0);
</script>
</body>
</html>'''


def generate(song):
    song_id = song["id"]
    pages = song["pages"]
    emoji = song.get("emoji", "🎵")
    display_title = f"{emoji} {song['title']}"
    title_clean = re.sub(r'[^a-zA-Z\s]', '', song['title']).strip()
    n_pages = len(pages) + 3

    cover_svg = make_scene_svg(song["svg_element"], song["svg_bg"])

    # Build pages JS entries
    pages_js = []
    for p in pages:
        s = p["sentence"].replace("'", "\\'")
        d = p["desc"]
        g = p["game"]
        pages_js.append(f"  {{ sentence:'{s}', desc:'{d}', game:'{g}', svg:'0' }},")
    pages_js_str = "\n".join(pages_js)

    # Build scenes array
    scene_svgs = [make_scene_svg(song["svg_element"], song["svg_bg"]) for _ in pages]
    scenes_str = ",\n    ".join(f"`{s}`" for s in scene_svgs)

    # Build match words
    seen = set()
    for p in pages:
        if p["game"] and p["game"] not in seen:
            seen.add(p["game"])
    match_words = ",".join(f'"{w}"' for w in seen)

    html = TEMPLATE_HTML
    html = html.replace("__DISPLAY_TITLE__", display_title)
    html = html.replace("__TITLE__", f"{emoji} {song['title']}")
    html = html.replace("__COVER_SUBTITLE__", song["cover_subtitle"])
    html = html.replace("__PAGES_JS__", pages_js_str)
    html = html.replace("__SCENES__", scenes_str)
    html = html.replace("__MATCH_WORDS__", match_words)
    html = html.replace("__MP3FILE__", song["mp3"])
    html = html.replace("__COVER_SVG__", cover_svg)
    html = html.replace("__SPEAK_TITLE__", display_title)
    html = html.replace("__SPEAK_TEXT__", title_clean)
    html = html.replace("__CURRENT__", "1")
    html = html.replace("__TOTAL__", str(n_pages))

    outpath = os.path.join(OUT, f"{song_id}.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ {song_id}.html ({len(html)} bytes)")


# Generate all
for s in SONGS:
    generate(s)

print(f"\n🎉 生成了 {len(SONGS)} 个课件")
