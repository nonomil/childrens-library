#!/usr/bin/env python3
"""Generate courseware - simple approach"""
import os, json, re, importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "docs/courseware")

# Read template
with open(os.path.join(BASE, "template_nursery_v3_fixed.html"), "r") as f:
    TPL = f.read()

# Import make_scene_svg from generate_courseware
spec = importlib.util.spec_from_file_location("gw", os.path.join(BASE, "generate_courseware.py"))
gw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw)
make_scene_svg = gw.make_scene_svg

# Import data from generate_courseware_v3
spec2 = importlib.util.spec_from_file_location("v3", os.path.join(BASE, "generate_courseware_v3.py"))
v3 = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(v3)
INTERACT_GAMES = v3.INTERACT_GAMES
QUIZ_DATA = v3.QUIZ_DATA
MELODIES = v3.MELODIES

SONGS = [
    {"id":"wheels-on-bus","title":"The Wheels on the Bus","emoji":"🚌","mp3":"wheels.mp3","cover_subtitle":"✏️ 公车的轮子转啊转！","pages":[
        {"sentence":'The <span class="hl" data-word="wheels">wheels</span> on the bus go <span class="hl" data-word="round">round</span> and <span class="hl" data-word="round">round</span>',"desc":"公车的轮子转啊转","game":"wheels"},
        {"sentence":'The <span class="hl" data-word="people">people</span> on the bus go <span class="hl" data-word="up">up</span> and <span class="hl" data-word="down">down</span>',"desc":"公车的人们上上下下","game":"people"},
        {"sentence":'The <span class="hl" data-word="wipers">wipers</span> on the bus go <span class="hl" data-word="swish">swish</span> swish swish',"desc":"公车的雨刷刷刷刷","game":"wipers"},
        {"sentence":'The <span class="hl" data-word="horn">horn</span> on the bus goes <span class="hl" data-word="beep">beep</span> beep beep',"desc":"公车的喇叭哔哔哔","game":"horn"},
        {"sentence":'The <span class="hl" data-word="door">door</span> on the bus goes <span class="hl" data-word="open">open</span> and <span class="hl" data-word="shut">shut</span>',"desc":"公车的门开了关","game":"door"},
    ],"svg_bg":"#87CEEB,#E0F7FA","svg_element":"bus"},
    {"id":"itsy-bitsy-spider","title":"Itsy Bitsy Spider","emoji":"🕷️","mp3":"itsybitsy.mp3","cover_subtitle":"✏️ 小蜘蛛爬水管！","pages":[
        {"sentence":'The <span class="hl" data-word="itsy">itsy</span> <span class="hl" data-word="bitsy">bitsy</span> <span class="hl" data-word="spider">spider</span> went up the water <span class="hl" data-word="spout">spout</span>',"desc":"小蜘蛛爬上了水管","game":"spider"},
        {"sentence":'Down came the <span class="hl" data-word="rain">rain</span> and washed the spider <span class="hl" data-word="out">out</span>',"desc":"下雨了把蜘蛛冲出来","game":"rain"},
        {"sentence":'Out came the <span class="hl" data-word="sun">sun</span> and dried up all the <span class="hl" data-word="rain">rain</span>',"desc":"太阳出来晒干了雨水","game":"sun"},
        {"sentence":'And the itsy bitsy spider went up the spout <span class="hl" data-word="again">again</span>',"desc":"小蜘蛛又爬上了水管","game":"again"},
    ],"svg_bg":"#A5D6A7,#C8E6C9","svg_element":"spider"},
    {"id":"bingo","title":"BINGO","emoji":"🐶","mp3":"bingo.mp3","cover_subtitle":"✏️ 农夫有一只小狗叫BINGO！","pages":[
        {"sentence":'There was a <span class="hl" data-word="farmer">farmer</span> had a <span class="hl" data-word="dog">dog</span>',"desc":"农夫有一只小狗","game":"farmer"},
        {"sentence":'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o',"desc":"Bingo是它的名字","game":"bingo"},
        {"sentence":'B-I-N-G-O, <span class="hl" data-word="B">B</span>-<span class="hl" data-word="I">I</span>-<span class="hl" data-word="N">N</span>-<span class="hl" data-word="G">G</span>-<span class="hl" data-word="O">O</span>',"desc":"拼出BINGO的名字","game":"bingo"},
        {"sentence":'And <span class="hl" data-word="Bingo">Bingo</span> was his <span class="hl" data-word="name">name</span>-o!',"desc":"Bingo就是它的名字！","game":"name"},
    ],"svg_bg":"#FFE0B2,#FFF3E0","svg_element":"dog"},
    {"id":"abc-song","title":"ABC Song","emoji":"🔤","mp3":"abcsong.mp3","cover_subtitle":"✏️ 一起来学英文字母歌！","pages":[
        {"sentence":'<span class="hl" data-word="A">A</span>-<span class="hl" data-word="B">B</span>-<span class="hl" data-word="C">C</span>-<span class="hl" data-word="D">D</span>-<span class="hl" data-word="E">E</span>-<span class="hl" data-word="F">F</span>-<span class="hl" data-word="G">G</span>',"desc":"字母ABCDEFG","game":"abcdefg"},
        {"sentence":'<span class="hl" data-word="H">H</span>-<span class="hl" data-word="I">I</span>-<span class="hl" data-word="J">J</span>-<span class="hl" data-word="K">K</span>-<span class="hl" data-word="L">L</span>-<span class="hl" data-word="M">M</span>-<span class="hl" data-word="N">N</span>-<span class="hl" data-word="O">O</span>-<span class="hl" data-word="P">P</span>',"desc":"字母HIJKLMNOP","game":"hijklmnop"},
        {"sentence":'<span class="hl" data-word="Q">Q</span>-<span class="hl" data-word="R">R</span>-<span class="hl" data-word="S">S</span>-<span class="hl" data-word="T">T</span>-<span class="hl" data-word="U">U</span>-<span class="hl" data-word="V">V</span>',"desc":"字母QRSTUV","game":"qrstuv"},
        {"sentence":'<span class="hl" data-word="W">W</span>-<span class="hl" data-word="X">X</span>-<span class="hl" data-word="Y">Y</span>-<span class="hl" data-word="Z">Z</span>',"desc":"字母WXYZ","game":"wxyz"},
        {"sentence":'Now I know my <span class="hl" data-word="ABC">ABC</span>s, sing with <span class="hl" data-word="me">me</span>!',"desc":"我会唱字母歌了！","game":"abcs"},
    ],"svg_bg":"#E8EAF6,#C5CAE9","svg_element":"abc"},
    {"id":"head-shoulders","title":"Head Shoulders Knees &amp; Toes","emoji":"🧍","mp3":"headshoulders.mp3","cover_subtitle":"✏️ 一起来认识身体部位！","pages":[
        {"sentence":'<span class="hl" data-word="Head">Head</span>, <span class="hl" data-word="shoulders">shoulders</span>, <span class="hl" data-word="knees">knees</span> and <span class="hl" data-word="toes">toes</span>',"desc":"头肩膀膝盖和脚趾","game":"head"},
        {"sentence":'<span class="hl" data-word="Eyes">Eyes</span> and <span class="hl" data-word="ears">ears</span> and <span class="hl" data-word="mouth">mouth</span> and <span class="hl" data-word="nose">nose</span>',"desc":"眼睛耳朵嘴巴和鼻子","game":"eyes"},
        {"sentence":'<span class="hl" data-word="Head">Head</span>, <span class="hl" data-word="shoulders">shoulders</span>, <span class="hl" data-word="knees">knees</span> and <span class="hl" data-word="toes">toes</span>',"desc":"我们再来一遍！","game":"knees"},
        {"sentence":'<span class="hl" data-word="Eyes">Eyes</span> and <span class="hl" data-word="ears">ears</span> and <span class="hl" data-word="mouth">mouth</span> and <span class="hl" data-word="nose">nose</span>',"desc":"我们都认识身体部位啦！","game":"mouth"},
    ],"svg_bg":"#FFF8E1,#FFECB3","svg_element":"star"},
    {"id":"humpty-dumpty","title":"Humpty Dumpty","emoji":"🥚","mp3":"humptydumpty.mp3","cover_subtitle":"✏️ 蛋头先生坐在墙头上！","pages":[
        {"sentence":'<span class="hl" data-word="Humpty">Humpty</span> <span class="hl" data-word="Dumpty">Dumpty</span> sat on a <span class="hl" data-word="wall">wall</span>',"desc":"蛋头先生坐在墙头上","game":"humpty"},
        {"sentence":'Humpty Dumpty had a <span class="hl" data-word="great">great</span> <span class="hl" data-word="fall">fall</span>',"desc":"蛋头先生摔了一大跤","game":"great"},
        {"sentence":'All the <span class="hl" data-word="king">king</span> horses and all the king men',"desc":"国王所有的马和士兵","game":"king"},
        {"sentence":'Couldn put Humpty together <span class="hl" data-word="again">again</span>',"desc":"都没法把蛋头拼回去","game":"again"},
    ],"svg_bg":"#E3F2FD,#BBDEFB","svg_element":"egg"},
    {"id":"if-youre-happy","title":"If You're Happy","emoji":"😊","mp3":"if_happy.mp3","cover_subtitle":"✏️ 如果你开心你就拍拍手！","pages":[
        {"sentence":'If you happy and you <span class="hl" data-word="know">know</span> it, <span class="hl" data-word="clap">clap</span> your <span class="hl" data-word="hands">hands</span>!',"desc":"如果你开心就拍拍手","game":"happy"},
        {"sentence":'If you happy and you know it, <span class="hl" data-word="stomp">stomp</span> your <span class="hl" data-word="feet">feet</span>!',"desc":"如果你开心就跺跺脚","game":"stomp"},
        {"sentence":'If you happy and you know it, <span class="hl" data-word="shout">shout</span> Hurray!',"desc":"如果你开心就喊Hurray","game":"shout"},
        {"sentence":'If you happy and you know it, do <span class="hl" data-word="all">all</span> <span class="hl" data-word="three">three</span>!',"desc":"如果你开心就全做一遍","game":"three"},
    ],"svg_bg":"#FFF9C4,#FFF59D","svg_element":"happy"},
    {"id":"london-bridge","title":"London Bridge","emoji":"🌉","mp3":"london_bridge.mp3","cover_subtitle":"✏️ 伦敦桥要倒啦！","pages":[
        {"sentence":'<span class="hl" data-word="London">London</span> <span class="hl" data-word="Bridge">Bridge</span> is <span class="hl" data-word="falling">falling</span> <span class="hl" data-word="down">down</span>',"desc":"伦敦桥要倒了","game":"london"},
        {"sentence":'London Bridge is falling down, my <span class="hl" data-word="fair">fair</span> <span class="hl" data-word="lady">lady</span>',"desc":"伦敦桥要倒了，我美丽的淑女","game":"fair"},
        {"sentence":'<span class="hl" data-word="Build">Build</span> it <span class="hl" data-word="up">up</span> with <span class="hl" data-word="iron">iron</span> <span class="hl" data-word="bars">bars</span>',"desc":"用铁棍把桥修好","game":"build"},
        {"sentence":'Iron bars will <span class="hl" data-word="bend">bend</span> and <span class="hl" data-word="break">break</span>',"desc":"铁棍也会弯会断","game":"break"},
    ],"svg_bg":"#E0F7FA,#B2EBF2","svg_element":"bridge"},
    {"id":"mary-lamb","title":"Mary Had a Little Lamb","emoji":"🐑","mp3":"mary_lamb.mp3","cover_subtitle":"✏️ 玛丽有一只小羊羔！","pages":[
        {"sentence":'<span class="hl" data-word="Mary">Mary</span> had a <span class="hl" data-word="little">little</span> <span class="hl" data-word="lamb">lamb</span>',"desc":"玛丽有只小羊羔","game":"mary"},
        {"sentence":'Mary had a little lamb, its <span class="hl" data-word="fleece">fleece</span> was white as <span class="hl" data-word="snow">snow</span>',"desc":"羊毛白如雪","game":"fleece"},
        {"sentence":'And everywhere that Mary went, the <span class="hl" data-word="lamb">lamb</span> was sure to <span class="hl" data-word="go">go</span>',"desc":"玛莉走到哪羊羔就跟到哪","game":"lamb"},
        {"sentence":'It <span class="hl" data-word="followed">followed</span> her to school one day',"desc":"有一天它跟着去了学校","game":"followed"},
    ],"svg_bg":"#F3E5F5,#E1BEE7","svg_element":"lamb"},
]

