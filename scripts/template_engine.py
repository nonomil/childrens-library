#!/usr/bin/env python3
"""
TEMPLATE_CONFIG 系统 - 四个视觉变体
基于飞书调研报告的架构设计
"""
import os
import re
from pathlib import Path

# ===== 四个视觉变体（来自飞书报告）=====
VISUAL_VARIANTS = {
    "space": {
        "name": "太空冒险",
        "emoji": "🚀",
        "bg_gradient": "linear-gradient(135deg, #0B1026 0%, #1A1A3E 50%, #2D1B4E 100%)",
        "card_bg": "rgba(255,255,255,0.08)",
        "card_border": "rgba(100,200,255,0.2)",
        "primary": "#64B5F6",
        "primary_dark": "#42A5F5",
        "secondary": "#FFD54F",
        "text": "#E3F2FD",
        "text_light": "#90CAF9",
        "accent": "#FFD54F",
        "cover_emoji": "🪐",
        "decorations": ["⭐", "🌙", "☄️", "🌌"],
    },
    "forest": {
        "name": "森林动物",
        "emoji": "🌿",
        "bg_gradient": "linear-gradient(135deg, #1A3A2A 0%, #2D5A3D 50%, #3E7A4E 100%)",
        "card_bg": "rgba(255,255,255,0.1)",
        "card_border": "rgba(144,238,144,0.3)",
        "primary": "#81C784",
        "primary_dark": "#66BB6A",
        "secondary": "#FFCC80",
        "text": "#E8F5E9",
        "text_light": "#A5D6A7",
        "accent": "#FFCC80",
        "cover_emoji": "🍄",
        "decorations": ["🦋", "🌸", "🐿️", "🍃"],
    },
    "ocean": {
        "name": "海洋世界",
        "emoji": "🌊",
        "bg_gradient": "linear-gradient(135deg, #0A1628 0%, #0D2137 50%, #1A3A5C 100%)",
        "card_bg": "rgba(255,255,255,0.08)",
        "card_border": "rgba(100,200,255,0.25)",
        "primary": "#4FC3F7",
        "primary_dark": "#29B6F6",
        "secondary": "#FF8A65",
        "text": "#E1F5FE",
        "text_light": "#81D4FA",
        "accent": "#FF8A65",
        "cover_emoji": "🐠",
        "decorations": ["🐚", "🦀", "🐡", "🐙"],
    },
    "fairy": {
        "name": "童话城堡",
        "emoji": "🏰",
        "bg_gradient": "linear-gradient(135deg, #2A1B3D 0%, #3D2B5A 50%, #5C3D8A 100%)",
        "card_bg": "rgba(255,255,255,0.1)",
        "card_border": "rgba(200,150,255,0.3)",
        "primary": "#CE93D8",
        "primary_dark": "#BA68C8",
        "secondary": "#FFD54F",
        "text": "#F3E5F5",
        "text_light": "#CE93D8",
        "accent": "#FFD54F",
        "cover_emoji": "👑",
        "decorations": ["✨", "🌟", "💫", "🎀"],
    },
}

# 故事类型 → 视觉变体映射
STORY_TYPE_MAP = {
    "poem": "fairy",      # 古诗讲解 → 童话城堡
    "lesson": "space",    # 教案活动 → 太空冒险
    "english": "ocean",   # 英语故事 → 海洋世界
    "story": "forest",    # 绘本故事 → 森林动物
}

def get_variant(filename):
    """根据文件名判断视觉变体"""
    if filename.startswith("poem_"):
        return "fairy"
    elif filename.startswith("lesson_"):
        return "space"
    elif filename.startswith("english_"):
        return "ocean"
    else:
        return "forest"

