#!/usr/bin/env python3
"""
Convert 27 coursewares to unified navigation.
Fixes per OpenCode review:
- Flexible top-bar removal (handles attributes)
- Preserve ALL page/slide classes & data attrs
- Add nav JS in all cases
- Handle CSS conflicts
- Handle multiple template patterns
"""
import os, re

DIR = "/home/deploy/childrens-library/docs/courseware"

FILES = [
    'chinese-04-nature.html','chinese-05-family.html','chinese-06-school.html',
    'chinese-07-pinyin.html','chinese-08-pinyin2.html','chinese-09-shengmu1.html',
    'chinese-10-shengmu2.html','english-07-animals.html','math-04-addition.html',
    'math-09-subtraction20.html','math-10-shapes.html','chinese-02-strokes.html',
    'english-06-family.html','english-11-weather.html','english-12-clothes.html',
    'english-13-actions.html','english-14-places.html','english-15-feelings.html',
    'english-16-time.html','math-08-addition20.html',
    'english-08-body.html','english-10-toys.html','english-19-lost-cat.html',
    'math-06-subtraction5.html','math-07-subtraction10.html',
    'math-11-measurement.html','math-12-review.html',
]

NAV_CSS = '''
  /* Unified nav-bar (added by conversion) */
  .nav-bar{display:flex;align-items:center;justify-content:center;gap:14px;padding:10px 0 4px;position:relative;bottom:0;background:inherit;z-index:50}
  .nav-btn{width:48px;height:48px;border-radius:50%;border:2px solid #42A5F5;background:#fff;color:#42A5F5;font-size:22px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;user-select:none}
  .nav-btn:active{transform:scale(.88);background:#42A5F5;color:#fff}
  .nav-btn:disabled{opacity:.25;pointer-events:none}
  .page-dots{display:flex;gap:6px}
  .page-dots .dot{width:10px;height:10px;border-radius:50%;background:#ddd;cursor:pointer;border:none;transition:all .25s;padding:0}
  .page-dots .dot.active{background:#42A5F5;transform:scale(1.35)}
  .read-btn{background:#fff;border:2px solid #66BB6A;border-radius:20px;padding:8px 20px;font-size:16px;font-weight:700;color:#2e7d32;cursor:pointer;font-family:inherit;transition:all .2s;display:inline-flex;align-items:center;gap:4px}
  .read-btn:active{transform:scale(.94);background:#66BB6A;color:#fff}
'''

NAV_HTML = '''
  <!-- Bottom Navigation -->
  <div class="nav-bar">
    <button class="nav-btn" id="prevBtn" onclick="navPrev()">&#9664;</button>
    <div class="page-dots" id="pageDots"></div>
    <button class="nav-btn" id="nextBtn" onclick="navNext()">&#9654;</button>
  </div>
  <div style="text-align:center;margin:4px 0 12px">
    <button class="read-btn" onclick="navSpeakCurrentPage()">&#128264; 读给我听</button>
  </div>
'''

NAV_JS = '''
<script>
/* Unified nav (added by conversion) - uses unique names to avoid conflicts */
(function(){
  var pages = document.querySelectorAll('.page,.slide');
  var total = pages.length;
  if(total < 2) return;
  var cur = 0;
  pages.forEach(function(p,i){ if(p.classList.contains('active')) cur = i; });
  
  window.navGoTo = function(n){
    n = Math.max(0, Math.min(total - 1, n));
    pages.forEach(function(p,i){ p.classList.toggle('active', i === n); });
    var p = document.getElementById('prevBtn'), nx = document.getElementById('nextBtn');
    if(p) p.disabled = n === 0;
    if(nx) nx.disabled = n === total - 1;
    var c = document.getElementById('pageDots');
    if(c){ c.querySelectorAll('.dot').forEach(function(d,i){ d.classList.toggle('active', i === n); }); }
    cur = n;
    if(window.speechSynthesis) window.speechSynthesis.cancel();
    // Trigger page change callback if exists
    if(typeof window.onPageChange === 'function') window.onPageChange(n);
  };
  window.navPrev = function(){ window.navGoTo(cur - 1); };
  window.navNext = function(){ window.navGoTo(cur + 1); };
  window.navSpeakCurrentPage = function(){
    var btn = document.getElementById('speakBtn') || document.querySelector('.speak-btn');
    if(btn) btn.click();
  };
  
  // Build dots
  var c = document.getElementById('pageDots');
  if(c){
    c.innerHTML = '';
    for(var i = 0; i < total; i++){
      var d = document.createElement('button');
      d.className = 'dot' + (i === cur ? ' active' : '');
      d.setAttribute('data-idx', i);
      d.onclick = function(){ window.navGoTo(parseInt(this.getAttribute('data-idx'))); };
      c.appendChild(d);
    }
  }
  var p = document.getElementById('prevBtn');
  if(p) p.disabled = cur === 0;
})();
</script>
'''

fixed = 0
for fname in FILES:
    fpath = os.path.join(DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # 1) Remove old top navigation (various patterns, with any attributes)
    top_patterns = [
        r'<div\s+class=["\']top-bar["\'][^>]*>.*?</div>',     # <div class="top-bar" ...>
        r'<div\s+class=["\']topbar["\'][^>]*>.*?</div>',      # <div class="topbar" ...>
        r'<header\s+class=["\']top-bar["\'][^>]*>.*?</header>', # <header class="top-bar">
        r'<header\s+class=["\']header-bar["\'][^>]*>.*?</header>', # <header class="header-bar">
        r'<div\s+class=["\']header-bar["\'][^>]*>.*?</div>',   # <div class="header-bar">
    ]
    for pat in top_patterns:
        c = re.sub(pat, '', c, flags=re.DOTALL)
    
    # 2) Remove orphaned old home/speak button references (spans in old top-bar that remain)
    # These are already removed with the top-bar div, but check for floats
    c = re.sub(r'<span\s+class=["\']home-btn["\'][^>]*>.*?</span>', '', c)
    c = re.sub(r'<button\s+class=["\']home-btn["\'][^>]*>.*?</button>', '', c)
    
    # 3) Check if already has our nav-bar
    if 'window.navGoTo' in c:
        print(f"  - {fname} already converted")
        continue
    
    # 4) Add nav CSS before </style>
    style_end = c.rfind('</style>')
    if style_end > 0:
        # Check if nav-bar CSS already exists
        if '.nav-bar' not in c[:style_end]:
            c = c[:style_end] + NAV_CSS + '\n' + c[style_end:]
    
    # 5) Count pages
    pages = re.findall(r'<div[^>]*class=["\'][^"\']*\b(?:page|slide)\b[^"\']*["\']', c)
    total = len(pages)
    if total < 2:
        print(f"  - {fname} only {total} page(s)")
        continue
    
    # 6) Insert nav HTML + JS before </body>
    body_end = c.rfind('</body>')
    if body_end < 0:
        print(f"  ✗ {fname} no body tag")
        continue
    
    insert = '\n' + NAV_HTML + '\n' + NAV_JS + '\n'
    c = c[:body_end] + insert + c[body_end:]
    
    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        fixed += 1
        print(f"  ✓ {fname} ({total} pages)")
    else:
        print(f"  - {fname} unchanged")

print(f"\nFixed: {fixed}/{len(FILES)}")
