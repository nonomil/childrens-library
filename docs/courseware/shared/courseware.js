(function(){
  "use strict";
  
  var LANG = window.COURSEWARE_LANG || "zh-CN";
  var SWIPE_THRESHOLD = window.COURSEWARE_SWIPE_THRESHOLD || 50;
  var curPage = 0;
  var totalPages = 0;
  var touchX = 0;
  var currentAudio = null;
  var isSpeaking = false;

  /* ============ SPEAK MODULE ============ */
  window.playClick = function(src, text) {
    stopSpeaking();
    var a = new Audio(src);
    a.onerror = function() { speakTTS(text); };
    a.play().catch(function(){ speakTTS(text); });
    currentAudio = a;
  };

  function speakTTS(text) {
    if (!window.speechSynthesis || !text) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = LANG; u.rate = 0.85;
    window.speechSynthesis.speak(u);
  }

  window.speakPage = function() {
    if (!window.speechSynthesis) return;
    var el = document.querySelector(".page.active, .content.active, .slide.active");
    if (!el) return;
    var t = (el.innerText || "").replace(/\s+/g, " ").trim();
    if (t.length < 2) return;
    stopSpeaking();
    var u = new SpeechSynthesisUtterance(t);
    u.lang = LANG; u.rate = 0.85;
    u.onstart = function(){ isSpeaking = true; };
    u.onend = u.onerror = function(){ isSpeaking = false; };
    window.speechSynthesis.speak(u);
  };

  window.stopSpeaking = function() {
    if (currentAudio) { currentAudio.pause(); currentAudio = null; }
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    isSpeaking = false;
  };

  /* ============ NAVIGATION MODULE ============ */
  window.navGoTo = function(n) {
    if (n < 0 || n >= totalPages) return;
    var pages = document.querySelectorAll(".page, .content, .slide");
    if (pages.length === 0) return;
    pages.forEach(function(p, i) {
      p.classList.toggle("active", i === n);
    });
    curPage = n;
    updateDots();
    stopSpeaking();
    if (typeof window.onPageChange === "function") window.onPageChange(n);
  };

  window.navPrev = function() { window.navGoTo(curPage - 1); };
  window.navNext = function() { window.navGoTo(curPage + 1); };

  function updateDots() {
    document.querySelectorAll(".dot").forEach(function(d, i) {
      d.classList.toggle("active", i === curPage);
    });
    var prev = document.getElementById("prevBtn");
    if (prev) prev.disabled = curPage === 0;
  }

  window.navSpeakCurrentPage = function() {
    var btn = document.getElementById("speakBtn") || document.querySelector(".speak-btn, .btn-speak, .read-btn");
    if (btn) btn.click();
  };

  /* ============ TOUCH SWIPE ============ */
  document.addEventListener("touchstart", function(e) {
    touchX = e.changedTouches[0].screenX;
  }, { passive: true });

  document.addEventListener("touchend", function(e) {
    var diff = touchX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > SWIPE_THRESHOLD) {
      diff > 0 ? window.navNext() : window.navPrev();
    }
  }, { passive: true });

  /* ============ KEYBOARD ============ */
  document.addEventListener("keydown", function(e) {
    if (e.key === "ArrowRight") window.navNext();
    else if (e.key === "ArrowLeft") window.navPrev();
    else if (e.key === "Home") window.navGoTo(0);
  });

  /* ============ CONFETTI ============ */
  window.celebrate = function() {
    if (typeof gsap === "undefined") return;
    var colors = ["#ff6b6b","#ffd93d","#6bcb77","#4d96ff","#ff9ff3","#f368e0","#ffa502"];
    for (var i = 0; i < 60; i++) {
      var el = document.createElement("div");
      el.className = "confetti-piece";
      el.style.background = colors[i % colors.length];
      el.style.left = Math.random() * 100 + "vw";
      el.style.top = "-10px";
      document.body.appendChild(el);
      gsap.to(el, {
        y: window.innerHeight + 20,
        x: (Math.random() - 0.5) * 200,
        rotation: Math.random() * 720 - 360,
        scale: 0.5 + Math.random(),
        duration: 1.5 + Math.random(),
        delay: Math.random() * 0.5,
        ease: "power2.out",
        onComplete: function() { el.remove(); }
      });
    }
  };

  /* ============ INIT ============ */
  function init() {
    totalPages = window.COURSEWARE_PAGES || document.querySelectorAll(".page, .content, .slide").length;
    updateDots();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

})();
