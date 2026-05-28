/**
 * ChildrenComponentEngine (CEC)
 * Reusable Canvas 2D component library for children's educational courseware.
 * Pure ES6, zero dependencies, touch+mouse, responsive.
 */
(function () {
  'use strict';

  const CEC = {};
  window.CEC = window.ChildrenComponentEngine = CEC;

  // ====================================================================
  // 1. Utility Functions (CEC.utils.*)
  // ====================================================================
  CEC.utils = {};

  CEC.utils.$ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  CEC.utils.$$ = function (sel, ctx) { return [...(ctx || document).querySelectorAll(sel)]; };
  CEC.utils.clamp = function (v, lo, hi) { return Math.max(lo, Math.min(hi, v)); };
  CEC.utils.lerp = function (a, b, t) { return a + (b - a) * t; };
  CEC.utils.dist = function (x1, y1, x2, y2) { return Math.hypot(x2 - x1, y2 - y1); };
  CEC.utils.randInt = function (lo, hi) { return Math.floor(Math.random() * (hi - lo + 1)) + lo; };
  CEC.utils.shuffle = function (arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = CEC.utils.randInt(0, i);
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  };
  CEC.utils.shadeColor = function (hex, pct) {
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16);
    let b = parseInt(hex.slice(5, 7), 16);
    r = CEC.utils.clamp(r + pct, 0, 255);
    g = CEC.utils.clamp(g + pct, 0, 255);
    b = CEC.utils.clamp(b + pct, 0, 255);
    return '#' + [r, g, b].map(function (c) { return c.toString(16).padStart(2, '0'); }).join('');
  };

  // ====================================================================
  // 2. Canvas Helpers (CEC.canvas.*)
  // ====================================================================
  CEC.canvas = {};

  CEC.canvas.setupCanvas = function (canvas, heightRatio) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const W = rect.width;
    const H = Math.min(W * (heightRatio || 0.65), 420);
    canvas.style.height = H + 'px';
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, W: W, H: H };
  };

  CEC.canvas.drawGear = function (ctx, cx, cy, radius, teeth, angle, color, hubColor) {
    const toothH = radius * 0.13;
    const outerR = radius + toothH;
    const innerR = radius - toothH * 0.5;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle);
    ctx.beginPath();
    for (let i = 0; i < teeth; i++) {
      const a1 = (i / teeth) * Math.PI * 2;
      const a2 = ((i + 0.3) / teeth) * Math.PI * 2;
      const a3 = ((i + 0.7) / teeth) * Math.PI * 2;
      const a4 = ((i + 1) / teeth) * Math.PI * 2;
      if (i === 0) ctx.moveTo(Math.cos(a1) * innerR, Math.sin(a1) * innerR);
      ctx.lineTo(Math.cos(a2) * outerR, Math.sin(a2) * outerR);
      ctx.lineTo(Math.cos(a3) * outerR, Math.sin(a3) * outerR);
      ctx.lineTo(Math.cos(a4) * innerR, Math.sin(a4) * innerR);
    }
    ctx.closePath();
    const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, outerR);
    grad.addColorStop(0, color);
    grad.addColorStop(1, CEC.utils.shadeColor(color, -20));
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.strokeStyle = CEC.utils.shadeColor(color, -30);
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, 0, radius * 0.6, 0, Math.PI * 2);
    ctx.fillStyle = CEC.utils.shadeColor(color, 15);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(0, 0, radius * 0.15, 0, Math.PI * 2);
    ctx.fillStyle = hubColor || '#fff';
    ctx.fill();
    ctx.strokeStyle = 'rgba(0,0,0,0.15)';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.restore();
  };

  CEC.canvas.drawGearEyes = function (ctx, cx, cy, radius, blinkPhase) {
    const eyeR = radius * 0.12;
    const pupilR = eyeR * 0.5;
    const eyeSpacing = radius * 0.22;
    const blinkScale = blinkPhase > 0.9 ? (1 - blinkPhase) * 10 : 1;
    ctx.save();
    ctx.beginPath();
    ctx.ellipse(cx - eyeSpacing, cy - radius * 0.05, eyeR, eyeR * blinkScale, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#fff';
    ctx.fill();
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx - eyeSpacing, cy - radius * 0.05, pupilR * blinkScale, 0, Math.PI * 2);
    ctx.fillStyle = '#333';
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(cx + eyeSpacing, cy - radius * 0.05, eyeR, eyeR * blinkScale, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#fff';
    ctx.fill();
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx + eyeSpacing, cy - radius * 0.05, pupilR * blinkScale, 0, Math.PI * 2);
    ctx.fillStyle = '#333';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(cx, cy + radius * 0.1, radius * 0.15, 0.1 * Math.PI, 0.9 * Math.PI);
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.restore();
  };

  CEC.canvas.drawLabel = function (ctx, text, x, y, color) {
    ctx.save();
    ctx.font = 'bold 13px -apple-system,sans-serif';
    ctx.fillStyle = color || '#555';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, x, y);
    ctx.restore();
  };

  // ====================================================================
  // 3. UI Helpers (CEC.ui.*)
  // ====================================================================
  CEC.ui = {};

  CEC.ui.createSparkle = function (x, y, container) {
    const emojis = ['✨', '⭐', '🌟', '💫', '🎉'];
    for (let i = 0; i < 6; i++) {
      const s = document.createElement('div');
      s.className = 'sparkle';
      s.textContent = emojis[CEC.utils.randInt(0, emojis.length - 1)];
      s.style.left = (x + CEC.utils.randInt(-30, 30)) + 'px';
      s.style.top = (y + CEC.utils.randInt(-30, 30)) + 'px';
      s.style.animationDelay = (i * 0.08) + 's';
      (container || document.body).appendChild(s);
      setTimeout(function () { s.remove(); }, 800);
    }
  };

  CEC.ui.showFeedback = function (canvas, emoji) {
    const wrap = canvas.parentElement;
    let fb = wrap.querySelector('.game-feedback');
    if (!fb) { fb = document.createElement('div'); fb.className = 'game-feedback'; wrap.appendChild(fb); }
    fb.textContent = emoji;
    fb.classList.add('show');
    setTimeout(function () { fb.classList.remove('show'); }, 800);
  };

  CEC.ui.createSlider = function (container, label, min, max, value, onChange) {
    const id = 'slider-' + Math.random().toString(36).slice(2, 8);
    const row = document.createElement('div');
    row.className = 'slider-row';
    row.innerHTML = '<label>' + label + ':</label>' +
      '<input type="range" id="' + id + '" min="' + min + '" max="' + max + '" value="' + value + '">' +
      '<span class="slider-val" id="' + id + '-val">' + value + '</span>';
    container.appendChild(row);
    const slider = row.querySelector('input[type=range]');
    const valEl = row.querySelector('.slider-val');
    slider.addEventListener('input', function () {
      valEl.textContent = slider.value;
      if (onChange) onChange(+slider.value);
    });
    return { row: row, slider: slider, valEl: valEl };
  };

  CEC.ui.createButton = function (container, text, className, onClick) {
    const btn = document.createElement('button');
    btn.className = 'btn ' + (className || 'btn-primary');
    btn.textContent = text;
    btn.addEventListener('click', onClick);
    container.appendChild(btn);
    return btn;
  };

  CEC.ui.createCard = function (container) {
    const card = document.createElement('div');
    card.className = 'card';
    container.appendChild(card);
    return card;
  };

  // ====================================================================
  // 4. Drag Helpers (CEC.drag.*)
  // ====================================================================
  CEC.drag = {};

  CEC.drag.addDrag = function (canvas, onStart, onMove, onEnd) {
    let dragging = false;
    function getPos(e) {
      const r = canvas.getBoundingClientRect();
      const t = e.touches ? e.touches[0] : e;
      return { x: t.clientX - r.left, y: t.clientY - r.top };
    }
    function start(e) { e.preventDefault(); dragging = true; var p = getPos(e); if (onStart) onStart(p); }
    function move(e) { if (!dragging) return; e.preventDefault(); var p = getPos(e); if (onMove) onMove(p); }
    function end() { if (!dragging) return; dragging = false; if (onEnd) onEnd(); }
    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', move);
    canvas.addEventListener('mouseup', end);
    canvas.addEventListener('mouseleave', end);
    canvas.addEventListener('touchstart', start, { passive: false });
    canvas.addEventListener('touchmove', move, { passive: false });
    canvas.addEventListener('touchend', end);
    return {
      destroy: function () {
        canvas.removeEventListener('mousedown', start);
        canvas.removeEventListener('mousemove', move);
        canvas.removeEventListener('mouseup', end);
        canvas.removeEventListener('mouseleave', end);
        canvas.removeEventListener('touchstart', start);
        canvas.removeEventListener('touchmove', move);
        canvas.removeEventListener('touchend', end);
      }
    };
  };

  // ====================================================================
  // 5. Interactive Components (CEC.components.*)
  // ====================================================================
  CEC.components = {};

  // --- InteractiveGear ---
  CEC.components.InteractiveGear = function (destEl, config) {
    config = config || {};
    var teeth = config.teeth || 12;
    var color = config.color || '#FF6B35';
    var heightRatio = config.heightRatio || 0.6;

    var canvas = document.createElement('canvas');
    destEl.appendChild(canvas);
    var setup = CEC.canvas.setupCanvas(canvas, heightRatio);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var angle = 0, angVel = 0, dragging = false, lastAngle = null;
    var blink = 0, nextBlink = 2000 + Math.random() * 2000, lastTime = 0;
    var rafId = null;

    // Controls
    var ctrlEl = document.createElement('div');
    destEl.appendChild(ctrlEl);
    var sliderInfo = CEC.ui.createSlider(ctrlEl, '齿数', 6, 24, teeth, function (v) { teeth = v; });

    CEC.drag.addDrag(canvas,
      function (p) { dragging = true; lastAngle = Math.atan2(p.y - H / 2, p.x - W / 2); },
      function (p) {
        if (!dragging) return;
        var a = Math.atan2(p.y - H / 2, p.x - W / 2);
        var d = a - lastAngle;
        if (d > Math.PI) d -= Math.PI * 2;
        if (d < -Math.PI) d += Math.PI * 2;
        angle += d;
        angVel = d * 60;
        lastAngle = a;
      },
      function () { dragging = false; }
    );

    function render(time) {
      var dt = time - lastTime; lastTime = time;
      if (!dragging) { angle += angVel * dt / 1000; angVel *= 0.97; }
      blink += dt / 1000;
      if (blink > nextBlink / 1000) { blink = 0; nextBlink = 2000 + Math.random() * 2000; }
      var blinkPhase = blink < 0.15 ? blink / 0.15 : 1;
      ctx.clearRect(0, 0, W, H);
      var r = Math.min(W, H) * 0.28;
      CEC.canvas.drawGear(ctx, W / 2, H / 2, r, teeth, angle, color, '#fff');
      CEC.canvas.drawGearEyes(ctx, W / 2, H / 2, r, blinkPhase);
      CEC.canvas.drawLabel(ctx, teeth + ' 齿', W / 2, H / 2 + r + 24, CEC.utils.shadeColor(color, -20));
      CEC.canvas.drawLabel(ctx, '拖拽旋转齿轮 ✨', W / 2, H - 16, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); canvas.remove(); ctrlEl.remove(); }
    };
  };

  // --- GearPair ---
  CEC.components.GearPair = function (destEl, config) {
    config = config || {};
    var t1 = config.teeth1 || 20;
    var t2 = config.teeth2 || 10;
    var heightRatio = config.heightRatio || 0.6;

    var canvas = document.createElement('canvas');
    destEl.appendChild(canvas);
    var setup = CEC.canvas.setupCanvas(canvas, heightRatio);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var angle1 = 0, angVel = 0, dragging = false, lastAngle = null;
    var blink = 0, nextBlink = 2500, lastTime = 0;
    var rafId = null;

    var r1 = function () { return Math.min(W, H) * 0.2; };
    var r2 = function () { return r1() * (t2 / t1); };
    var gap = function () { return r1() + r2() + r1() * 0.1; };
    var c1x = function () { return W / 2 - gap() / 2; };
    var c2x = function () { return W / 2 + gap() / 2; };
    var cy = function () { return H / 2; };

    CEC.drag.addDrag(canvas,
      function (p) { dragging = true; lastAngle = Math.atan2(p.y - cy(), p.x - c1x()); },
      function (p) {
        if (!dragging) return;
        var a = Math.atan2(p.y - cy(), p.x - c1x());
        var d = a - lastAngle;
        if (d > Math.PI) d -= Math.PI * 2;
        if (d < -Math.PI) d += Math.PI * 2;
        angle1 += d;
        angVel = d * 60;
        lastAngle = a;
      },
      function () { dragging = false; }
    );

    function render(time) {
      var dt = time - lastTime; lastTime = time;
      if (!dragging) { angle1 += angVel * dt / 1000; angVel *= 0.97; }
      blink += dt / 1000;
      if (blink > nextBlink / 1000) { blink = 0; nextBlink = 2500; }
      var bp = blink < 0.15 ? blink / 0.15 : 1;
      ctx.clearRect(0, 0, W, H);
      CEC.canvas.drawGear(ctx, c1x(), cy(), r1(), t1, angle1, '#FF6B35', '#fff');
      CEC.canvas.drawGearEyes(ctx, c1x(), cy(), r1(), bp);
      CEC.canvas.drawGear(ctx, c2x(), cy(), r2(), t2, -angle1 * (t1 / t2), '#2196F3', '#fff');
      CEC.canvas.drawGearEyes(ctx, c2x(), cy(), r2(), bp);
      CEC.canvas.drawLabel(ctx, t1 + ' 齿 (慢)', c1x(), cy() + r1() + 24, '#E8751A');
      CEC.canvas.drawLabel(ctx, t2 + ' 齿 (快' + (t1 / t2) + '×)', c2x(), cy() + r2() + 24, '#1565C0');
      CEC.canvas.drawLabel(ctx, '拖拽大齿轮试试', W / 2, H - 16, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); canvas.remove(); }
    };
  };

  // --- ChainDrive ---
  CEC.components.ChainDrive = function (destEl, config) {
    config = config || {};
    var heightRatio = config.heightRatio || 0.6;
    var tension = 0.5;

    var canvas = document.createElement('canvas');
    destEl.appendChild(canvas);
    var setup = CEC.canvas.setupCanvas(canvas, heightRatio);
    var ctx = setup.ctx, W = setup.W, H = setup.H;
    var ctrlEl = document.createElement('div');
    destEl.appendChild(ctrlEl);

    var angle = 0, angVel = 0, dragging = false, lastAngle = null;
    var rafId = null;

    CEC.ui.createSlider(ctrlEl, '链条松紧', 0, 100, 50, function (v) { tension = v / 100; });

    var r1 = function () { return Math.min(W, H) * 0.2; };
    var r2 = function () { return r1() * 0.65; };
    var gap = function () { return r1() + r2() + W * 0.25; };
    var c1x = function () { return W / 2 - gap() / 2; };
    var c2x = function () { return W / 2 + gap() / 2; };
    var cy = function () { return H / 2; };

    CEC.drag.addDrag(canvas,
      function (p) { dragging = true; lastAngle = Math.atan2(p.y - cy(), p.x - c1x()); },
      function (p) {
        if (!dragging) return;
        var a = Math.atan2(p.y - cy(), p.x - c1x());
        var d = a - lastAngle;
        if (d > Math.PI) d -= Math.PI * 2;
        if (d < -Math.PI) d += Math.PI * 2;
        angle += d;
        angVel = d * 60;
        lastAngle = a;
      },
      function () { dragging = false; }
    );

    function render() {
      if (!dragging) { angle += angVel * 0.016; angVel *= 0.97; }
      ctx.clearRect(0, 0, W, H);
      var yOff = (1 - tension) * 15;
      ctx.beginPath();
      ctx.moveTo(c1x(), cy() - r1());
      ctx.lineTo(c2x(), cy() - r2() - yOff);
      ctx.arc(c2x(), cy(), r2(), -Math.PI / 2, Math.PI / 2);
      ctx.lineTo(c1x(), cy() + r1() + yOff);
      ctx.arc(c1x(), cy(), r1(), Math.PI / 2, -Math.PI / 2);
      ctx.closePath();
      ctx.strokeStyle = '#555';
      ctx.lineWidth = 8;
      ctx.stroke();
      ctx.strokeStyle = '#888';
      ctx.lineWidth = 4;
      ctx.setLineDash([6, 4]);
      ctx.lineDashOffset = -angle * r1() * 0.5;
      ctx.stroke();
      ctx.setLineDash([]);
      CEC.canvas.drawGear(ctx, c1x(), cy(), r1(), 16, angle, '#A0826A', '#8B6F57');
      CEC.canvas.drawGear(ctx, c2x(), cy(), r2(), 10, -angle * 1.6, '#A0826A', '#8B6F57');
      CEC.canvas.drawLabel(ctx, '⛓️ 链条传动', W / 2, 24, '#8B6F57');
      CEC.canvas.drawLabel(ctx, '拖拽转动 · 自行车就是这样传动的', W / 2, H - 16, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); canvas.remove(); ctrlEl.remove(); }
    };
  };

  // --- Linkage ---
  CEC.components.Linkage = function (destEl, config) {
    config = config || {};
    var heightRatio = config.heightRatio || 0.65;

    var canvas = document.createElement('canvas');
    destEl.appendChild(canvas);
    var setup = CEC.canvas.setupCanvas(canvas, heightRatio);
    var ctx = setup.ctx, W = setup.W, H = setup.H;
    var ctrlEl = document.createElement('div');
    destEl.appendChild(ctrlEl);

    var angle = 0, autoPlay = true;
    var rafId = null;

    var toggle = CEC.ui.createButton(ctrlEl, '⏸ 暂停', 'btn-secondary', function () {
      autoPlay = !autoPlay;
      toggle.textContent = autoPlay ? '⏸ 暂停' : '▶ 播放';
    });
    toggle.style.display = 'block';
    toggle.style.margin = '0 auto';

    CEC.drag.addDrag(canvas,
      function () {},
      function (p) {
        var cx = W * 0.3, cy = H * 0.5;
        angle = Math.atan2(p.y - cy, p.x - cx);
      },
      function () {}
    );

    function render() {
      if (autoPlay) angle += 0.02;
      ctx.clearRect(0, 0, W, H);
      var cx = W * 0.3, cy = H * 0.5;
      var crankR = Math.min(W, H) * 0.15;
      var rodLen = crankR * 2.5;
      var rockerLen = crankR * 1.8;
      var fixedDist = crankR * 2.2;
      var ex = cx + Math.cos(angle) * crankR;
      var ey = cy + Math.sin(angle) * crankR;
      var rx = cx + fixedDist, ry = cy;
      var dx = ex - rx, dy = ey - ry;
      var d = Math.hypot(dx, dy);
      var cosA = CEC.utils.clamp((d * d + rockerLen * rockerLen - rodLen * rodLen) / (2 * d * rockerLen), -1, 1);
      var baseA = Math.atan2(dy, dx);
      var rockerAngle = baseA + Math.acos(cosA);
      var bx = rx + Math.cos(rockerAngle) * rockerLen;
      var by = ry + Math.sin(rockerAngle) * rockerLen;
      ctx.lineWidth = 6;
      ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ex, ey);
      ctx.strokeStyle = '#FF6B35'; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(ex, ey); ctx.lineTo(bx, by);
      ctx.strokeStyle = '#2196F3'; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(rx, ry); ctx.lineTo(bx, by);
      ctx.strokeStyle = '#4CAF50'; ctx.stroke();
      [cx, rx].forEach(function (px) {
        ctx.beginPath(); ctx.arc(px, cy, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#333'; ctx.fill();
      });
      [[ex, ey], [bx, by]].forEach(function (j) {
        ctx.beginPath(); ctx.arc(j[0], j[1], 5, 0, Math.PI * 2);
        ctx.fillStyle = '#FF9800'; ctx.fill();
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
      });
      ctx.beginPath();
      ctx.arc(bx, by, 3, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,107,53,0.3)'; ctx.fill();
      CEC.canvas.drawLabel(ctx, '🔗 曲柄摇杆机构', W / 2, 24, '#333');
      CEC.canvas.drawLabel(ctx, '橙色=曲柄 蓝色=连杆 绿色=摇杆', W / 2, H - 16, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); canvas.remove(); ctrlEl.remove(); }
    };
  };

  // --- BeltDrive ---
  CEC.components.BeltDrive = function (destEl, config) {
    config = config || {};
    var heightRatio = config.heightRatio || 0.6;

    var canvas = document.createElement('canvas');
    destEl.appendChild(canvas);
    var setup = CEC.canvas.setupCanvas(canvas, heightRatio);
    var ctx = setup.ctx, W = setup.W, H = setup.H;
    var ctrlEl = document.createElement('div');
    destEl.appendChild(ctrlEl);

    var angle = 0, crossed = false;
    var rafId = null;

    var toggle = CEC.ui.createButton(ctrlEl, '🔄 切换交叉/平行', 'btn-primary', function () {
      crossed = !crossed;
      toggle.textContent = crossed ? '🔄 平行传动' : '🔄 交叉传动';
    });
    toggle.style.display = 'block';
    toggle.style.margin = '0 auto';

    CEC.drag.addDrag(canvas,
      function () {},
      function (p) {
        var cx = W * 0.25, cy = H / 2;
        angle = Math.atan2(p.y - cy, p.x - cx);
      },
      function () {}
    );

    function render() {
      angle += 0.015;
      ctx.clearRect(0, 0, W, H);
      var r1 = Math.min(W, H) * 0.18;
      var r2 = r1 * 0.6;
      var c1x = W * 0.3, cy = H / 2;
      var c2x = W * 0.7;
      ctx.beginPath();
      if (crossed) {
        ctx.moveTo(c1x, cy - r1);
        ctx.lineTo(c2x, cy + r2);
        ctx.arc(c2x, cy, r2, Math.PI / 2, -Math.PI / 2, true);
        ctx.lineTo(c1x, cy + r1);
        ctx.arc(c1x, cy, r1, Math.PI / 2, -Math.PI / 2, true);
      } else {
        ctx.moveTo(c1x, cy - r1);
        ctx.lineTo(c2x, cy - r2);
        ctx.arc(c2x, cy, r2, -Math.PI / 2, Math.PI / 2);
        ctx.lineTo(c1x, cy + r1);
        ctx.arc(c1x, cy, r1, Math.PI / 2, -Math.PI / 2);
      }
      ctx.closePath();
      ctx.fillStyle = crossed ? 'rgba(255,152,0,0.15)' : 'rgba(33,150,243,0.15)';
      ctx.fill();
      ctx.strokeStyle = crossed ? '#FF9800' : '#2196F3';
      ctx.lineWidth = 10;
      ctx.stroke();
      ctx.strokeStyle = crossed ? '#FFB74D' : '#64B5F6';
      ctx.lineWidth = 4;
      ctx.setLineDash([8, 5]);
      ctx.lineDashOffset = -angle * r1;
      ctx.stroke();
      ctx.setLineDash([]);
      CEC.canvas.drawGear(ctx, c1x, cy, r1, 1, angle, '#795548', '#5D4037');
      CEC.canvas.drawGear(ctx, c2x, cy, r2, 1, crossed ? -angle * (r1 / r2) : angle * (r1 / r2), '#795548', '#5D4037');
      CEC.canvas.drawLabel(ctx, crossed ? '交叉传动 (反向)' : '平行传动 (同向)', W / 2, 24, '#795548');
      CEC.canvas.drawLabel(ctx, '点击按钮切换传动方式', W / 2, H - 16, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); canvas.remove(); ctrlEl.remove(); }
    };
  };

  // --- GearLab ---
  CEC.components.GearLab = function (destEl, config) {
    config = config || {};
    var heightRatio = config.heightRatio || 0.65;
    var t1 = config.teeth1 || 20;
    var t2 = config.teeth2 || 12;

    var canvas = document.createElement('canvas');
    destEl.appendChild(canvas);
    var setup = CEC.canvas.setupCanvas(canvas, heightRatio);
    var ctx = setup.ctx, W = setup.W, H = setup.H;
    var ctrlEl = document.createElement('div');
    destEl.appendChild(ctrlEl);

    var angle = 0, angVel = 0, dragging = false, lastAngle = null;
    var rafId = null;

    CEC.ui.createSlider(ctrlEl, '主动轮', 8, 28, t1, function (v) { t1 = v; });
    CEC.ui.createSlider(ctrlEl, '从动轮', 8, 28, t2, function (v) { t2 = v; });

    var r1 = function () { return Math.min(W, H) * 0.15 * (t1 / 16); };
    var r2 = function () { return Math.min(W, H) * 0.15 * (t2 / 16); };
    var gap = function () { return r1() + r2() + 4; };
    var c1x = function () { return W / 2 - gap() / 2; };
    var c2x = function () { return W / 2 + gap() / 2; };
    var cy = function () { return H / 2; };

    CEC.drag.addDrag(canvas,
      function (p) { dragging = true; lastAngle = Math.atan2(p.y - cy(), p.x - c1x()); },
      function (p) {
        if (!dragging) return;
        var a = Math.atan2(p.y - cy(), p.x - c1x());
        var d = a - lastAngle;
        if (d > Math.PI) d -= Math.PI * 2;
        if (d < -Math.PI) d += Math.PI * 2;
        angle += d;
        angVel = d * 60;
        lastAngle = a;
      },
      function () { dragging = false; }
    );

    function render() {
      if (!dragging) { angle += angVel * 0.016; angVel *= 0.97; }
      ctx.clearRect(0, 0, W, H);
      CEC.canvas.drawGear(ctx, c1x(), cy(), r1(), t1, angle, '#FF6B35', '#fff');
      CEC.canvas.drawGear(ctx, c2x(), cy(), r2(), t2, -angle * (t1 / t2), '#2196F3', '#fff');
      var ratio = t1 / t2;
      CEC.canvas.drawLabel(ctx, t1 + '齿', c1x(), cy() + r1() + 18, '#E8751A');
      CEC.canvas.drawLabel(ctx, t2 + '齿', c2x(), cy() + r2() + 18, '#1565C0');
      CEC.canvas.drawLabel(ctx, '速比 ' + t1 + ':' + t2 + ' = ' + ratio.toFixed(2) + ':1', W / 2, H - 40, '#333');
      CEC.canvas.drawLabel(ctx, '从动轮转速 ' + ratio.toFixed(1) + '×', W / 2, H - 20, ratio > 1 ? '#4CAF50' : '#FF5722');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); canvas.remove(); ctrlEl.remove(); }
    };
  };

  // ====================================================================
  // 6. Game Engines (CEC.games.*)
  // ====================================================================
  CEC.games = {};

  // --- GameMatch ---
  CEC.games.Match = function (destEl, config) {
    config = config || {};
    var difficulty = config.difficulty || 'Easy';
    var targetValue = config.targetValue;

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.55);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0, target = 0, current = 12;
    var total = config.total || 5;
    var targets = config.targets || [2, 3, 0.5, 1.5, 4];

    var sliderInfo = CEC.ui.createSlider(extra, '从动齿轮齿数', 6, 24, 12, function (v) { current = v; });
    var submitBtn = CEC.ui.createButton(extra, '确认 ✓', 'btn-primary', function () {
      var ratio = 24 / current;
      if (Math.abs(ratio - target) < 0.3) {
        score++;
        CEC.ui.showFeedback(canvas, '✅');
        CEC.ui.createSparkle(W / 2, H / 2, canvasWrap);
      } else {
        CEC.ui.showFeedback(canvas, '❌');
        canvasWrap.style.animation = 'shake .3s';
        setTimeout(function () { canvasWrap.style.animation = ''; }, 300);
      }
      scoreEl.textContent = '⭐ ' + score;
      round++;
      setTimeout(newRound, 800);
    });
    submitBtn.style.display = 'block';
    submitBtn.style.margin = '8px auto 0';

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 游戏结束！得分: ' + score + '/' + total; return; }
      target = targets[round];
      current = 12;
      goalEl.textContent = '🎯 目标速比: ' + target + ':1  ←  调整滑块!';
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
      sliderInfo.slider.value = 12;
      sliderInfo.valEl.textContent = '12';
    }

    var angle = 0;
    var rafId = null;
    function render() {
      angle += 0.02;
      ctx.clearRect(0, 0, W, H);
      var r1 = Math.min(W, H) * 0.22;
      var r2 = r1 * (current / 24);
      var g = r1 + r2 + 4;
      var c1x = W / 2 - g / 2, c2x = W / 2 + g / 2, cy = H / 2;
      CEC.canvas.drawGear(ctx, c1x, cy, r1, 24, angle, '#FF6B35', '#fff');
      CEC.canvas.drawGear(ctx, c2x, cy, r2, current, -angle * (24 / current), '#2196F3', '#fff');
      CEC.canvas.drawLabel(ctx, '24齿 (主动)', c1x, cy + r1 + 20, '#E8751A');
      CEC.canvas.drawLabel(ctx, current + '齿 (从动)', c2x, cy + r2 + 20, '#1565C0');
      CEC.canvas.drawLabel(ctx, '当前比: ' + (24 / current).toFixed(2) + ':1', W / 2, H - 16, '#333');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GameFix ---
  CEC.games.Fix = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.5);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0;
    var total = config.total || 5;
    var levels = config.levels || [
      { text: '🔧 需要连接两个远距离的轴', answer: 'chain', options: ['gear', 'chain', 'belt', 'rod'] },
      { text: '🔧 需要改变转速比', answer: 'gear', options: ['gear', 'chain', 'belt', 'rod'] },
      { text: '🔧 需要把旋转变成往复运动', answer: 'rod', options: ['gear', 'chain', 'belt', 'rod'] },
      { text: '🔧 需要连接两个较远的轴且允许打滑', answer: 'belt', options: ['gear', 'chain', 'belt', 'rod'] },
      { text: '🔧 需要精确同步两个轴的转速', answer: 'gear', options: ['gear', 'chain', 'belt', 'rod'] }
    ];
    var emojiMap = { gear: '⚙️', chain: '⛓️', belt: '🏗️', rod: '🔗' };
    var nameMap = { gear: '齿轮', chain: '链条', belt: '传动带', rod: '连杆' };

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 修理完成！得分: ' + score + '/' + total; extra.innerHTML = ''; return; }
      var lv = levels[round];
      goalEl.textContent = lv.text;
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
      extra.innerHTML = '<div class="game-options">' + CEC.utils.shuffle([...lv.options]).map(function (o) {
        return '<button class="game-option" data-val="' + o + '">' + emojiMap[o] + ' ' + nameMap[o] + '</button>';
      }).join('') + '</div>';
      extra.querySelectorAll('.game-option').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (btn.dataset.val === lv.answer) {
            btn.classList.add('correct');
            score++;
            CEC.ui.showFeedback(canvas, '✅');
            CEC.ui.createSparkle(W / 2, H / 2, canvasWrap);
          } else {
            btn.classList.add('wrong');
            CEC.ui.showFeedback(canvas, '❌');
          }
          scoreEl.textContent = '⭐ ' + score;
          extra.querySelectorAll('.game-option').forEach(function (b) { b.style.pointerEvents = 'none'; });
          round++;
          setTimeout(newRound, 900);
        });
      });
    }

    var rafId = null;
    function render() {
      ctx.clearRect(0, 0, W, H);
      CEC.canvas.drawLabel(ctx, '🔧 选择正确的传动零件！', W / 2, H / 2, '#666');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GameChain ---
  CEC.games.Chain = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.55);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0;
    var total = config.total || 5;
    var levels = config.levels || [
      { goal: '让输出变快 3×', sizes: [24, 12, 8], answer: [8, 12, 24] },
      { goal: '让输出变慢 2×', sizes: [8, 12, 24], answer: [24, 12, 8] },
      { goal: '让输出最快', sizes: [20, 10, 16], answer: [20, 10, 16] },
      { goal: '让输出最慢', sizes: [10, 20, 14], answer: [14, 20, 10] },
      { goal: '速度不变 (1:1)', sizes: [16, 12, 16], answer: [16, 16, 12] }
    ];
    var placed = [];

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 完成！得分: ' + score + '/' + total; extra.innerHTML = ''; return; }
      var lv = levels[round];
      placed = [];
      goalEl.textContent = '🐲 ' + lv.goal;
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
      extra.innerHTML = '<div class="game-palette" id="chainPalette"></div>' +
        '<div style="text-align:center;margin:6px 0;font-size:13px;color:#888">点击齿轮按顺序放入（从左到右）</div>' +
        '<div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap" id="chainSlots"></div>' +
        '<div style="text-align:center;margin-top:8px"><button class="btn btn-primary" id="chainCheck">检查 ✓</button> <button class="btn btn-warning" id="chainReset">重置</button></div>';
      var palette = extra.querySelector('#chainPalette');
      var slots = extra.querySelector('#chainSlots');
      CEC.utils.shuffle([...lv.sizes]).forEach(function (s) {
        var el = document.createElement('div');
        el.className = 'game-palette-item';
        el.textContent = s;
        el.style.fontSize = '14px';
        el.style.fontWeight = '700';
        el.addEventListener('click', function () {
          if (placed.length < 3) {
            placed.push(s);
            el.style.opacity = '0.3';
            el.style.pointerEvents = 'none';
            updateSlots();
          }
        });
        palette.appendChild(el);
      });
      function updateSlots() {
        slots.innerHTML = placed.map(function (s) {
          return '<div style="width:50px;height:50px;border-radius:50%;background:#FF6B35;color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700">' + s + '</div>';
        }).join('');
        if (placed.length < 3) {
          slots.innerHTML += '<div style="width:50px;height:50px;border-radius:50%;border:2px dashed #ccc;display:flex;align-items:center;justify-content:center;color:#ccc">?</div>'.repeat(3 - placed.length);
        }
      }
      updateSlots();
      extra.querySelector('#chainReset').addEventListener('click', function () {
        placed = [];
        palette.querySelectorAll('.game-palette-item').forEach(function (e) { e.style.opacity = '1'; e.style.pointerEvents = 'auto'; });
        updateSlots();
      });
      extra.querySelector('#chainCheck').addEventListener('click', function () {
        if (placed.length !== 3) return;
        var ok = placed[0] === lv.answer[0] && placed[1] === lv.answer[1] && placed[2] === lv.answer[2];
        if (ok) { score++; CEC.ui.showFeedback(canvas, '✅'); CEC.ui.createSparkle(W / 2, H / 2, canvasWrap); }
        else { CEC.ui.showFeedback(canvas, '❌'); }
        scoreEl.textContent = '⭐ ' + score;
        round++;
        setTimeout(newRound, 900);
      });
    }

    var rafId = null;
    function render() {
      ctx.clearRect(0, 0, W, H);
      CEC.canvas.drawLabel(ctx, '🐲 拖拽齿轮按顺序排列', W / 2, H / 2, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GameSort ---
  CEC.games.Sort = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.35);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var score = 0, total = config.total || 8;
    var items = config.items || [
      { emoji: '🚲', name: '自行车', cat: 'chain' },
      { emoji: '⏰', name: '钟表', cat: 'gear' },
      { emoji: '🚗', name: '汽车引擎', cat: 'gear' },
      { emoji: '🏭', name: '传送带', cat: 'belt' },
      { emoji: '🚂', name: '蒸汽火车', cat: 'rod' },
      { emoji: '🛗', name: '电梯', cat: 'belt' },
      { emoji: '🌀', name: '风扇', cat: 'belt' },
      { emoji: '🧵', name: '缝纫机', cat: 'gear' }
    ];
    var catNames = config.catNames || { gear: '⚙️齿轮', chain: '⛓️链条', belt: '🏗️传动带', rod: '🔗连杆' };
    var remaining = CEC.utils.shuffle([...items]);

    function renderSort() {
      goalEl.textContent = '📦 把每个物品拖到正确的传动类型!';
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = '剩余: ' + remaining.length;
      extra.innerHTML =
        '<div class="game-buckets">' +
        Object.keys(catNames).map(function (c) {
          var parts = catNames[c].split(' ');
          return '<div class="game-bucket" data-cat="' + c + '"><div class="game-bucket-label">' + parts[0] + '</div><div class="game-bucket-text">' + (parts[1] || '') + '</div><div class="game-bucket-items" id="bucket-' + c + '"></div></div>';
        }).join('') +
        '</div>' +
        '<div class="game-palette" id="sortPalette"></div>';
      var palette = extra.querySelector('#sortPalette');
      if (remaining.length > 0) {
        var item = remaining[0];
        var el = document.createElement('div');
        el.className = 'game-palette-item';
        el.textContent = item.emoji;
        el.style.fontSize = '32px';
        el.style.animation = 'pulse 1s ease-in-out infinite';
        palette.appendChild(el);
        var nameEl = document.createElement('div');
        nameEl.style.cssText = 'text-align:center;font-size:14px;font-weight:600;color:#333;margin-top:4px';
        nameEl.textContent = item.name;
        palette.appendChild(nameEl);
      }
      extra.querySelectorAll('.game-bucket').forEach(function (bucket) {
        bucket.addEventListener('click', function () {
          if (remaining.length === 0) return;
          var item = remaining[0];
          if (bucket.dataset.cat === item.cat) {
            score++;
            CEC.ui.showFeedback(canvas, '✅');
            CEC.ui.createSparkle(W / 2, H / 2, canvasWrap);
            var bItems = bucket.querySelector('.game-bucket-items');
            var span = document.createElement('span');
            span.textContent = item.emoji;
            span.style.fontSize = '20px';
            bItems.appendChild(span);
          } else {
            CEC.ui.showFeedback(canvas, '❌');
          }
          scoreEl.textContent = '⭐ ' + score;
          remaining.shift();
          if (remaining.length > 0) setTimeout(renderSort, 500);
          else { goalEl.textContent = '🎉 分类完成！得分: ' + score + '/' + total; extra.innerHTML = ''; }
        });
      });
    }

    var rafId = null;
    function render() {
      ctx.clearRect(0, 0, W, H);
      CEC.canvas.drawLabel(ctx, '📦 点击下方物品，再点正确的分类桶', W / 2, H / 2, '#999');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    renderSort();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GameSpeed ---
  CEC.games.Speed = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.5);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0;
    var total = config.total || 6;
    var levels = config.levels || [
      { text: '🏃 需要最大速度', need: 'speed', answer: 'small' },
      { text: '💪 需要最大力量', need: 'power', answer: 'big' },
      { text: '🏃 需要快速传送', need: 'speed', answer: 'small' },
      { text: '💪 需要举起重物', need: 'power', answer: 'big' },
      { text: '⚖️ 需要平衡速度和力量', need: 'balanced', answer: 'medium' },
      { text: '💪 需要最大扭矩', need: 'power', answer: 'big' }
    ];

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 完成！得分: ' + score + '/' + total; extra.innerHTML = ''; return; }
      var lv = levels[round];
      goalEl.textContent = lv.text;
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
      extra.innerHTML = '<div class="game-options">' +
        '<button class="game-option" data-val="small">🔴 小齿轮<br><small>高转速</small></button>' +
        '<button class="game-option" data-val="medium">🟡 中齿轮<br><small>均衡</small></button>' +
        '<button class="game-option" data-val="big">🟢 大齿轮<br><small>大力量</small></button>' +
        '</div>';
      extra.querySelectorAll('.game-option').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (btn.dataset.val === lv.answer) {
            btn.classList.add('correct');
            score++;
            CEC.ui.showFeedback(canvas, '✅');
            CEC.ui.createSparkle(W / 2, H / 2, canvasWrap);
          } else {
            btn.classList.add('wrong');
            CEC.ui.showFeedback(canvas, '❌');
          }
          scoreEl.textContent = '⭐ ' + score;
          extra.querySelectorAll('.game-option').forEach(function (b) { b.style.pointerEvents = 'none'; });
          round++;
          setTimeout(newRound, 900);
        });
      });
    }

    var rafId = null;
    function render() {
      ctx.clearRect(0, 0, W, H);
      CEC.canvas.drawLabel(ctx, '💪 选择合适的齿轮完成任务', W / 2, H / 2, '#666');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GamePuzzle ---
  CEC.games.Puzzle = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.6);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0;
    var total = config.total || 4;
    var levels = config.levels || [
      { grid: [[12, 0, 8], [0, 16, 12], [10, 8, 0]], answers: [10, 20, 14] },
      { grid: [[16, 12, 0], [8, 0, 12], [12, 8, 16]], answers: [14, 10] },
      { grid: [[0, 10, 16], [12, 0, 8], [8, 12, 0]], answers: [14, 14, 12] },
      { grid: [[20, 0, 12, 8], [0, 16, 0, 12], [12, 0, 10, 0], [8, 12, 0, 16]], answers: [14, 14, 14, 10] }
    ];
    var filled = [];

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 拼图完成！得分: ' + score + '/' + total; extra.innerHTML = ''; return; }
      var lv = levels[round];
      filled = lv.grid.map(function (row) { return row.map(function (v) { return v; }); });
      goalEl.textContent = '🧩 填满空缺(0)，让所有齿轮能转动';
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
      extra.innerHTML = '<div class="game-palette" id="puzzlePalette"></div>' +
        '<div style="text-align:center;margin-top:8px"><button class="btn btn-primary" id="puzzleCheck">检查 ✓</button> <button class="btn btn-warning" id="puzzleReset">重置</button></div>';
      var palette = extra.querySelector('#puzzlePalette');
      CEC.utils.shuffle([...lv.answers]).forEach(function (s) {
        var el = document.createElement('div');
        el.className = 'game-palette-item';
        el.textContent = s;
        el.style.fontSize = '14px';
        el.style.fontWeight = '700';
        el.dataset.val = s;
        el.addEventListener('click', function () {
          for (var r = 0; r < filled.length; r++) {
            for (var c = 0; c < filled[r].length; c++) {
              if (filled[r][c] === 0) {
                filled[r][c] = s;
                el.style.opacity = '0.3';
                el.style.pointerEvents = 'none';
                return;
              }
            }
          }
        });
        palette.appendChild(el);
      });
      extra.querySelector('#puzzleReset').addEventListener('click', function () {
        filled = lv.grid.map(function (row) { return row.map(function (v) { return v; }); });
        palette.querySelectorAll('.game-palette-item').forEach(function (e) { e.style.opacity = '1'; e.style.pointerEvents = 'auto'; });
      });
      extra.querySelector('#puzzleCheck').addEventListener('click', function () {
        var correct = true;
        for (var r = 0; r < filled.length; r++) for (var c = 0; c < filled[r].length; c++) {
          if (filled[r][c] === 0) { correct = false; break; }
        }
        if (correct) {
          score++;
          CEC.ui.showFeedback(canvas, '✅');
          CEC.ui.createSparkle(W / 2, H / 2, canvasWrap);
        } else {
          CEC.ui.showFeedback(canvas, '❌');
        }
        scoreEl.textContent = '⭐ ' + score;
        round++;
        setTimeout(newRound, 900);
      });
    }

    var angle = 0;
    var rafId = null;
    function render() {
      angle += 0.015;
      ctx.clearRect(0, 0, W, H);
      if (round < total) {
        var lv = levels[round];
        var cols = lv.grid[0].length;
        var rows = lv.grid.length;
        var cellSize = Math.min((W - 40) / cols, (H - 40) / rows, 80);
        var ox = (W - cols * cellSize) / 2;
        var oy = (H - rows * cellSize) / 2;
        for (var r = 0; r < rows; r++) {
          for (var c = 0; c < cols; c++) {
            var cx = ox + c * cellSize + cellSize / 2;
            var cy = oy + r * cellSize + cellSize / 2;
            var teeth = filled[r][c];
            if (teeth > 0) {
              var radius = cellSize * 0.35;
              var dir = (r + c) % 2 === 0 ? 1 : -1;
              CEC.canvas.drawGear(ctx, cx, cy, radius, teeth, angle * dir, '#FF6B35', '#fff');
            } else {
              ctx.beginPath();
              ctx.arc(cx, cy, cellSize * 0.35, 0, Math.PI * 2);
              ctx.strokeStyle = '#ddd';
              ctx.lineWidth = 3;
              ctx.setLineDash([5, 5]);
              ctx.stroke();
              ctx.setLineDash([]);
              CEC.canvas.drawLabel(ctx, '?', cx, cy, '#ccc');
            }
          }
        }
      }
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GameFind ---
  CEC.games.Find = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var setup = CEC.canvas.setupCanvas(canvas, 0.6);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0;
    var total = config.total || 6;
    var levels = config.levels || [
      { text: '🔍 点击图中的齿轮', type: 'gear', regions: [{ x: 0.3, y: 0.4, r: 0.12 }, { x: 0.55, y: 0.5, r: 0.1 }] },
      { text: '🔍 点击图中的链条', type: 'chain', regions: [{ x: 0.45, y: 0.35, r: 0.15 }] },
      { text: '🔍 点击图中的传动带', type: 'belt', regions: [{ x: 0.5, y: 0.55, r: 0.15 }] },
      { text: '🔍 点击图中的连杆', type: 'rod', regions: [{ x: 0.65, y: 0.4, r: 0.12 }] },
      { text: '🔍 点击图中的齿轮', type: 'gear', regions: [{ x: 0.4, y: 0.6, r: 0.1 }, { x: 0.7, y: 0.35, r: 0.08 }] },
      { text: '🔍 点击图中的传动带', type: 'belt', regions: [{ x: 0.5, y: 0.5, r: 0.18 }] }
    ];

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 找完了！得分: ' + score + '/' + total; return; }
      goalEl.textContent = levels[round].text;
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
    }

    canvas.onclick = function (e) {
      if (round >= total) return;
      var rect = canvas.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width;
      var y = (e.clientY - rect.top) / rect.height;
      var lv = levels[round];
      var hit = false;
      for (var i = 0; i < lv.regions.length; i++) {
        var reg = lv.regions[i];
        if (CEC.utils.dist(x, y, reg.x, reg.y) < reg.r) { hit = true; break; }
      }
      if (hit) {
        score++;
        CEC.ui.showFeedback(canvas, '✅');
        CEC.ui.createSparkle(e.clientX - rect.left, e.clientY - rect.top, canvasWrap);
      } else {
        CEC.ui.showFeedback(canvas, '❌');
      }
      scoreEl.textContent = '⭐ ' + score;
      round++;
      setTimeout(newRound, 700);
    };

    var t = 0;
    var rafId = null;
    function render() {
      t += 0.02;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#f0f0f0';
      ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = '#888';
      ctx.fillRect(W * 0.1, H * 0.7, W * 0.8, H * 0.08);
      ctx.fillStyle = '#555';
      ctx.fillRect(W * 0.12, H * 0.5, W * 0.12, H * 0.2);
      CEC.canvas.drawLabel(ctx, '电机', W * 0.18, H * 0.6, '#fff');
      CEC.canvas.drawGear(ctx, W * 0.3, H * 0.4, W * 0.08, 12, t, '#FF6B35', '#fff');
      CEC.canvas.drawGear(ctx, W * 0.45, H * 0.5, W * 0.06, 8, -t * 1.5, '#FF9800', '#fff');
      ctx.beginPath();
      ctx.moveTo(W * 0.5, H * 0.35);
      ctx.lineTo(W * 0.7, H * 0.35);
      ctx.strokeStyle = '#8B6F57';
      ctx.lineWidth = 6;
      ctx.setLineDash([4, 3]);
      ctx.lineDashOffset = -t * 20;
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.beginPath();
      ctx.ellipse(W * 0.5, H * 0.55, W * 0.15, H * 0.06, 0, 0, Math.PI * 2);
      ctx.strokeStyle = '#2196F3';
      ctx.lineWidth = 4;
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(W * 0.65, H * 0.4);
      ctx.lineTo(W * 0.8, H * 0.5);
      ctx.strokeStyle = '#4CAF50';
      ctx.lineWidth = 5;
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(W * 0.65, H * 0.4, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#4CAF50'; ctx.fill();
      ctx.beginPath();
      ctx.arc(W * 0.8, H * 0.5, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#4CAF50'; ctx.fill();
      CEC.canvas.drawLabel(ctx, '⚙️齿轮', W * 0.37, H * 0.28, '#E8751A');
      CEC.canvas.drawLabel(ctx, '⛓️链条', W * 0.6, H * 0.28, '#8B6F57');
      CEC.canvas.drawLabel(ctx, '🏗️传动带', W * 0.5, H * 0.68, '#1565C0');
      CEC.canvas.drawLabel(ctx, '🔗连杆', W * 0.75, H * 0.38, '#2E7D32');
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // --- GameBuild ---
  CEC.games.Build = function (destEl, config) {
    config = config || {};

    var area = document.createElement('div');
    area.className = 'card game-area';
    destEl.appendChild(area);

    var header = document.createElement('div');
    header.className = 'game-header';
    var scoreEl = document.createElement('span');
    scoreEl.className = 'game-score';
    var progressEl = document.createElement('span');
    progressEl.className = 'game-progress';
    header.appendChild(scoreEl);
    header.appendChild(progressEl);
    area.appendChild(header);

    var goalEl = document.createElement('div');
    goalEl.className = 'game-goal';
    area.appendChild(goalEl);

    var canvasWrap = document.createElement('div');
    canvasWrap.className = 'game-canvas-wrap';
    var canvas = document.createElement('canvas');
    canvasWrap.appendChild(canvas);
    var feedback = document.createElement('div');
    feedback.className = 'game-feedback';
    canvasWrap.appendChild(feedback);
    area.appendChild(canvasWrap);

    var extra = document.createElement('div');
    area.appendChild(extra);

    var setup = CEC.canvas.setupCanvas(canvas, 0.55);
    var ctx = setup.ctx, W = setup.W, H = setup.H;

    var round = 0, score = 0;
    var total = config.total || 4;
    var levels = config.levels || [
      { text: '🏭 组装一个能快速转动的机器', required: ['gear_big', 'gear_small'], hint: '大齿轮带动小齿轮 = 变快' },
      { text: '🏭 组装一个能举起重物的机器', required: ['gear_small', 'gear_big'], hint: '小齿轮带动大齿轮 = 有力' },
      { text: '🏭 用链条连接两个轴', required: ['chain', 'sprocket', 'sprocket'], hint: '链条连接两个链轮' },
      { text: '🏭 组装一个传动带机器', required: ['belt', 'pulley', 'pulley'], hint: '皮带连接两个皮带轮' }
    ];
    var parts = config.parts || [
      { id: 'gear_big', emoji: '⚙️', name: '大齿轮', size: 50 },
      { id: 'gear_small', emoji: '⚙️', name: '小齿轮', size: 35 },
      { id: 'chain', emoji: '⛓️', name: '链条', size: 40 },
      { id: 'belt', emoji: '🔗', name: '传动带', size: 40 },
      { id: 'sprocket', emoji: '⚙️', name: '链轮', size: 38 },
      { id: 'pulley', emoji: '🔵', name: '皮带轮', size: 38 },
      { id: 'motor', emoji: '🔴', name: '电机', size: 40 },
      { id: 'rod', emoji: '📏', name: '连杆', size: 40 }
    ];
    var placedParts = [];

    function newRound() {
      if (round >= total) { goalEl.textContent = '🎉 创造完成！得分: ' + score + '/' + total; extra.innerHTML = ''; return; }
      var lv = levels[round];
      placedParts = [];
      goalEl.textContent = lv.text + '\n💡 ' + lv.hint;
      scoreEl.textContent = '⭐ ' + score;
      progressEl.textContent = (round + 1) + ' / ' + total;
      extra.innerHTML = '<div class="game-palette" id="buildPalette"></div>' +
        '<div style="text-align:center;margin:6px 0;font-size:13px;color:#888">点击零件添加到机器中</div>' +
        '<div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap;min-height:50px;padding:8px;background:#f9f9f9;border-radius:12px;margin:0 8px" id="buildSlots"></div>' +
        '<div style="text-align:center;margin-top:8px"><button class="btn btn-success" id="buildRun">▶ 运行</button> <button class="btn btn-warning" id="buildReset">重置</button></div>';
      var palette = extra.querySelector('#buildPalette');
      parts.forEach(function (p) {
        var el = document.createElement('div');
        el.className = 'game-palette-item';
        el.textContent = p.emoji;
        el.title = p.name;
        el.addEventListener('click', function () {
          placedParts.push(p.id);
          updateBuildSlots();
        });
        palette.appendChild(el);
      });
      function updateBuildSlots() {
        var slots = extra.querySelector('#buildSlots');
        slots.innerHTML = placedParts.map(function (id) {
          var p = parts.find(function (x) { return x.id === id; });
          return '<div style="width:40px;height:40px;border-radius:10px;background:#fff;border:2px solid #ddd;display:flex;align-items:center;justify-content:center;font-size:20px">' + p.emoji + '</div>';
        }).join('');
        if (placedParts.length === 0) slots.innerHTML = '<span style="color:#ccc;font-size:13px">点击上方零件添加...</span>';
      }
      updateBuildSlots();
      extra.querySelector('#buildReset').addEventListener('click', function () { placedParts = []; updateBuildSlots(); });
      extra.querySelector('#buildRun').addEventListener('click', function () {
        var req = [...lv.required].sort();
        var got = [...placedParts].sort();
        var ok = req.length === got.length && req.every(function (v, i) { return v === got[i]; });
        if (ok) {
          score++;
          CEC.ui.showFeedback(canvas, '✅');
          CEC.ui.createSparkle(W / 2, H / 2, canvasWrap);
        } else {
          CEC.ui.showFeedback(canvas, '❌');
          goalEl.textContent = '❌ 还不对！需要: ' + lv.required.map(function (id) { return parts.find(function (p) { return p.id === id; }).name; }).join(', ') + '\n💡 ' + lv.hint;
        }
        scoreEl.textContent = '⭐ ' + score;
        round++;
        setTimeout(newRound, 1200);
      });
    }

    var t = 0;
    var rafId = null;
    function render() {
      t += 0.02;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#f5f5f5';
      ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = '#ddd';
      ctx.lineWidth = 2;
      ctx.setLineDash([8, 4]);
      ctx.strokeRect(10, 10, W - 20, H - 20);
      ctx.setLineDash([]);
      if (round < total) {
        placedParts.forEach(function (id, i) {
          var p = parts.find(function (x) { return x.id === id; });
          var x = 40 + (i % 6) * 60;
          var y = Math.floor(i / 6) * 60 + 40;
          ctx.font = '28px sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(p.emoji, x, y);
        });
        if (placedParts.length === 0) {
          CEC.canvas.drawLabel(ctx, '🏭 在下方选择零件组装机器', W / 2, H / 2, '#ccc');
        }
      }
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);
    newRound();

    return {
      destroy: function () { if (rafId) cancelAnimationFrame(rafId); area.remove(); }
    };
  };

  // ====================================================================
  // 7. Section Builders (CEC.sections.*)
  // ====================================================================
  CEC.sections = {};

  CEC.sections.buildKnowledgeSections = function (containerEl, sectionConfigs) {
    var allSections = [];
    sectionConfigs.forEach(function (sec) {
      var el = document.createElement('section');
      el.className = 'section';
      el.id = 'sec-' + sec.id;
      el.innerHTML =
        '<div class="section-inner">' +
        '<div class="sec-icon">' + sec.icon + '</div>' +
        '<h2 class="sec-title">' + sec.title + '</h2>' +
        '<p class="sec-desc">' + sec.desc + '</p>' +
        '<div class="card" id="canvas-' + sec.id + '">' +
        '<canvas id="cv-' + sec.id + '"></canvas>' +
        '</div>' +
        '<div id="controls-' + sec.id + '"></div>' +
        '</div>';
      containerEl.appendChild(el);
      allSections.push(el);
    });
    return allSections;
  };

  CEC.sections.buildGameSections = function (containerEl, gameConfigs) {
    var allSections = [];
    gameConfigs.forEach(function (game) {
      var el = document.createElement('section');
      el.className = 'section';
      el.id = 'sec-' + game.id;
      el.innerHTML =
        '<div class="section-inner">' +
        '<div class="sec-icon">' + game.icon + '</div>' +
        '<h2 class="sec-title">' + game.title + '</h2>' +
        '<p class="sec-desc">' + game.desc + ' <span style="color:#999;font-size:12px">[' + game.difficulty + ']</span></p>' +
        '<div class="card game-area" id="area-' + game.id + '">' +
        '<div class="game-header">' +
        '<span class="game-score" id="score-' + game.id + '">⭐ 0</span>' +
        '<span class="game-progress" id="progress-' + game.id + '">1 / 5</span>' +
        '</div>' +
        '<div class="game-goal" id="goal-' + game.id + '"></div>' +
        '<div class="game-canvas-wrap">' +
        '<canvas id="cv-' + game.id + '"></canvas>' +
        '<div class="game-feedback"></div>' +
        '</div>' +
        '<div id="game-extra-' + game.id + '"></div>' +
        '</div>' +
        '</div>';
      containerEl.appendChild(el);
      allSections.push(el);
    });
    return allSections;
  };

  CEC.sections.buildSummary = function (containerEl, topics) {
    var grid = document.createElement('div');
    grid.className = 'summary-grid';
    grid.innerHTML = topics.map(function (t) {
      return '<div class="summary-card"><div class="icon">' + t.icon + '</div><div class="label">' + t.label + '</div><div class="value">' + t.value + '</div></div>';
    }).join('');
    containerEl.appendChild(grid);
    return grid;
  };

  // ====================================================================
  // 8. Navigation (CEC.nav.*)
  // ====================================================================
  CEC.nav = {};

  CEC.nav.initNavDots = function (containerEl, sections, onDotClick) {
    var dots = [];
    sections.forEach(function (sec, i) {
      var dot = document.createElement('button');
      dot.className = 'nav-dot';
      dot.title = sec.querySelector('.sec-title') ? sec.querySelector('.sec-title').textContent : 'Section';
      dot.addEventListener('click', function () {
        if (onDotClick) onDotClick(i);
        sec.scrollIntoView({ behavior: 'smooth' });
      });
      containerEl.appendChild(dot);
      dots.push(dot);
    });
    return dots;
  };

  CEC.nav.initScrollObserver = function (sections, dots) {
    var currentSection = 0;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          var idx = sections.indexOf(entry.target);
          if (idx >= 0) {
            currentSection = idx;
            dots.forEach(function (d, i) { d.classList.toggle('active', i === idx); });
          }
        }
      });
    }, { threshold: 0.2 });
    sections.forEach(function (sec) { observer.observe(sec); });
    return { observer: observer, getCurrentSection: function () { return currentSection; } };
  };

  // ====================================================================
  // 9. Factory API (CEC.create / CEC.createGame)
  // ====================================================================
  var componentMap = {
    InteractiveGear: CEC.components.InteractiveGear,
    GearPair: CEC.components.GearPair,
    ChainDrive: CEC.components.ChainDrive,
    Linkage: CEC.components.Linkage,
    BeltDrive: CEC.components.BeltDrive,
    GearLab: CEC.components.GearLab
  };

  var gameMap = {
    Match: CEC.games.Match,
    Fix: CEC.games.Fix,
    Chain: CEC.games.Chain,
    Sort: CEC.games.Sort,
    Speed: CEC.games.Speed,
    Puzzle: CEC.games.Puzzle,
    Find: CEC.games.Find,
    Build: CEC.games.Build
  };

  CEC.create = function (name, destEl, config) {
    var Factory = componentMap[name];
    if (!Factory) throw new Error('CEC: Unknown component "' + name + '"');
    return Factory(destEl, config || {});
  };

  CEC.createGame = function (name, destEl, config) {
    var Factory = gameMap[name];
    if (!Factory) throw new Error('CEC: Unknown game "' + name + '"');
    return Factory(destEl, config || {});
  };

  // ====================================================================
  // 10. Hero Background Gears
  // ====================================================================
  CEC.initHeroGears = function (canvas) {
    var ctx = canvas.getContext('2d');
    var W, H;
    function resize() {
      W = window.innerWidth;
      H = window.innerHeight;
      canvas.width = W;
      canvas.height = H;
    }
    resize();
    window.addEventListener('resize', resize);

    var gears = [
      { x: 0.1, y: 0.2, r: 40, t: 10, speed: 0.01, color: 'rgba(255,255,255,0.3)' },
      { x: 0.85, y: 0.15, r: 30, t: 8, speed: -0.015, color: 'rgba(255,255,255,0.2)' },
      { x: 0.15, y: 0.8, r: 50, t: 12, speed: 0.008, color: 'rgba(255,255,255,0.15)' },
      { x: 0.9, y: 0.75, r: 35, t: 9, speed: -0.012, color: 'rgba(255,255,255,0.2)' },
      { x: 0.5, y: 0.1, r: 25, t: 7, speed: 0.02, color: 'rgba(255,255,255,0.15)' }
    ];
    var angles = gears.map(function () { return 0; });
    var rafId = null;

    function render() {
      ctx.clearRect(0, 0, W, H);
      gears.forEach(function (g, i) {
        angles[i] += g.speed;
        CEC.canvas.drawGear(ctx, g.x * W, g.y * H, g.r, g.t, angles[i], g.color, 'transparent');
      });
      rafId = requestAnimationFrame(render);
    }
    rafId = requestAnimationFrame(render);

    return {
      destroy: function () {
        if (rafId) cancelAnimationFrame(rafId);
        window.removeEventListener('resize', resize);
      }
    };
  };

  // ====================================================================
  // 11. Boot (CEC.boot)
  // ====================================================================
  CEC.boot = function (config) {
    config = config || {};
    var topic = config.topic || {};
    var games = config.games || [];
    var sections = topic.sections || [];

    // Apply theme
    if (topic.heroColor) {
      document.documentElement.style.setProperty('--primary', topic.heroColor);
      document.documentElement.style.setProperty('--hero-color', topic.heroColor);
    }

    // Build DOM
    var knowledgeContainer = config.knowledgeContainer;
    var gameContainer = config.gameContainer;
    var summaryContainer = config.summaryContainer;
    var navContainer = config.navContainer;

    var allSections = [];

    if (knowledgeContainer) {
      var kSections = CEC.sections.buildKnowledgeSections(knowledgeContainer, sections);
      allSections = allSections.concat(kSections);
    }
    if (gameContainer) {
      var gSections = CEC.sections.buildGameSections(gameContainer, games);
      allSections = allSections.concat(gSections);
    }

    // Summary
    if (summaryContainer && config.summaryTopics) {
      CEC.sections.buildSummary(summaryContainer, config.summaryTopics);
    }

    // Nav
    var dots = [];
    var scrollObs = null;
    if (navContainer && allSections.length > 0) {
      dots = CEC.nav.initNavDots(navContainer, allSections);
      scrollObs = CEC.nav.initScrollObserver(allSections, dots);
    }

    // Hero
    if (config.heroCanvas) {
      CEC.initHeroGears(config.heroCanvas);
    }

    return {
      sections: allSections,
      dots: dots,
      scrollObserver: scrollObs,
      destroy: function () {
        if (scrollObs && scrollObs.observer) scrollObs.observer.disconnect();
      }
    };
  };

})();