print(f"Loaded {len(SONGS)} songs")
print(f"  make_scene_svg: {'ok' if 'make_scene_svg' in dir() else 'MISSING'}")
print(f"  INTERACT_GAMES: {len(INTERACT_GAMES)}, QUIZ_DATA: {len(QUIZ_DATA)}, MELODIES: {len(MELODIES)}")

for s in SONGS:
    sid = s["id"]
    pages = s["pages"]
    emoji = s.get("emoji", "🎵")
    title = f"{emoji} {s['title']}".replace("'", "\\'")
    title_clean = re.sub(r'[^a-zA-Z\s]', '', s['title']).strip()
    sub = s["cover_subtitle"].replace("'", "\\'")
    n_pages = len(pages) + 5
    cover_svg = make_scene_svg(s["svg_element"], s["svg_bg"])
    
    pages_js_lines = []
    for p in pages:
        sen = p["sentence"].replace("'", "\\'")
        pages_js_lines.append(f"  {{ sentence:'{sen}', desc:'{p['desc']}', game:'{p['game'] or ''}', svg:'0' }},")
    pages_js = "\n".join(pages_js_lines)
    scenes_str = ",\n    ".join(f"`{make_scene_svg(s['svg_element'], s['svg_bg'])}`" for _ in pages)
    
    seen = set()
    for p in pages:
        if p["game"] and p["game"] not in seen: seen.add(p["game"])
    match_words = ",".join(f'"{w}"' for w in seen)
    
    melody_func = MELODIES.get(sid, "function playMelody(){playNote(440,0.5);}")
    
    qdata = QUIZ_DATA.get(sid, [{"q":"Is this fun?","opts":["Yes!","No"],"ans":0,"feedback":"Learning is fun!"}])
    quiz_json = json.dumps(qdata, ensure_ascii=False)
    
    interact = INTERACT_GAMES.get(sid, {"title":"🎮 互动游戏","inst":"把物品拖到对应位置！","items":[]})
    interact_json = json.dumps(interact["items"], ensure_ascii=False)
    
    html = TPL
    for old, new in [
        ("__DISPLAY_TITLE__", title),
        ("__TITLE__", f"{emoji} {s['title']}"),
        ("__COVER_SUBTITLE__", sub),
        ("__PAGES_JS__", pages_js),
        ("__SCENES__", scenes_str),
        ("__MATCH_WORDS__", match_words),
        ("__MP3FILE__", s["mp3"]),
        ("__COVER_SVG__", cover_svg),
        ("__SPEAK_TITLE__", title),
        ("__SPEAK_TEXT__", title_clean),
        ("__SONG_MELODY__", melody_func),
        ("__QUIZ_DATA__", quiz_json),
        ("__INTERACT_ITEMS__", interact_json),
        ("__INTERACT_TITLE__", interact["title"]),
        ("__INTERACT_INST__", interact["inst"]),
        ("__TOTAL__", str(n_pages)),
    ]:
        html = html.replace(old, new)
    
    path = os.path.join(OUT, f"{sid}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {sid}.html ({len(html)} bytes)")

print(f"\n🎉 Done!")
