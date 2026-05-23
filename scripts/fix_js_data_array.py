#!/usr/bin/env python3
"""
Fix js-data-array and unknown type coursewares by modifying their JS render function.
"""
import re, os

CHILDRENS_LIB = "/home/deploy/childrens-library"

files = {
    "math-13-numbers100": {
        "img_path": "images/math-13-numbers100/webp",
        "count": 8,
        "type": "js-data-array"
    },
    "math-14-addsub2digit": {
        "img_path": "images/math-14-addsub2digit/webp",
        "count": 8,
        "type": "js-data-array"
    },
    "math-15-money": {
        "img_path": "images/math-15-money/webp",
        "count": 8,
        "type": "js-data-array"
    },
    "math-16-clock": {
        "img_path": "images/math-16-clock/webp",
        "count": 8,
        "type": "js-data-array"
    },
    "math-18-sorting": {
        "img_path": "images/math-18-sorting/webp",
        "count": 8,
        "type": "js-data-array"
    },
}

for name, cfg in files.items():
    path = os.path.join(CHILDRENS_LIB, "courseware", f"{name}.html")
    if not os.path.exists(path):
        print(f"❌ {name}.html not found")
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # For js-data-array: add image before text in render function
    # Find the else block where text/content pages are rendered
    # Pattern: }else{\n    h=`<div class="slide active" ... <h3>${p.title}</h3>` + ...
    
    img_line = f'if(p.text||p.items||p.svg){{h+=`<div style="text-align:center;margin-bottom:10px"><img src="{cfg["img_path"]}/page-${{String(n+1).padStart(2,\\"0\\")}}.webp" style="max-width:100%;border-radius:14px" loading="lazy" alt="配图"></div>`;}}\n    '
    
    # Find the else block in render function
    # Look for: }else{\n    h=`<div class="slide active" style="gap:6px">
    target = '}else{\n    h=`<div class="slide active" style="gap:6px"><h3 style="font-size:18px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.15)">${p.title}</h3>`;'
    
    if target in html:
        # Insert img_line AFTER the target (after ${p.title}</h3>`;)
        insert_pos = html.index(target) + len(target)
        html = html[:insert_pos] + '\n    ' + img_line + html[insert_pos:]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ {name}: image insertion added to render function")
    else:
        print(f"❌ {name}: target pattern not found")
        # Debug: show the actual pattern around the else block
        idx = html.find('}else{')
        if idx >= 0:
            print(f"   Found else at pos {idx}: {html[idx:idx+200]}")

print("\nDone!")