def parse_story(filepath):
    """解析 Markdown 故事"""
    content = filepath.read_text(encoding='utf-8')
    lines = content.strip().split('\n')
    
    title = ""
    paragraphs = []
    current_para = []
    
    for line in lines:
        if line.startswith('# ') and not title:
            title = line[2:].strip()
        elif line.strip() == '---':
            if current_para:
                paragraphs.append('\n'.join(current_para))
                current_para = []
        elif line.strip():
            current_para.append(line)
    
    if current_para:
        paragraphs.append('\n'.join(current_para))
    
    return {'title': title, 'paragraphs': paragraphs, 'filename': filepath.stem}

def generate_html(story, variant_key):
    """基于视觉变体生成 HTML 课件"""
    v = VISUAL_VARIANTS[variant_key]
    emoji = get_emoji_for_story(story['title'], story['filename'])
    
    # 构建段落
    paras_html = ""
    for i, p in enumerate(story['paragraphs']):
        paras_html += f'<div class="para" style="animation-delay:{i*0.1}s"><p>{p}</p></div>\n'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>{story['title']} - {v['name']}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
body{{
  font-family:'Nunito','PingFang SC','Microsoft YaHei',sans-serif;
  background:{v['bg_gradient']};
  min-height:100dvh;padding:16px;color:{v['text']};
}}
.container{{max-width:480px;margin:0 auto}}
.cover{{
  background:{v['card_bg']};border:1px solid {v['card_border']};
  border-radius:24px;padding:32px 24px;text-align:center;
  box-shadow:0 8px 40px rgba(0,0,0,.3);margin-bottom:16px;
  backdrop-filter:blur(10px);animation:fadeInUp .6s ease-out;
}}
.cover-deco{{font-size:24px;letter-spacing:16px;margin-bottom:8px;opacity:.6}}
.cover-emoji{{font-size:72px;margin-bottom:12px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.3))}}
.cover-title{{
  font-size:28px;font-weight:800;color:{v['primary']};
  margin-bottom:6px;text-shadow:0 2px 8px rgba(0,0,0,.2);
}}
.cover-sub{{font-size:14px;color:{v['text_light']};margin-bottom:20px}}
.start-btn{{
  background:{v['primary']};color:#fff;border:none;padding:12px 32px;
  border-radius:24px;font-size:16px;font-weight:700;cursor:pointer;
  box-shadow:0 4px 16px rgba(0,0,0,.3);transition:all .2s;
}}
.start-btn:active{{transform:scale(.95)}}
.section{{
  background:{v['card_bg']};border:1px solid {v['card_border']};
  border-radius:20px;padding:24px 20px;
  box-shadow:0 4px 20px rgba(0,0,0,.2);margin-bottom:16px;
  backdrop-filter:blur(10px);display:none;
}}
.section.active{{display:block;animation:fadeInUp .5s ease-out}}
.section-title{{
  font-size:18px;font-weight:700;color:{v['primary']};
  margin-bottom:16px;display:flex;align-items:center;gap:8px;
}}
.para{{
  background:rgba(255,255,255,.05);border-radius:12px;padding:16px;
  margin-bottom:12px;border-left:4px solid {v['primary']};
  animation:fadeIn .4s ease-out both;
}}
.para p{{font-size:15px;line-height:1.8;color:{v['text']}}
.quiz-q{{margin-bottom:16px}}
.quiz-q p{{font-size:14px;font-weight:600;margin-bottom:8px}}
.quiz-opt{{
  background:rgba(255,255,255,.08);border:1px solid {v['card_border']};
  border-radius:10px;padding:10px 14px;font-size:13px;
  cursor:pointer;transition:all .2s;margin-bottom:6px;display:block;width:100%;text-align:left;color:{v['text']};
}}
.quiz-opt:hover{{border-color:{v['primary']}}}
.quiz-opt.correct{{background:rgba(76,175,80,.2);border-color:#4CAF50}}
.quiz-opt.wrong{{background:rgba(244,67,54,.2);border-color:#EF5350}}
.btn-row{{display:flex;gap:8px;margin-top:16px;justify-content:center;flex-wrap:wrap}}
.btn{{
  background:{v['primary']};color:#fff;border:none;padding:10px 20px;
  border-radius:16px;font-size:13px;font-weight:700;cursor:pointer;
}}
.btn-sec{{background:transparent;border:2px solid {v['primary']};color:{v['primary']}}}
.back-btn{{
  display:block;width:100%;background:{v['secondary']};color:#fff;
  border:none;padding:14px;border-radius:16px;font-size:16px;
  font-weight:700;cursor:pointer;text-decoration:none;text-align:center;
  margin-bottom:16px;
}}
.read-btn{{
  position:fixed;bottom:24px;right:24px;width:56px;height:56px;
  border-radius:50%;background:{v['primary']};color:#fff;border:none;
  font-size:24px;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.4);z-index:100;
}}
.read-btn.speaking{{animation:pulse 1s infinite}}
@keyframes fadeInUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(255,255,255,.4)}}50%{{box-shadow:0 0 0 12px rgba(255,255,255,0)}}}}
</style>
</head>
<body>
<div class="container">
  <div class="cover" id="cover">
    <div class="cover-deco">{' '.join(v['decorations'])}</div>
    <div class="cover-emoji">{emoji}</div>
    <h1 class="cover-title">{story['title']}</h1>
    <p class="cover-sub">{v['name']} · 适合 4-8 岁</p>
    <button class="start-btn" onclick="startStory()">🚀 开始阅读</button>
  </div>
  <div class="section" id="story">
    {paras_html}
    <div class="btn-row">
      <button class="btn" onclick="showQuiz()">🎯 小测验</button>
      <button class="btn btn-sec" onclick="showSummary()">📚 总结</button>
    </div>
  </div>
  <div class="section" id="quiz">
    <div class="section-title">🎯 小测验</div>
    <div class="quiz-q"><p>1. 故事里的主角做了什么？</p>
      <button class="quiz-opt" onclick="check(this,false)">选项A</button>
      <button class="quiz-opt" onclick="check(this,true)">选项B ✅</button>
      <button class="quiz-opt" onclick="check(this,false)">选项C</button>
    </div>
    <div class="quiz-q"><p>2. 这个故事告诉我们什么？</p>
      <button class="quiz-opt" onclick="check(this,true)">坚持就是胜利 ✅</button>
      <button class="quiz-opt" onclick="check(this,false)">放弃也没关系</button>
    </div>
  </div>
  <div class="section" id="summary">
    <div class="section-title">📚 知识总结</div>
    <div class="para"><p><strong>故事道理：</strong>每个故事都教会我们一个道理。坚持、勇敢、善良、好奇...这些品质让我们的世界更美好！</p></div>
  </div>
  <a href="../docs/index.html" class="back-btn">🏠 返回绘本首页</a>
