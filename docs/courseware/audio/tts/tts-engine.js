/**
 * TTS Engine - 用预生成MP3代替浏览器speechSynthesis
 * 解决移动端Chrome语音合成不发音的问题
 * 
 * 工作原理：
 * 1. 加载时请求 map.json 获取文本 -> MP3 文件名映射
 * 2. speakText() 被替换为 ttsPlay()，先查映射表
 * 3. 命中 → 播放预生成 MP3
 * 4. 未命中 → 降级到 speechSynthesis
 */
(function(){
  var ttsMap = {};
  var ttsMapLoaded = false;
  var ttsAudio = null;

  // 加载映射表
  function loadTTSMap() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'audio/tts/map.json?' + Date.now(), true);
    xhr.onload = function() {
      try {
        ttsMap = JSON.parse(xhr.responseText);
        ttsMapLoaded = true;
      } catch(e) {}
    };
    xhr.onerror = function() {};
    xhr.send();
  }

  // 清理文本：去HTML标签、emoji、首尾空格
  function ttsClean(text) {
    if (!text) return '';
    return text.replace(/<[^>]+>/g, '')
               .replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, '')
               .replace(/[\u0300-\u036f\u200d\ufe0f\u20e3\u20e4]/g, '')
               .replace(/['"]/g, '')
               .trim();
  }

  // 播放 MP3
  function ttsPlayMP3(filename) {
    if (ttsAudio) {
      ttsAudio.pause();
      ttsAudio = null;
    }
    ttsAudio = new Audio('audio/tts/' + filename + '.mp3');
    ttsAudio.volume = 0.9;
    ttsAudio.play().catch(function(err) {
      // 播放失败（浏览器限制等），静默处理
    });
  }

  // 降级：使用浏览器 speechSynthesis
  function ttsFallback(text) {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      var u = new SpeechSynthesisUtterance(text);
      // 判断语言
      if (/[\u4e00-\u9fff]/.test(text)) {
        u.lang = 'zh-CN';
        u.rate = 0.85;
        u.pitch = 1.1;
      } else {
        u.lang = 'en-US';
        u.rate = 0.75;
        u.pitch = 1.0;
      }
      u.volume = 1.0;
      window.speechSynthesis.speak(u);
    }
  }

  // 主入口：TTS 播放
  window.ttsPlay = function(text) {
    var clean = ttsClean(text);
    if (!clean) return;

    // 先查映射表
    if (ttsMapLoaded && ttsMap[clean]) {
      ttsPlayMP3(ttsMap[clean]);
      return;
    }

    // 映射表还没加载好，也有可能就是没有映射
    // 再试一次用精确的文本匹配（包括可能包含的标点）
    if (ttsMapLoaded) {
      // 尝试原文本（不清理标点）
      var raw = text.replace(/<[^>]+>/g, '').trim();
      if (ttsMap[raw]) {
        ttsPlayMP3(ttsMap[raw]);
        return;
      }
    }

    // 降级到 speechSynthesis
    ttsFallback(clean);
  };

  // 兼容旧代码：全局 speakText 改名引用
  // (每个HTML文件中的 speakText 函数体会被替换为 ttsPlay(text);)

  // 初始化加载映射表
  loadTTSMap();
})();
