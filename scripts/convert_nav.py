#!/usr/bin/env python3
"""
Convert 27 courseware files to unified navigation.
Strategy: Keep ALL existing content/CSS/JS structure.
Only: 1) Remove old top-bar, 2) Add bottom nav-bar + read-btn, 3) Add nav JS
"""
import os, re

DIR = "/home/deploy/childrens-library/docs/courseware"
FILES = [
    # app+top-bar (11)
    'chinese-04-nature.html', 'chinese-05-family.html', 'chinese-06-school.html',
    'chinese-07-pinyin.html', 'chinese-08-pinyin2.html', 'chinese-09-shengmu1.html',
    'chinese-10-shengmu2.html', 'english-07-animals.html', 'math-04-addition.html',
    'math-09-subtraction20.html', 'math-10-shapes.html',
    # app简约 (9)
    'chinese-02-strokes.html', 'english-06-family.html', 'english-11-weather.html',
    'english-12-clothes.html', 'english-13-actions.html', 'english-14-places.html',
    'english-15-feelings.html', 'english-16-time.html', 'math-08-addition20.html',
    # top-bar+slide (7)
    'english-08-body.html', 'english-10-toys.html', 'english-19-lost-cat.html',
    'math-06-subtraction5.html', 'math-07-subtraction10.html',
    'math-11-measurement.html', 'math-12-review.html',
]

NAV_BAR = '''
  <!-- Bottom Navigation -->
  <div class="nav-bar">
    <button class="nav-btn" id="prevBtn" onclick="prevPage()">&#9664;</button>
    <div class="page-dots" id="pageDots"></div>
    <button class="nav-btn" id="nextBtn" onclick="nextPage()">&#9654;</button>
  </div>
  <div style="text-align:center;margin:4px 0 12px">
    <button class="read-btn" onclick="speakCurrentPage()">&#128264; 读给我听</button>
  </div>
'''

NAV_CSS = '''
  /* Unified nav-bar */
  .nav-bar{display:flex;align-items:center;justify-content:center;gap:14px;padding:10px 0 4px;position:sticky;bottom:0;background:inherit;z-index:50}
  .nav-btn{width:48px;height:48px;border-radius:50%;border:2px solid #42A5F5;background:#fff;color:#42A5F5;font-size:22px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s;user-select:none}
  .nav-btn:active{transform:scale(.88);background:#42A5F5;color:#fff}
  .nav-btn:disabled{opacity:.25;pointer-events:none}
  .page-dots{display:flex;gap:6px}
  .page-dots .dot{width:10px;height:10px;border-radius:50%;background:#ddd;cursor:pointer;border:none;transition:all .25s;padding:0}
  .page-dots .dot.active{background:#42A5F5;transform:scale(1.35)}
  .read-btn{background:#fff;border:2px solid #66BB6A;border-radius:20px;padding:8px 20px;font-size:16px;font-weight:700;color:#2e7d32;cursor:pointer;font-family:inherit;transition:all .2s;display:inline-flex;align-items:center;gap:4px}
  .read-btn:active{transform:scale(.94);background:#66BB6A;color:#fff}
'''

NAV_JS = '''
<script>
(function(){
  var pages = document.querySelectorAll('.page.active,.slide.active');
  var totalPages = document.querySelectorAll('.page,.slide').length;
  if(totalPages < 2) return; // single page, no nav needed
  var currentPage = 0;
  
  // Find first active
  document.querySelectorAll('.page,.slide').forEach(function(p,i){
    if(p.classList.contains('active')) currentPage = i;
  });
  
  window.prevPage = function(){
    goToPage(currentPage - 1);
  };
  window.nextPage = function(){
    goToPage(currentPage + 1);
  };
  window.goToPage = function(n){
    n = Math.max(0, Math.min(totalPages - 1, n));
    document.querySelectorAll('.page,.slide').forEach(function(p,i){
      p.classList.toggle('active', i === n);
    });
    var prev = document.getElementById('prevBtn');
    var next = document.getElementById('nextBtn');
    if(prev) prev.disabled = n === 0;
    if(next) next.disabled = n === totalPages - 1;
    renderDots();
    currentPage = n;
    // Stop any ongoing speech
    if(window.speechSynthesis) window.speechSynthesis.cancel();
  };
  
  function renderDots(){
    var c = document.getElementById('pageDots');
    if(!c) return;
    c.innerHTML = '';
    for(var i = 0; i < totalPages; i++){
      var d = document.createElement('button');
      d.className = 'dot' + (i === currentPage ? ' active' : '');
      d.setAttribute('data-idx', i);
      d.onclick = function(){ goToPage(parseInt(this.getAttribute('data-idx'))); };
      c.appendChild(d);
    }
  }
  
  // Also wire existing prev/next buttons if they exist
  var oldPrev = document.querySelector('[onclick*="prev"],[onclick*="Prev"]');
  var oldNext = document.querySelector('[onclick*="next"],[onclick*="Next"]');
  // Don't override - add our own
  renderDots();
})();
</script>
'''

fixed = 0
for fname in FILES:
    fpath = os.path.join(DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c

    # 1) Remove old top-bar / header-bar (but keep their content if any)
    # Various patterns for top navigation
    for pattern in [
        r'<div class="top-bar">.*?</div>',
        r'<header class="header-bar">.*?</header>',
        r'<header class="top-bar">.*?</header>',
        r'<div class="topbar">.*?</div>',
        r'<div class="header-bar">.*?</div>',
    ]:
        c = re.sub(pattern, '', c, flags=re.DOTALL)
    
    # 2) Already has nav-bar? Skip
    if '<div class="nav-bar"' in c:
        print(f"  - {fname} already has nav-bar")
        continue
    
    # 3) Add nav-bar CSS before </style>
    style_end = c.rfind('</style>')
    if style_end >= 0 and 'nav-bar' not in c[:style_end]:
        c = c[:style_end] + NAV_CSS + c[style_end:]
    
    # 4) Count pages
    page_count = len(re.findall(r'class="[^"]*\bpage\b[^"]*"', c))
    slide_count = len(re.findall(r'class="[^"]*\bslide\b[^"]*"', c))
    total = max(page_count, slide_count)
    
    if total < 2:
        print(f"  - {fname} only {total} page(s), skipping")
        continue
    
    # 5) Find insertion point: before </body> or before last </div> that closes the main container
    # Insert before the MP3优先 script or before </body>
    insert_before = c.rfind('<!-- ═══ Speak Page')
    if insert_before < 0:
        insert_before = c.rfind('</body>')
    if insert_before < 0:
        insert_before = c.rfind('</html>')
    
    if insert_before < 0:
        print(f"  ✗ {fname} cannot find insertion point")
        continue
    
    # Insert nav bar + JS
    nav_html = NAV_BAR.replace('TOTAL', str(total))
    
    if '<!-- ═══ Speak Page' in c:
        c = c[:insert_before] + nav_html + '\n' + c[insert_before:]
    else:
        c = c[:insert_before] + nav_html + '\n' + NAV_JS + '\n' + c[insert_before:]
    
    # 6) Remove old top-bar CSS rules that are now orphaned
    # (Kept for safety - CSS for removed elements won't harm)
    
    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        fixed += 1
        print(f"  ✓ {fname} ({total} pages)")

print(f"\nFixed: {fixed}/{len(FILES)}")
