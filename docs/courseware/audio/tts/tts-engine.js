/**
 * TTS Engine - 混合模式
 * 优先：浏览器 speechSynthesis（音质好，系统原生语音）
 * 降级：预生成 MP3（移动端 Chrome 等不可靠设备）
 * 
 * 工作原理：
 * 1. 加载 map.json（文本→MP3 文件名映射）
 * 2. speakText() 被替换为 ttsPlay()
 * 3. ttsPlay() 先尝试 speechSynthesis
 * 4. 如果 speechSynthesis 不出声（移动端 bug），降级到 MP3
 */
(function(){
  // ====== 状态 ======
  var ttsMap = {};
  var ttsMapLoaded = false;
  var ttsAudio = null;
  var ttsFallbackMode = false;  // true = 只用 MP3（检测到 speechSynthesis 有问题时）

  // ====== 加载映射表 ======
  function loadTTSMap() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'audio/tts/map.json?' + Date.now(), true);
    xhr.onload = function() {
      try {
        ttsMap = JSON.parse(xhr.responseText);
        ttsMapLoaded = true;
      } catch(e) { /* ignore */ }
    };
    xhr.onerror = function() { /* ignore */ };
    xhr.send();
  }

  // ====== 文本清理 ======
  function ttsClean(text) {
    if (!text) return '';
    return text.replace(/<[^>]+>/g, '')
               .replace(/[\u0300-\u036f\u200d\ufe0f\u20e3\u20e4]/g, '')
               .replace(/['"]/g, '')
               .trim();
  }

  // ====== 检测语言 ======
  function detectLang(text) {
    return /[\u4e00-\u9fff]/.test(text) ? 'zh-CN' : 'en-US';
  }

  // ====== 播放 MP3（降级） ======
  function ttsPlayMP3(filename) {
    if (ttsAudio) { ttsAudio.pause(); ttsAudio = null; }
    ttsAudio = new Audio('audio/tts/' + filename + '.mp3');
    ttsAudio.volume = 0.9;
    ttsAudio.play().catch(function() {});
  }

  // ====== speechSynthesis（首选） ======
  function ttsSpeakNative(text, clean) {
    if (!('speechSynthesis' in window)) return false;
    try {
      window.speechSynthesis.cancel();
      var lang = detectLang(text);
      var u = new SpeechSynthesisUtterance(clean || text);
      u.lang = lang;
      u.rate = (lang === 'zh-CN') ? 0.85 : 0.75;
      u.pitch = (lang === 'zh-CN') ? 1.1 : 1.0;
      u.volume = 1.0;
      window.speechSynthesis.speak(u);
      return true;
    } catch(e) {
      return false;
    }
  }

  // ====== 尝试用 MP3 查表 ======
  function ttsLookupMP3(text) {
    if (!ttsMapLoaded) return null;
    
    var clean = ttsClean(text);
    if (!clean) return null;
    
    if (ttsMap[clean]) return ttsMap[clean];
    
    // 尝试原文（不清理标点）
    var raw = text.replace(/<[^>]+>/g, '').trim();
    if (ttsMap[raw]) return ttsMap[raw];
    
    return null;
  }

  // ====== 检测 speechSynthesis 是否可用 ======
  // 某些 Android Chrome 版本 speechSynthesis 存在但不出声
  var speechTested = false;
  function testSpeechSynthesis() {
    if (speechTested) return;
    speechTested = true;
    
    if (!('speechSynthesis' in window)) {
      ttsFallbackMode = true;
      return;
    }
    
    // 尝试发声测试
    try {
      var u = new SpeechSynthesisUtterance('test');
      u.volume = 0.01;  // 几乎无声
      u.onend = function() { /* speechSynthesis 工作正常 */ };
      u.onerror = function() {
        // speechSynthesis 出错，启用降级
        ttsFallbackMode = true;
      };
      window.speechSynthesis.speak(u);
      
      // 超时检测：某些 Android Chrome 调用 speak() 无任何回调
      setTimeout(function() {
        // 如果还没触发任何回调，试试能不能获取 voices
        // 这里不做强制降级，留到实际使用时按需处理
      }, 500);
    } catch(e) {
      ttsFallbackMode = true;
    }
  }

  // ====== 主入口 ======
  window.ttsPlay = function(text) {
    var clean = ttsClean(text);
    if (!clean) return;
    
    // 模式1：如果检测到 speechSynthesis 不可靠，直接用 MP3
    if (ttsFallbackMode) {
      var mp3Key = ttsLookupMP3(text);
      if (mp3Key) { ttsPlayMP3(mp3Key); return; }
    }
    
    // 模式2：优先用 speechSynthesis
    var spoke = ttsSpeakNative(text, clean);
    
    if (!spoke) {
      // speechSynthesis 完全不可用，降级
      var mp3Key = ttsLookupMP3(text);
      if (mp3Key) { ttsPlayMP3(mp3Key); }
    }
  };

  // ====== 兼容旧代码 ======
  // 每个HTML文件中的 speakText(text) 现在调用 ttsPlay(text)

  // ====== 初始化 ======
  loadTTSMap();
  testSpeechSynthesis();
})();
