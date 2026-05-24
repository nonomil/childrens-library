# The Day the Crayons Quit — 逐页阅读

> **作者**：Drew Daywalt · 插画：Oliver Jeffers · **适合年龄**：4-8岁
> **5 张配图** · AI 生成插画

---

<div id="crayons_quit-reader" style="max-width: 800px; margin: 0 auto; text-align: center;">
  <div id="page-display" style="position: relative;">
    <img id="page-img" src="../../images/crayons_quit/page_01.webp"
         style="width: 100%; max-width: 700px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); cursor: pointer;"
         onclick="nextPage()" alt="Page">
    <div style="position: absolute; bottom: 12px; right: 12px;
                background: rgba(0,0,0,0.6); color: #fff;
                padding: 4px 12px; border-radius: 20px;
                font-size: 14px; font-weight: bold;">
      <span id="page-num">1</span> / 5
    </div>
  </div>

  <div style="margin: 20px 0; display: flex; justify-content: center; gap: 16px; align-items: center; flex-wrap: wrap;">
    <button onclick="firstPage()" style="padding: 10px 18px; border: 2px solid #009688; border-radius: 30px; background: white; color: #009688; font-size: 16px; cursor: pointer; font-weight: bold;">⏮ 首页</button>
    <button onclick="prevPage()" style="padding: 10px 24px; border: 2px solid #009688; border-radius: 30px; background: #009688; color: white; font-size: 16px; cursor: pointer; font-weight: bold;">◀ 上一页</button>
    <span id="page-input-area" style="font-size: 16px; color: #666;">
      第 <input id="page-input" type="number" min="1" max="5" value="1"
                 style="width: 50px; text-align: center; font-size: 16px; padding: 6px; border: 2px solid #ddd; border-radius: 8px;"
                 onkeydown="if(event.key==='Enter')goToPage()"> 页
      <button onclick="goToPage()" style="padding: 6px 14px; border: none; border-radius: 8px; background: #009688; color: white; cursor: pointer;">跳转</button>
    </span>
    <button onclick="nextPage()" style="padding: 10px 24px; border: 2px solid #009688; border-radius: 30px; background: #009688; color: white; font-size: 16px; cursor: pointer; font-weight: bold;">下一页 ▶</button>
    <button onclick="lastPage()" style="padding: 10px 18px; border: 2px solid #009688; border-radius: 30px; background: white; color: #009688; font-size: 16px; cursor: pointer; font-weight: bold;">末页 ⏭</button>
  </div>

  <div style="width: 100%; max-width: 700px; margin: 0 auto; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden;">
    <div id="progress-bar" style="height: 100%; width: 20.0%; background: linear-gradient(90deg, #FF5722, #FF9800); border-radius: 3px; transition: width 0.3s;"></div>
  </div>

  <div style="margin: 16px 0; font-size: 14px; color: #999;">
    💡 键盘：← 上一页 · → 下一页 · 点击图片翻页
  </div>

  <div style="margin: 24px 0;">
    <a href="../../pdfs/crayons_quit.pdf" target="_blank" style="display: inline-block; padding: 12px 28px; background: #ff6f00; color: white; border-radius: 30px; text-decoration: none; font-size: 18px; font-weight: bold;">📥 下载完整PDF</a>
  </div>
</div>

<script>
const totalPages = 5;
const imgCache = {};

function loadPage(n) {
  if (n < 1 || n > totalPages) return;
  const img = document.getElementById('page-img');
  const pageNum = document.getElementById('page-num');
  const progress = document.getElementById('progress-bar');
  const input = document.getElementById('page-input');
  const src = `../../images/crayons_quit/page_${String(n).padStart(2, '0')}.webp`;
  if (!imgCache[n]) { const pre = new Image(); pre.src = src; imgCache[n] = pre; }
  img.src = src;
  pageNum.textContent = n;
  input.value = n;
  progress.style.width = `${(n / totalPages) * 100}%`;
  for (let i = n - 1; i <= n + 1; i++) {
    if (i >= 1 && i <= totalPages && !imgCache[i]) {
      const pre = new Image();
      pre.src = `../../images/crayons_quit/page_${String(i).padStart(2, '0')}.webp`;
      imgCache[i] = pre;
    }
  }
}
function nextPage() { const n = parseInt(document.getElementById('page-num').textContent); if (n < totalPages) loadPage(n + 1); }
function prevPage() { const n = parseInt(document.getElementById('page-num').textContent); if (n > 1) loadPage(n - 1); }
function firstPage() { loadPage(1); }
function lastPage() { loadPage(totalPages); }
function goToPage() { const n = parseInt(document.getElementById('page-input').value); if (n >= 1 && n <= totalPages) loadPage(n); }
document.addEventListener('keydown', function(e) {
  if (e.target.id === 'page-input') return;
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { prevPage(); e.preventDefault(); }
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { nextPage(); e.preventDefault(); }
});
loadPage(1);
</script>

---

## 📚 亲子阅读小贴士

| 阶段 | 怎么读 |
|------|--------|
| **第1遍** | 每读一封信，用不同语气扮演不同蜡笔（红色很生气、粉色很伤心）|
| **第2遍** | 让孩子猜猜每种颜色画了什么（消防车、草莓……），再揭晓答案 |
| **第3遍** | 让孩子给家里的蜡笔写一封信，蜡笔会怎么回复？ |

!!! tip "Drew Daywalt的秘诀"
    每支蜡笔都是一个角色。阅读时让孩子看图猜情绪，这比直接认单词更有效。

---

[← 返回书目](./crayons_quit.md)
