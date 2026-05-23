#!/usr/bin/env python3
"""Generate all nursery rhyme courseware with drag-interactive games"""
import os, re, json, sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "docs/courseware")

# Read and execute the data definitions
with open(os.path.join(BASE, "generate_courseware_v3.py"), "r", encoding="utf-8") as f:
    data_code = f.read()

# Create a namespace dict and execute the data
ns = {"__file__": os.path.join(BASE, "generate_courseware_v3.py")}
exec(data_code, ns)
# Copy all names
for name in ns:
    if not name.startswith('_'):
        globals()[name] = ns[name]

print(f"  Loaded {len(SONGS)} songs, {len(INTERACT_GAMES)} interact games")

# Read the template
with open(os.path.join(BASE, "template_nursery_v3.html"), "r", encoding="utf-8") as f:
    TEMPLATE_HTML = f.read()

def generate(song):
    song_id = song["id"]
    pages = song["pages"]
    emoji = song.get("emoji", "🎵")
    display_title = f"{emoji} {song['title']}".replace("'", "\\'")
    title_clean = re.sub(r'[^a-zA-Z\\s]', '', song['title']).strip()
    sub_escaped = song["cover_subtitle"].replace("'", "\\'")
    n_pages = len(pages) + 5  # cover + pages + interact + match + quiz + final

    cover_svg = make_scene_svg(song["svg_element"], song["svg_bg"])

    # Build pages JS entries
    pages_js = []
    for p in pages:
        s = p["sentence"].replace("'", "\\'")
        d = p["desc"]
        g = p["game"] or ""
        pages_js.append(f"  {{ sentence:'{s}', desc:'{d}', game:'{g}', svg:'0' }},")
    pages_js_str = "\n".join(pages_js)

    scene_svgs = [make_scene_svg(song["svg_element"], song["svg_bg"]) for _ in pages]
    scenes_str = ",\n    ".join(f"`{s}`" for s in scene_svgs)

    # Match words
    seen = set()
    for p in pages:
        if p["game"] and p["game"] not in seen:
            seen.add(p["game"])
    match_words = ",".join(f'"{w}"' for w in seen)

    # Melody
    melody_key = song.get("melody_key", song_id)
    melody_func = MELODIES.get(melody_key, "function playMelody(){playNote(440,0.5);}")

    # Quiz data
    quiz_key = song.get("quiz_key", song_id)
    quiz_data_list = QUIZ_DATA.get(quiz_key, [{"q":"Is this fun?","opts":["Yes!","No"],"ans":0,"feedback":"Learning is fun!"}])
    quiz_data_json = json.dumps(quiz_data_list, ensure_ascii=False)

    # Interactive game data
    interact = INTERACT_GAMES.get(song_id, {"title":"🎮 互动游戏","inst":"把物品拖到对应位置！","items":[
        {"id":"a","emoji":"⭐","label":"A","zone":"位置1","target":"100,100"},
        {"id":"b","emoji":"⭐","label":"B","zone":"位置2","target":"250,100"},
    ]})
    interact_items_json = json.dumps(interact["items"], ensure_ascii=False)

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
    html = html.replace("__INTERACT_ITEMS__", interact_items_json)
    html = html.replace("__INTERACT_TITLE__", interact["title"])
    html = html.replace("__INTERACT_INST__", interact["inst"])
    html = html.replace("__TOTAL__", str(n_pages))

    outpath = os.path.join(OUT, f"{song_id}.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✅ {song_id}.html ({len(html)} bytes)")

if __name__ == "__main__":
    print(f"🎵 生成 {len(SONGS)} 个童谣互动课件 (v3 - drag game)...")
    for s in SONGS:
        generate(s)
    print(f"\n🎉 全部完成!")