</div>
<button class="read-btn" id="readBtn" onclick="toggleRead()">🔊</button>
<script>
let speaking=false;
function toggleRead(){{
  if(speaking){{window.speechSynthesis.cancel();speaking=false;document.getElementById('readBtn').classList.remove('speaking')}}
  else{{const t=document.getElementById('story').innerText;const u=new SpeechSynthesisUtterance(t);u.lang='zh-CN';u.rate=0.9;u.onend=()=>{{speaking=false;document.getElementById('readBtn').classList.remove('speaking')}};window.speechSynthesis.speak(u);speaking=true;document.getElementById('readBtn').classList.add('speaking')}}
}}
function startStory(){{document.getElementById('cover').style.display='none';document.querySelectorAll('.section').forEach(s=>s.classList.add('active'))}}
function showQuiz(){{document.getElementById('quiz').scrollIntoView({{behavior:'smooth'}})}}
function showSummary(){{document.getElementById('summary').scrollIntoView({{behavior:'smooth'}})}}
function check(btn,ok){{
  btn.parentElement.querySelectorAll('.quiz-opt').forEach(b=>b.disabled=true);
  btn.classList.add(ok?'correct':'wrong');
  if(!ok)btn.textContent+=' ❌';
}}
</script>
</body>
</html>'''
    return html

def get_emoji_for_story(title, filename):
    """根据标题选择emoji"""
    emoji_map = {
        '小蜗牛':'🐌','石头':'🪨','圣诞':'🎄','美人鱼':'🧜‍♀️','时间':'⏰',
        '彩虹':'🌈','大象':'🐘','兔子':'🐰','图书馆':'📚','太空':'🚀',
        '小兔子':'🐰','小青蛙':'🐸','小猴子':'🐵','小猫':'🐱','小蚂蚁':'🐜',
        '小熊':'🐻','小松鼠':'🐿️','小鸟':'🐦','小狐狸':'🦊','小猪':'🐷',
        '星星':'⭐','月亮':'🌙','云朵':'☁️','河水':'💧','种子':'🌱',
        '春天':'🌸','夏天':'☀️','秋天':'🍂','冬天':'❄️','小蜜蜂':'🐝',
        'Tortoise':'🐢','Lion':'🦁','Duckling':'🦆','Wolf':'🐺','Pigs':'🐷',
        'Bears':'🐻','Ant':'🐜','Hare':'🐇','Beanstalk':'🌿',
        '鹿柴':'🦌','春晓':'🌸','静夜思':'🌙','相思':'❤️','竹里馆':'🎋',
        '送别':'👋','田园乐':'🌾','辋川':'🏡','辛夷坞':'🌺','漆园':'🌳',
        '咏鹅':'🦆','悯农':'🌾','登鹳雀楼':'🏔️','望庐山瀑布':'💦',
        '江雪':'❄️','游子吟':'👩‍👦','鸟鸣涧':'🐦','杂诗':'📜','书事':'📖',
        '数学':'📐','科学':'🔬','艺术':'🎨','语言':'📝','体育':'⚽',
        '音乐':'🎵','户外':'🌿','社会':'👥','健康':'💪','创意':'💡',
    }
    for k,e in emoji_map.items():
        if k in title or k in filename:
            return e
    return '📖'

def main():
    print("=== TEMPLATE_CONFIG 四变体课件生成 ===\n")
    
    stories_dir = Path("/home/deploy/childrens-library/stories")
    output_dir = Path("/home/deploy/childrens-library/courseware")
    output_dir.mkdir(exist_ok=True)
    
    stories = sorted(stories_dir.glob("*.md"))
    print(f"找到 {len(stories)} 个故事\n")
    
    counts = {"space":0, "forest":0, "ocean":0, "fairy":0}
    
    for i, sf in enumerate(stories):
        try:
            story = parse_story(sf)
            variant = get_variant(sf.name)
            html = generate_html(story, variant)
            
            # 生成输出文件名
            parts = sf.stem.split("_", 2)
            if len(parts) >= 3:
                idx = parts[1] if parts[1].isdigit() else f"{i+1:02d}"
                name = parts[2] if len(parts) > 2 else parts[-1]
                out_name = f"{parts[0]}-{idx}-{name}.html"
            else:
                out_name = f"{sf.stem}.html"
            
            out_file = output_dir / out_name
            out_file.write_text(html, encoding='utf-8')
            counts[variant] += 1
            
            print(f"[{i+1:02d}/{len(stories)}] {VISUAL_VARIANTS[variant]['emoji']} {variant:8s} | {story['title'][:20]} → {out_name}")
        except Exception as e:
            print(f"[{i+1:02d}/{len(stories)}] ❌ {sf.name}: {e}")
    
    print(f"\n=== 完成 ===")
    print(f"太空冒险: {counts['space']} | 森林动物: {counts['forest']} | 海洋世界: {counts['ocean']} | 童话城堡: {counts['fairy']}")

if __name__ == "__main__":
    main()
