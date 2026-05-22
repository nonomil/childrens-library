#!/usr/bin/env python3
"""Fix template escaping issues and regenerate"""
import re, os, json

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "docs/courseware")

# Read the template
with open(os.path.join(BASE, "template_nursery_v3.html"), "r") as f:
    template = f.read()

# Fix 1: word game - use data attributes instead of inline onclick with backslashes
old = "const tiles=letters.map(function(l){return '<div class=\"letter-tile\" draggable=\"true\" onclick=\"pickLetter('+idx+',\\\\''+l+'\\\\',this)\" ondragstart=\"onDragStart(event,'+idx+',\\\\''+l+'\\\\')\" ondragend=\"onDragEnd(event)\">'+l+'</div>';}).join('');"
new = "const tiles=letters.map(function(l){return '<div class=\"letter-tile\" draggable=\"true\" data-idx=\"'+idx+'\" data-letter=\"'+l+'\" onclick=\"pickTile(this)\" ondragstart=\"onDragStart(event,'+idx+',\"'+l+'\")\" ondragend=\"onDragEnd(event)\">'+l+'</div>';}).join('');"
template = template.replace(old, new)

# Fix 2: match game - use data-word already present
old2 = "return '<div class=\"word-choice\" data-word=\"'+w+'\" onclick=\"checkMatch(\\\\''+w+'\\\\',this)\" '+d+'>'+w+'</div>';"
new2 = "return '<div class=\"word-choice\" data-word=\"'+w+'\" onclick=\"checkMatchByData(this)\" '+d+'>'+w+'</div>';"
template = template.replace(old2, new2)

# Add the pickTile and checkMatchByData functions
template = template.replace(
    "function pickLetter(idx,letter,el) {",
    "function pickTile(el){pickLetter(parseInt(el.dataset.idx),el.dataset.letter,el);}\nfunction pickLetter(idx,letter,el) {"
)
template = template.replace(
    "function checkMatch(word,el) {",
    "function checkMatchByData(el){var w=el.dataset.word;if(w){checkMatch(w,el);}}\nfunction checkMatch(word,el) {"
)

# Also fix the ondragstart which has similar quoting issues
template = template.replace(
    'ondragstart=\"onDragStart(event,\'+idx+\',\"\'+l+\'\")\"',
    "ondragstart=\"onDragStart(event,'+idx+','\"+l+\"')\""
)
# Actually let me check what's in the template now
with open(os.path.join(BASE, "template_nursery_v3_fixed.html"), "w") as f:
    f.write(template)

print("Template fixed, saved to template_nursery_v3_fixed.html")

# Now read the data files
with open(os.path.join(BASE, "generate_courseware.py"), "r") as f:
    old_code = f.read()
with open(os.path.join(BASE, "generate_courseware_v3.py"), "r") as f:
    v3_code = f.read()

# Extract code sections
idx1 = old_code.find("def make_scene_svg")
idx2 = old_code.find("MELODIES = {")
idx3 = old_code.find("TEMPLATE_HTML")
idx4 = old_code.find("SONGS = [")
idx5 = old_code.find("def generate", idx4)

# From v3 file
iq = v3_code.find("QUIZ_DATA = {")
im = v3_code.find("MELODIES = {")
ii = v3_code.find("INTERACT_GAMES = {")

# Build combined code
code = ""
code += old_code[idx1:idx2]  # make_scene_svg
code += "\n" + v3_code[ii:iq]  # INTERACT_GAMES
code += "\n" + v3_code[iq:im]  # QUIZ_DATA
code += "\n" + old_code[idx2:idx3].replace('os.path.dirname(os.path.abspath(__file__))', 'BASE')  # MELODIES (but not TEMPLATE_HTML)
code += "\n" + old_code[idx4:idx5]  # SONGS

# Read new template
with open(os.path.join(BASE, "template_nursery_v3_fixed.html"), "r") as f:
    TEMPLATE = f.read()

# Execute the data code
ns = {}
exec(code, ns)
SONGS = ns.get("SONGS", [])
INTERACT_GAMES = ns.get("INTERACT_GAMES", {})
MELODIES = ns.get("MELODIES", {})
QUIZ_DATA = ns.get("QUIZ_DATA", {})
make_scene_svg = ns.get("make_scene_svg")

print(f"Loaded {len(SONGS)} songs, {len(INTERACT_GAMES)} interact games")

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
    
    melody_key = s.get("melody_key", sid)
    melody_func = MELODIES.get(melody_key, "function playMelody(){playNote(440,0.5);}")
    
    quiz_key = s.get("quiz_key", sid)
    qdata = QUIZ_DATA.get(quiz_key, [{"q":"Is this fun?","opts":["Yes!","No"],"ans":0,"feedback":"Learning is fun!"}])
    quiz_json = json.dumps(qdata, ensure_ascii=False)
    
    interact = INTERACT_GAMES.get(sid, {"title":"🎮 互动游戏","inst":"把物品拖到对应位置！","items":[]})
    interact_json = json.dumps(interact["items"], ensure_ascii=False)
    
    html = TEMPLATE
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

print(f"\n🎉 Generated {len(SONGS)} files!")
