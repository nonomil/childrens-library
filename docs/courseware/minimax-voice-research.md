# MiniMax 语音 API 调研 — AI 有声绘本制作

> 来源: 小红书笔记 + MiniMax 官方文档  
> 日期: 2026-05-27

## 核心结论

| 能力 | 实现方式 | 效果 |
|------|---------|------|
| **多角色声音** | MiniMax TTS API，每个角色用不同 voice_id | ✅ 5个角色5种声音 |
| **情绪控制** | prompt 描述情绪（"开心地"、"生气地"） | ✅ 同句不同情绪 |
| **背景音乐** | MiniMax Music/Sonic API | ✅ 描述氛围一键生成 |
| **声音克隆** | 上传30秒音频样本 | ✅ 父母声音讲故事 |

---

## 1. MiniMax 语音 API 接入

### 1.1 TTS（文本转语音）

```python
import requests

def minimax_tts(text, voice_id, emotion=""):
    \"\"\"调用 MiniMax TTS 生成语音
    
    Args:
        text: 要朗读的文本
        voice_id: 声音ID（如 "female-01", "male-02"）
        emotion: 情绪描述（如"开心地"、"生气地"）
    \"\"\"
    url = "https://api.minimax.chat/v1/t2a_v2"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "speech-01",
        "text": f"{emotion}{text}" if emotion else text,
        "voice_id": voice_id,
        "audio_format": "mp3",
        "speed": 1.0
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()  # {\"audio_url\": \"...\"}
```

### 1.2 声音克隆（Voice Clone）

```python
def clone_voice(audio_sample_path, name):
    \"\"\"克隆声音 — 上传30秒音频样本\"\"\"
    url = "https://api.minimax.chat/v1/voice_clone"
    
    with open(audio_sample_path, 'rb') as f:
        files = {'audio': f}
        data = {'name': name}
        resp = requests.post(url, headers=headers, files=files, data=data)
    
    return resp.json()  # {\"voice_id\": \"cloned-xxx\"}
```

### 1.3 背景音乐生成

```python
def generate_music(description, duration=30):
    \"\"\"根据描述生成背景音乐\"\"\"
    url = "https://api.minimax.chat/v1/music_generation"
    payload = {
        "model": "music-01",
        "description": description,  # e.g. \"温馨儿童睡前故事背景音乐，轻柔钢琴，梦幻\" 
        "duration": duration,
        \"audio_format\": \"mp3\"
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()
```

---

## 2. 有声绘本制作流程

```
┌─────────────────┐
│ 1. 写剧本       │ → 分角色对话 + 旁白 + 场景描述
│    (ChatGPT)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. 分配声音     │ → 为每个角色选 voice_id 或克隆
│    (MiniMax)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. 生成语音     │ → 逐句调用 TTS，注意情绪标记
│    (MiniMax)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. 生成BGM      │ → 描述场景氛围生成背景音乐
│    (MiniMax)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. 合成编辑     │ → 用 ffmpeg 混合语音+BGM
│    (ffmpeg)     │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 6. 嵌入绘本     │ → HTML5 翻页 + 点击播放
│    (Turn.js)    │
└─────────────────┘
```

---

## 3. 关键参数调优

### 3.1 情绪控制

| 场景 | prompt 写法 |
|------|------------|
| 开心 | `[emotion=happy] 今天天气真好！` |
| 生气 | `[emotion=angry] 你怎么能这样！` |
| 惊讶 | `[emotion=surprised] 哇，真的吗？` |
| 温柔 | `[emotion=gentle] 宝贝，该睡觉啦` |
| 害怕 | `[emotion=scared] 那里有什么东西...` |

### 3.2 语速调节

```python
# 小孩角色 — 慢一点
payload = {..., "speed": 0.85}

# 旁白 — 正常
payload = {..., "speed": 1.0}

# 紧张场景 — 快一点  
payload = {..., "speed": 1.2}
```

---

## 4. 替代方案

