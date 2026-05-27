---
title: 静夜思
description: 李白《静夜思》古诗词学习
---

# 静夜思

<div class="poetry-header">
  <h1>静夜思</h1>
  <p class="author">「唐」李白</p>
  <p class="tags">#月亮 #思乡 #李白 #秋天 #夜晚</p>
</div>

---

## 📜 原诗朗诵

<div class="poem-text">

<p class="poem-line">床前明月光<span class="pinyin">Chuáng qián míng yuè guāng</span></p>
<p class="poem-line">疑是地上霜<span class="pinyin">Yí shì dì shàng shuāng</span></p>
<p class="poem-line">举头望明月<span class="pinyin">Jǔ tóu wàng míng yuè</span></p>
<p class="poem-line">低头思故乡<span class="pinyin">Dī tóu sī gù xiāng</span></p>

</div>

<button class="tts-button" onclick="speakPoem()">🔊 朗读</button>

---

## 📝 现代译文

<div class="translation-box">

明亮的月光洒在床前的窗户上，好像地上泛起了一层霜。我禁不住抬起头来，看那天窗外空中的一轮明月，不由得低头沉思，想起远方的家乡。

</div>

---

## 🏞️ 场景故事


🏞️ **场景描写**：

这是一个深秋的夜晚，诗人独自住在扬州的一家旅舍中。

推开窗户，一轮皎洁的明月高悬夜空，月光如流水般倾泻而下，
洒在床前的地面上。秋夜的凉意让月光看起来如同地上的白霜。

诗人从睡梦中醒来，被这清冷的月光所吸引。他抬头望向明月，
那轮圆月仿佛就是家乡的天空。低头时，思乡之情涌上心头。

🌙 **意象元素**：
- 明月：象征团圆、思念
- 霜：秋夜的清寒、时光的流逝
- 床/井栏：孤独、漂泊
- 故乡：温暖、归属感


---

## 📖 诗人介绍


李白（701年－762年），字太白，号青莲居士，又号「谪仙人」，唐代伟大的浪漫主义诗人，被后人誉为「诗仙」。

这首《静夜思》是李白最脍炙人口的诗作之一，约作于唐玄宗开元十四年（726年）。当时李白26岁，离开家乡四川，
在扬州旅舍写下此诗。诗人在异乡客居，秋夜难眠，望着天上的明月，思念起远方的故乡和亲人。

诗中的「床」并非现代意义上的床，有学者认为是「井栏」或「坐具」之意。但无论如何理解，都不影响这首诗
表达的那份 universal 的思乡之情。


---

## 📝 学习要点


📝 **学习要点**：

1. **朗读技巧**
   - 「明月光」读得轻柔、缓慢
   - 「地上霜」带一点惊讶的语气
   - 「望明月」抬头仰望的感觉
   - 「思故乡」声音渐低，表达思念

2. **生字学习**
   - 床：古代指坐具，今天指睡觉的家具
   - 疑：怀疑、以为
   - 举：抬起
   - 故乡：家乡

3. **文化知识**
   - 中秋节赏月的传统
   - 「月是故乡明」的文化内涵
   - 唐诗的格律（五言绝句）

4. **延伸活动**
   - 画一幅「静夜思」的画
   - 观察月亮，说说月亮像什么
   - 学习「月」字的演变
   - 唱《静夜思》儿歌


---

## 🎨 配图卡片

<div class="card-preview">
  <img src="card.png" alt="静夜思卡片" />
  <p class="card-hint">💡 右键保存图片，可打印成A6卡片</p>
</div>

---

<script>
function speakPoem() {
  const lines = ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"];
  const text = lines.join('，');
  
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.8;
    speechSynthesis.speak(utterance);
  } else {
    alert('您的浏览器不支持语音朗读');
  }
}
</script>

<style>
.poetry-header { text-align: center; padding: 20px 0; }
.poetry-header h1 { font-size: 2.5em; color: #8B4513; margin-bottom: 10px; }
.poetry-header .author { font-size: 1.2em; color: #666; }
.poetry-header .tags { color: #999; margin-top: 10px; }

.poem-text { 
  background: linear-gradient(135deg, #f5f0e6 0%, #faf7f0 100%); 
  padding: 30px; 
  border-radius: 16px; 
  margin: 20px 0;
  text-align: center;
}
.poem-line { 
  font-size: 1.8em; 
  color: #2F4F4F; 
  margin: 20px 0;
  font-weight: bold;
}
.pinyin { 
  display: block; 
  font-size: 0.6em; 
  color: #888; 
  margin-top: 5px;
  font-weight: normal;
}

.translation-box {
  background: #FAF7F0;
  border-left: 4px solid #FFB347;
  padding: 20px;
  margin: 20px 0;
  border-radius: 0 8px 8px 0;
}

.tts-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  margin: 20px 0;
}
.tts-button:hover { opacity: 0.9; }

.card-preview {
  text-align: center;
  padding: 20px;
}
.card-preview img {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.card-hint {
  color: #666;
  margin-top: 15px;
  font-size: 0.9em;
}
</style>
