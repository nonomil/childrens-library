# Knuffle Bunny: A Cautionary Tale — 逐页阅读

> **作者**：Mo Willems · **适合年龄**：2-5岁
> **5 张配图** · AI 生成插画

---

<div id="knuffle_bunny-reader" style="max-width: 800px; margin: 0 auto; text-align: center;">
  <div id="page-display" style="position: relative;">
    <img id="page-img" src="../../images/knuffle_bunny/page_01.webp"
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
    <div id="progress-bar" style="height: 100%; width: 20.0%; background: linear-gradient(90deg, #9C27B0, #E91E63); border-radius: 3px; transition: width 0.3s;"></div>
  </div>

  <div style="margin: 16px 0; font-size: 14px; color: #999;">
    💡 键盘：← 上一页 · → 下一页 · 点击图片翻页
  </div>

  <div style="margin: 24px 0;">
    <a href="../../pdfs/knuffle_bunny.pdf" target="_blank" style="display: inline-block; padding: 12px 28px; background: #ff6f00; color: white; border-radius: 30px; text-decoration: none; font-size: 18px; font-weight: bold;">📥 下载完整PDF</a>
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
  const src = `../../images/knuffle_bunny/page_${String(n).padStart(2, '0')}.webp`;
  if (!imgCache[n]) { const pre = new Image(); pre.src = src; imgCache[n] = pre; }
  img.src = src;
  pageNum.textContent = n;
  input.value = n;
  progress.style.width = `${(n / totalPages) * 100}%`;
  for (let i = n - 1; i <= n + 1; i++) {
    if (i >= 1 && i <= totalPages && !imgCache[i]) {
      const pre = new Image();
      pre.src = `../../images/knuffle_bunny/page_${String(i).padStart(2, '0')}.webp`;
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
| **第1遍** | 让所有"还在牙牙学语"的孩子感同身受地读 |
| **第2遍** | 到 Trixie 大哭那页时暂停，问孩子"她怎么了？" |
| **第3遍** | 角色扮演——你是爸爸，孩子是 Trixie，用肢体语言交流 |

!!! tip "Mo Willems的秘诀"
    这本书一半的故事在文字里，一半在插图中爸爸的表情里。翻页时让孩子先看爸爸的脸，再读文字。

---

[← 返回书目](./knuffle_bunny.md)