| 方案 | 特点 | 适用 |
|------|------|------|
| **MiniMax** | 中文强、情绪丰富 | 中文绘本首选 |
| **ElevenLabs** | 英文强、克隆效果好 | 英文内容 |
| **Azure TTS** | 稳定、SSML精细 | 企业级应用 |
| **OpenAI TTS** | 简单、性价比高 | 快速原型 |
| **Edge TTS** | 免费、离线可用 | 预算有限 |

---

## 5. 完整代码示例：自动生成有声绘本

```python
#!/usr/bin/env python3
\"\"\"自动生成有声绘本\"\"\"
import requests
import subprocess
import os

class MiniMaxVoiceBook:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = \"https://api.minimax.chat/v1\"
        self.headers = {
            \"Authorization\": f\"Bearer {api_key}\",
            \"Content-Type\": \"application/json\"
        }
    
    def tts(self, text, voice_id, output_path):
        \"\"\"生成单句语音\"\"\"
        url = f\"{self.base_url}/t2a_v2\"
        payload = {
            \"model\": \"speech-01\",
            \"text\": text,
            \"voice_id\": voice_id,
            \"audio_format\": \"mp3\"
        }
        resp = requests.post(url, headers=self.headers, json=payload)
        data = resp.json()
        # 下载音频
        audio_url = data.get(\"audio_url\")
        if audio_url:
            audio_data = requests.get(audio_url).content
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            return output_path
        return None
    
    def generate_bgm(self, description, duration=30, output_path=\"bgm.mp3\"):
        \"\"\"生成背景音乐\"\"\"
        url = f\"{self.base_url}/music_generation\"
        payload = {
            \"model\": \"music-01\",
            \"description\": description,
            \"duration\": duration
        }
        resp = requests.post(url, headers=self.headers, json=payload)
        data = resp.json()
        audio_url = data.get(\"audio_url\")
        if audio_url:
            audio_data = requests.get(audio_url).content
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            return output_path
        return None
    
    def mix_audio(self, voice_files, bgm_file, output_path=\"final.mp3\"):
        \"\"\"混合语音和背景音乐(ffmpeg)\"\"\"
        # 合并所有语音文件
        concat_list = \"concat.txt\"
        with open(concat_list, 'w') as f:
            for vf in voice_files:
                f.write(f\"file '{vf}'\n\")
        
        # 先合并语音
        subprocess.run([
            \"ffmpeg\", \"-y\", \"-f\", \"concat\", \"-safe\", \"0\",
            \"-i\", concat_list, \"-acodec\", \"libmp3lame\", \"voice_mixed.mp3\"
        ], check=True)
        
        # 混合BGM（降低音量到20%）
        subprocess.run([
            \"ffmpeg\", \"-y\", \"-i\", \"voice_mixed.mp3\", \"-i\", bgm_file,
            \"-filter_complex\", \"[1:a]volume=0.2[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]\",
            \"-map\", \"[a]\", output_path
        ], check=True)
        
        # 清理
        os.remove(concat_list)
        os.remove(\"voice_mixed.mp3\")
        
        return output_path


# 使用示例
if __name__ == \"__main__\":
    book = MiniMaxVoiceBook(api_key=\"your-api-key\")
    
    # 1. 生成角色语音
    voice_files = []
    scenes = [
        (\"小兔子：妈妈，我想去森林里玩！\", \"female-child-01\", \"scene01.mp3\"),
        (\"兔妈妈：好啊，但是要小心大灰狼哦~\", \"female-gentle-01\", \"scene02.mp3\"),
    ]
    
    for text, voice, filename in scenes:
        path = book.tts(text, voice, filename)
        if path:
            voice_files.append(path)
    
    # 2. 生成背景音乐
    book.generate_bgm(\"温馨森林冒险背景音乐，轻快活泼，适合儿童\", duration=60, output_path=\"bgm.mp3\")
    
    # 3. 混合
    book.mix_audio(voice_files, \"bgm.mp3\", \"my-audiobook.mp3\")
```

---

## 6. 参考资源

- MiniMax 开放平台: https://www.minimaxi.com/
- MiniMax TTS 文档: https://www.minimaxi.com/document/speech
- 小红书笔记: https://xhslink.com/o/lDh382f3oj
- Turn.js 翻页效果: https://www.turnjs.com/

---

*调研完成于 2026-05-27*
