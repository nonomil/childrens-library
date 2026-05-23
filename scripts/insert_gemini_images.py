#!/usr/bin/env python3
"""
Batch script v3: Insert Gemini images from bilingual-picturebooks.
Fixed: zero-padded page numbers, math chapters 13+ alt path.
"""

import os, re, subprocess, shutil

CHILDRENS_LIB = "/home/deploy/childrens-library"
BPB = "/home/deploy/bilingual-picturebooks"
MATH_IMG = f"{BPB}/math-kindergarten/images"

# All 18 coursewares that need images
CHAPTER_MAP = {
    "english-02-abc": {
        "src": f"{BPB}/english/chapters/img/chapter-02",
        "count": 15,
    },
    "chinese-01-characters": {
        "src": f"{BPB}/chinese-language/chapters/img/chapter-01",
        "count": 17,
    },
    "chinese-02-strokes": {
        "src": f"{BPB}/chinese-language/chapters/img/chapter-02",
        "count": 17,
    },
    "chinese-14-colors": {
        "src": f"{BPB}/chinese-language/chapters/img/chapter-14",
        "count": 17,
    },
    "math-01-counting": {
        "src": f"{MATH_IMG}/chapter-01",
        "count": 27,
    },
    "math-02-counting-11to20": {
        "src": f"{MATH_IMG}/chapter-02",
        "count": 29,
    },
    "math-13-numbers100": {
        "src": f"{MATH_IMG}/chapter-13",
        "count": 29,
    },
    "math-14-addsub2digit": {
        "src": f"{MATH_IMG}/chapter-14",
        "count": 29,
    },
    "math-15-money": {
        "src": f"{MATH_IMG}/chapter-15",
        "count": 29,
    },
    "math-16-clock": {
        "src": f"{MATH_IMG}/chapter-16",
        "count": 29,
    },
    "math-17-shapes": {
        "src": f"{MATH_IMG}/chapter-17",
        "count": 29,
    },
    "math-18-sorting": {
        "src": f"{MATH_IMG}/chapter-18",
        "count": 29,
    },
    "math-19-statistics": {
        "src": f"{MATH_IMG}/chapter-19",
        "count": 29,
    },
    "math-20-direction": {
        "src": f"{MATH_IMG}/chapter-20",
        "count": 29,
    },
    "math-21-multiplication": {
        "src": f"{MATH_IMG}/chapter-21",
        "count": 29,
    },
    "math-22-fractions": {
        "src": f"{MATH_IMG}/chapter-22",
        "count": 29,
    },
    "math-23-word-problems": {
        "src": f"{MATH_IMG}/chapter-23",
        "count": 29,
    },
    "math-24-carnival": {
        "src": f"{MATH_IMG}/chapter-24",
        "count": 29,
    },
}

def zero_pad(p):
    """Zero-pad numbers: 1 → 01, 10 → 10, '07a' → '07a'"""
    s = str(p)
    try:
        n = int(s)
        return f"{n:02d}"
    except ValueError:
        return s

def copy_and_convert(name, cfg):
    src_dir = cfg["src"]
    if not os.path.isdir(src_dir):
        print(f"  ❌ Source missing: {src_dir}")
        return []
    
    img_dir = os.path.join(CHILDRENS_LIB, "courseware", "images", name, "webp")
    os.makedirs(img_dir, exist_ok=True)
    
    converted = []
    for i in range(1, cfg["count"] + 1):
        p_str = zero_pad(i)
        src_png = os.path.join(src_dir, f"page-{p_str}.png")
        dst_webp = os.path.join(img_dir, f"page-{p_str}.webp")
        
        if os.path.exists(src_png):
            if os.path.exists(dst_webp):
                print(f"  ✅ page-{p_str}.webp (cached)")
            elif shutil.which("cwebp"):
                r = subprocess.run(["cwebp", "-q", "80", src_png, "-o", dst_webp],
                                  capture_output=True, timeout=30)
                if r.returncode == 0:
                    kb = os.path.getsize(dst_webp) // 1024
                    print(f"  ✅ page-{p_str}.webp ({kb}KB)")
                else:
                    print(f"  ⚠️  page-{p_str}.png convert error")
                    continue
            else:
                print(f"  ⚠️  No cwebp, skipping convert")
                continue
            converted.append(p_str)
        # Skip silently if file doesn't exist (gaps in numbering are normal)
    
    return converted


def classify(html):
    """Classify HTML structure."""
    if re.search(r'render\s*:\s*`', html):
        return "render-literal"
    if re.search(r'class="[^"]*slide[^"]*"', html) and re.search(r'data-page="', html):
        return "slides"
    if re.search(r'class="page[^"]*"', html) and re.search(r'data-page="', html):
        return "html-divs"
    m = re.search(r'const\s+pages\s*=\s*\[', html)
    if m:
        return "js-data-array"
    return "unknown"


def insert_into_html(html, name, pages):
    """
    Universal insertion: find each <div class="page...data-page="X""> or 
    <div class="slide...data-page="X""> and insert image after the first heading.
    If no heading, insert after the opening div tag.
    """
    changes = 0
    pattern = re.compile(r'(<(?:div)[^>]*class="[^"]*(?:page|slide)[^"]*"[^>]*data-page="(\d+)"[^>]*>)')
    
    # Process in REVERSE order so insertions don't shift earlier positions
    matches = list(pattern.finditer(html))
    matches.reverse()
    
    for m in matches:
        p_idx = int(m.group(2))
        p_str = zero_pad(p_idx + 1)
        
        if p_str not in pages:
            continue
        
        after_tag = html[m.end():m.end()+600]
        heading = re.search(r'<(?:h[1-6]|div[^>]*class="[^"]*title[^"]*")[^>]*>', after_tag)
        
        insert_pos = m.end() + (heading.end() if heading else 0)
        
        img = (f'<div style="text-align:center;margin-bottom:10px;">'
               f'<img src="images/{name}/webp/page-{p_str}.webp" '
               f'style="max-width:100%;border-radius:14px;" loading="lazy" alt="courseware illustration"></div>\n      ')
        
        html = html[:insert_pos] + img + html[insert_pos:]
        changes += 1
    
    return html, changes


def main():
    os.chdir(CHILDRENS_LIB)
    total_ok = 0
    
    for name, cfg in sorted(CHAPTER_MAP.items()):
        html_path = os.path.join(CHILDRENS_LIB, "courseware", f"{name}.html")
        if not os.path.exists(html_path):
            print(f"\n❌ {name}.html not found")
            continue
        
        print(f"\n{'='*60}")
        print(f"📁 {name}")
        print(f"{'='*60}")
        
        # 1. Copy & convert
        converted = copy_and_convert(name, cfg)
        if not converted:
            print(f"  ⚠️  No images found at {cfg['src']}")
            continue
        
        # 2. Read & classify
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        struct = classify(html)
        print(f"  📄 Type: {struct}")
        
        if struct == "render-literal":
            print(f"  ⏭️  render-literal (already done)")
            total_ok += 1
            continue
        
        if struct == "unknown":
            print(f"  ⏭️  unknown structure, skipping")
            continue
        
        # 3. Insert
        html, changes = insert_into_html(html, name, set(converted))
        
        if changes > 0:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✅ {changes} images inserted into HTML")
            total_ok += 1
        else:
            print(f"  ⚠️  0 images inserted (page structure mismatch)")
    
    print(f"\n{'='*60}")
    print(f"📊 Done: {total_ok} coursewares updated")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
