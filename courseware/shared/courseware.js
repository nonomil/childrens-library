/**
 * courseware.js — Shared utility library for children's educational courseware
 * 
 * OPT-IN only: defines functions but does NOT auto-bind events.
 * Each file chooses what to use by calling the functions it needs.
 * 
 * Usage:
 *   <script src="shared/courseware.js"></script>
 *   <script>
 *     // Use what you need, ignore the rest:
 *     playClick('audio/sound.mp3', 'hello');    // MP3→TTS fallback
 *     speakPage();                                // Read current page aloud
 *     celebrate();                                // Confetti celebration
 *     initSwipe();                                // Enable touch swipe (if file has no touch handler)
 *     initKeyboard();                             // Enable keyboard nav (if file has no keyboard handler)
 *     navGoTo(3);                                 // Navigate (if file uses this naming)
 *   </script>
 */

(function(){
  "use strict";

  /* ===== CONFIG ===== */
  var LANG = window.COURSEWARE_LANG || "zh-CN";

  /* ===== SPEAK MODULE ===== */
  var currentAudio = null;

  /**
   * Play a word/phrase with MP3 audio, fallback to TTS
   * @param {string} src - MP3 file path (e.g. "audio/char-yun.mp3")
   * @param {string} text - Text to speak as fallback (e.g. "云")
   */
  window.playClick = function(src, text) {
    stopSpeaking();
    var a = new Audio(src);
    a.onerror = function() { speakTTS(text); };
    a.play().catch(function(){ speakTTS(text); });
    currentAudio = a;
  };

  /** Internal TTS fallback */
  function speakTTS(text) {
    if (!window.speechSynthesis || !text) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = LANG; u.rate = 0.85;
    window.speechSynthesis.speak(u);
  }

  /**
   * Read current active page content aloud
   * Finds .page.active, .content.active, or .slide.active
   */
  window.speakPage = function() {
    if (!window.speechSynthesis) return;
    var el = document.querySelector(".page.active, .content.active, .slide.active, #page" + (window.curPage || 0));
    if (!el) {
      // Try slide-based pages
      el = document.querySelector(".slide.active") || document.querySelector(".book-page.active");
    }
    if (!el) return;
    var t = (el.innerText || "").replace(/\s+/g, " ").trim();
    if (t.length < 2) return;
    stopSpeaking();
    var u = new SpeechSynthesisUtterance(t);
    u.lang = LANG; u.rate = 0.85;
    window.speechSynthesis.speak(u);
  };

  /** Stop any current audio or speech */
  window.stopSpeaking = function() {
    if (currentAudio) { currentAudio.pause(); currentAudio = null; }
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  };

  /* ===== NAVIGATION MODULE (Optional) ===== */
  /** 
   * Go to page n (0-indexed) using .page/.content/.slide active class toggle
   * Only works if the file uses this page class structure
   */
  window.navGoTo = function(n) {
    var totalPages = window.COURSEWARE_PAGES || 0;
    var pages = document.querySelectorAll(".page, .content, .slide");
    if (pages.length > 0) totalPages = pages.length;
    if (n < 0 || n >= totalPages) return;
    pages.forEach(function(p, i) { p.classList.toggle("active", i === n); });
    window.curPage = n;
    window.stopSpeaking();
    // Update dots if they exist
    document.querySelectorAll(".dot").forEach(function(d, i) { d.classList.toggle("active", i === n); });
    var prev = document.getElementById("prevBtn");
    if (prev) prev.disabled = n === 0;
    if (typeof window.onPageChange === "function") window.onPageChange(n);
  };

  window.navPrev = function() { window.navGoTo((window.curPage || 0) - 1); };
  window.navNext = function() { window.navGoTo((window.curPage || 0) + 1); };

  window.navSpeakCurrentPage = function() {
    var btn = document.getElementById("speakBtn") || document.querySelector(".speak-btn, .btn-speak, .read-btn");
    if (btn) btn.click();
  };

  /* ===== TOUCH SWIPE MODULE (Opt-in) ===== */
  var touchX = 0;
  var swipeEnabled = false;

  /**
   * Enable touch swipe navigation
   * @param {number} threshold - minimum swipe distance in px (default 50)
   */
  window.initSwipe = function(threshold) {
    if (swipeEnabled) return;
    swipeEnabled = true;
    threshold = threshold || 50;
    
    document.addEventListener("touchstart", function(e) {
      touchX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener("touchend", function(e) {
      var diff = touchX - e.changedTouches[0].screenX;
      if (Math.abs(diff) > threshold) {
        if (typeof window.navNext === 'function' && typeof window.navPrev === 'function') {
          diff > 0 ? window.navNext() : window.navPrev();
        }
      }
    }, { passive: true });
  };

  /* ===== KEYBOARD MODULE (Opt-in) ===== */
  var keyboardEnabled = false;

  /**
   * Enable keyboard navigation (ArrowLeft/Right, Home)
   */
  window.initKeyboard = function() {
    if (keyboardEnabled) return;
    keyboardEnabled = true;
    
    document.addEventListener("keydown", function(e) {
      if (e.key === "ArrowRight" && typeof window.navNext === 'function') window.navNext();
      else if (e.key === "ArrowLeft" && typeof window.navPrev === 'function') window.navPrev();
      else if (e.key === "Home" && typeof window.navGoTo === 'function') window.navGoTo(0);
    });
  };

  /* ===== CONFETTI MODULE ===== */
  /**
   * Celebration confetti burst (requires GSAP loaded globally)
   * Creates 60 colored particles that fall with animation
   */
  window.celebrate = function() {
    if (typeof gsap === "undefined") return;
    var colors = ["#ff6b6b","#ffd93d","#6bcb77","#4d96ff","#ff9ff3","#f368e0","#ffa502"];
    for (var i = 0; i < 60; i++) {
      var el = document.createElement("div");
      el.className = "confetti-piece";
      el.style.cssText = "position:fixed;background:" + colors[i % colors.length] + 
        ";left:" + (Math.random() * 100) + "vw;top:-10px;width:" + (6+Math.random()*8) + 
        "px;height:" + (6+Math.random()*8) + "px;border-radius:" + (Math.random()>.5?"50%":"2px") + 
        ";z-index:9999;pointer-events:none";
      document.body.appendChild(el);
      gsap.to(el, {
        y: window.innerHeight + 20,
        x: (Math.random() - 0.5) * 200,
        rotation: Math.random() * 720 - 360,
        scale: 0.5 + Math.random(),
        duration: 1.5 + Math.random(),
        delay: Math.random() * 0.5,
        ease: "power2.out",
        onComplete: function() { if (el.parentNode) el.remove(); }
      });
    }
  };

})();
