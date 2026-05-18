# Don't Let the Pigeon Drive the Bus! — 逐页阅读

> **作者/插画**：Mo Willems · **获奖**：Caldecott Honor  
> **适合年龄**：2-6岁 · **39页**

---

<div id="pigeon-reader" style="max-width: 800px; margin: 0 auto; text-align: center;">
  <!-- 封面显示 -->
  <div id="page-display" style="position: relative;">
    <img id="page-img" src="../../images/pigeon_bus/page_01.png" 
         style="width: 100%; max-width: 700px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); cursor: pointer;"
         onclick="nextPage()" alt="Page">
    
    <!-- 页码角标 -->
    <div style="position: absolute; bottom: 12px; right: 12px; 
                background: rgba(0,0,0,0.6); color: #fff; 
                padding: 4px 12px; border-radius: 20px; 
                font-size: 14px; font-weight: bold;">
      <span id="page-num">1</span> / 39
    </div>
  </div>

  <!-- 控制按钮 -->
  <div style="margin: 20px 0; display: flex; justify-content: center; gap: 16px; align-items: center; flex-wrap: wrap;">
    <button onclick="firstPage()" style="padding: 10px 18px; border: 2px solid #009688; border-radius: 30px; background: white; color: #009688; font-size: 16px; cursor: pointer; font-weight: bold;">⏮ 首页</button>
    <button onclick="prevPage()" style="padding: 10px 24px; border: 2px solid #009688; border-radius: 30px; background: #009688; color: white; font-size: 16px; cursor: pointer; font-weight: bold;">◀ 上一页</button>
    <span id="page-input-area" style="font-size: 16px; color: #666;">
      第 <input id="page-input" type="number" min="1" max="39" value="1" 
                 style="width: 50px; text-align: center; font-size: 16px; padding: 6px; border: 2px solid #ddd; border-radius: 8px;"
                 onkeydown="if(event.key==='Enter')goToPage()"> 页
      <button onclick="goToPage()" style="padding: 6px 14px; border: none; border-radius: 8px; background: #009688; color: white; cursor: pointer;">跳转</button>
    </span>
    <button onclick="nextPage()" style="padding: 10px 24px; border: 2px solid #009688; border-radius: 30px; background: #009688; color: white; font-size: 16px; cursor: pointer; font-weight: bold;">下一页 ▶</button>
    <button onclick="lastPage()" style="padding: 10px 18px; border: 2px solid #009688; border-radius: 30px; background: white; color: #009688; font-size: 16px; cursor: pointer; font-weight: bold;">末页 ⏭</button>
  </div>

  <!-- 进度条 -->
  <div style="width: 100%; max-width: 700px; margin: 0 auto; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden;">
    <div id="progress-bar" style="height: 100%; width: 2.56%; background: linear-gradient(90deg, #009688, #26a69a); border-radius: 3px; transition: width 0.3s;"></div>
  </div>

  <!-- 键盘提示 -->
  <div style="margin: 16px 0; font-size: 14px; color: #999;">
    💡 键盘：← 上一页 · → 下一页 · 点击图片翻页
  </div>

  <!-- 下载 -->
  <div style="margin: 24px 0;">
    <a href="../../pdfs/pigeon_bus.pdf" target="_blank" style="display: inline-block; padding: 12px 28px; background: #ff6f00; color: white; border-radius: 30px; text-decoration: none; font-size: 18px; font-weight: bold;">📥 下载完整PDF</a>
  </div>
</div>

<script>
// 图片懒加载预缓存
const totalPages = 39;
const imgCache = {};

function loadPage(n) {
  if (n < 1 || n > totalPages) return;
  
  const img = document.getElementById('page-img');
  const pageNum = document.getElementById('page-num');
  const progress = document.getElementById('progress-bar');
  const input = document.getElementById('page-input');
  
  // 预加载当前页（如果还没缓存）
  const src = `../../images/pigeon_bus/page_${String(n).padStart(2, '0')}.png`;
  
  if (!imgCache[n]) {
    const preload = new Image();
    preload.src = src;
    imgCache[n] = preload;
  }
  
  img.src = src;
  pageNum.textContent = n;
  input.value = n;
  progress.style.width = `${(n / totalPages) * 100}%`;
  
  // 预读相邻两页
  for (let i = n - 1; i <= n + 1; i++) {
    if (i >= 1 && i <= totalPages && !imgCache[i]) {
      const pre = new Image();
      pre.src = `../../images/pigeon_bus/page_${String(i).padStart(2, '0')}.png`;
      imgCache[i] = pre;
    }
  }
}

function nextPage() {
  const n = parseInt(document.getElementById('page-num').textContent);
  if (n < totalPages) loadPage(n + 1);
}

function prevPage() {
  const n = parseInt(document.getElementById('page-num').textContent);
  if (n > 1) loadPage(n - 1);
}

function firstPage() { loadPage(1); }
function lastPage() { loadPage(totalPages); }
function goToPage() {
  const n = parseInt(document.getElementById('page-input').value);
  if (n >= 1 && n <= totalPages) loadPage(n);
}

// 键盘事件
document.addEventListener('keydown', function(e) {
  if (e.target.id === 'page-input') return;  // 输入框内不拦截
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { prevPage(); e.preventDefault(); }
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { nextPage(); e.preventDefault(); }
});

// 初始化
loadPage(1);
</script>

---

## 📚 亲子阅读小贴士

| 阶段 | 怎么读 |
|------|--------|
| **第1遍** | 用夸张的语气读对话，让鸽子"活"起来 |
| **第2遍** | 问孩子"要不要让鸽子开车？"——互动问答 |
| **第3遍** | 让孩子扮演司机，你扮演鸽子，对话式朗读 |

!!! tip "Mo Willems的秘诀"
    这本书的幽默全靠**对话节奏**。读的时候停顿要够长，让孩子有时间反应和笑。鸽子生气时声音变大，求人时变小。
