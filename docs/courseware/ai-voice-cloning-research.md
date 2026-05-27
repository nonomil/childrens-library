# 调研：AI 语音捏制 / 声音克隆方案

> 来源: 小红书笔记《绷不住了，声音居然可以这样捏出来》  
> 日期: 2026-05-27  
> 调研目的: 了解"捏声音"的技术方案，为项目落地做准备

---

## 什么是"捏声音"

"捏声音"指的是通过 AI 技术，用少量语音样本（甚至不用样本）生成特定音色、语调、情绪的语音。核心能力包括：

1. **声音克隆 (Voice Cloning)**：用 5-30 秒音频，复制一个人的声音
2. **多角色语音 (Multi-Character TTS)**：为不同角色生成不同音色
3. **情绪控制 (Emotion Control)**：在声音中注入开心、悲伤、愤怒等情绪
4. **背景音乐 (BGM)**：自动匹配场景氛围的背景音乐

---

## 方案对比表

| 方案 | 费用 | 中文支持 | 声音克隆 | 情绪控制 | 适合场景 | 上手难度 |
|------|------|---------|---------|---------|---------|---------|
| **MiniMax TTS** | 付费 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 有声绘本、角色配音 | 低 |
| **ElevenLabs** | 付费/免费额度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 英文播客、有声书 | 低 |
| **GPT-SoVITS** | 免费（开源） | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 中文角色配音、二创 | 中 |
| **Fish Audio** | 免费额度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 实时语音合成 | 低 |
| **RVC (实时变声)** | 免费（开源） | ⭐⭐ | ⭐⭐ | ⭐ | 直播、实时变声 | 高 |
| **OpenVoice** | 免费（开源） | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 多语言克隆 | 中 |
| **KikiVoice** | 免费在线 | ⭐⭐ | ⭐⭐ | ⭐ | 快速体验 | 极低 |
| **SpeechGen** | 免费在线 | ⭐⭐ | ⭐⭐ | ⭐ | 快速体验 | 极低 |

---

## 方案一：MiniMax（推荐，适合中文场景）

### 简介

MiniMax 是国内领先的 AI 公司，其 TTS 和语音克隆 API 在中文场景下表现优秀。支持：

- 声音克隆：上传 5-30 秒音频，即可克隆声音
- 多角色：内置多种音色（男童、女童、老人、青年等）
- 情绪控制：支持开心、悲伤、生气、平静等情绪
- 背景音乐：可选配 BGM

### API 调用示例

```python
import requests
import json

# MiniMax TTS API（假设端点，需确认官方文档）
def minimax_tts(text, voice_id, emotion="neutral"):
    url = "https://api.minimax.chat/v1/text_to_speech"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_id": voice_id,
        "emotion": emotion,
        "speed": 1.0,
        "format": "mp3"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        return "output.mp3"
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 示例
minimax_tts(
    text="从前有座山，山里有座庙，庙里有个小和尚。",
    voice_id="zh_male_001",
    emotion="happy"
)
```

### 价格参考（预估）

| 服务 | 价格 | 备注 |
|------|------|------|
| 标准 TTS | ~0.005 元/字 | 按字符计费 |
| 声音克隆 | ~0.01 元/字 | 克隆后按合成字数计费 |
| 自定义音色训练 | ~50-200 元/次 | 上传 5-30 秒样本 |

> **注意**: 具体价格以 MiniMax 官网为准，以上为市场调研参考价

---

## 方案二：ElevenLabs（推荐，适合英文/多语言）

### 简介

ElevenLabs 是全球最知名的 AI 语音平台，支持：

- **Voice Cloning**: 上传 1-3 分钟音频，克隆任何声音
- **Voice Design**: 通过参数（年龄、性别、口音）"设计"声音
- **Multi-language**: 支持 50+ 种语言
- **Emotion Control**: 控制语调、语气、情感强度

### API 调用示例

```python
import requests

def elevenlabs_tts(text, voice_id, api_key):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    return None
```

### 价格

| 套餐 | 价格 | 包含 |
|------|------|------|
| Free | $0/月 | 10,000 字符/月 |
| Starter | $5/月 | 30,000 字符/月 |
| Creator | $22/月 | 100,000 字符/月 |
| Pro | $99/月 | 500,000 字符/月 |

---

## 方案三：GPT-SoVITS（开源，技术极客）

### 简介

GPT-SoVITS 是中文社区最火的 AI 语音克隆项目，特点：

- **零样本克隆**: 仅需 5 秒音频即可克隆
- **跨语言**: 支持中英日等语言互转
- **情感控制**: 可控制语气、语速、停顿
- **完全免费**: 开源，可本地部署

### 部署方式

```bash
# 安装依赖
pip install gpt-sovits

# 启动 Web UI
python webui.py --share
```

### 适用场景

- 二次元角色配音
- 有声小说制作
- 个人声音备份
- 教育内容制作

---

## 方案四：Fish Audio（新兴方案）

### 简介

Fish Audio 是新兴的开源 TTS 项目，特点：

- **低延迟**: 支持实时语音合成
- **多说话人**: 支持多角色对话
- **开源**: 可本地部署
- **Web API**: 提供在线 API

### 在线体验

- 官网: https://fish.audio/
- GitHub: https://github.com/fishaudio/fish-speech

---

## 快速体验方案（免费在线工具）

### 1. KikiVoice（推荐）

- 网址: https://kikivoice.ai/
- 特点: 无需注册，3 分钟生成克隆声音
- 语言: 支持 75+ 种语言
- 费用: 免费试用额度

### 2. SpeechGen

- 网址: https://speechgen.io/
- 特点: 支持 146 种语言
- 费用: 免费试用

### 3. NiceVoice

- 网址: https://nicevoice.org/
- 特点: 免费 AI 声音克隆
- 语言: 中文支持

---

## 落地建议

### 场景 1：有声绘本（小星 Bot）

| 需求 | 推荐方案 | 理由 |
|------|---------|------|
| 多角色配音 | MiniMax / ElevenLabs | API 稳定，中文好 |
| 低成本 | GPT-SoVITS 本地部署 | 免费，一次训练多次使用 |
| 快速上线 | ElevenLabs | 注册即用，API 完善 |

### 场景 2：AI 家教（小乐 Bot）

| 需求 | 推荐方案 | 理由 |
|------|---------|------|
| 自然对话 | ElevenLabs / MiniMax | 语音自然度高 |
| 实时交互 | Fish Audio | 低延迟，适合对话 |
| 成本控制 | GPT-SoVITS | 完全免费 |

### 场景 3：内容创作

| 需求 | 推荐方案 | 理由 |
|------|---------|------|
| 多语言 | ElevenLabs | 50+ 语言 |
| 声音克隆 | GPT-SoVITS | 零样本，效果好 |
| 批量生成 | MiniMax API | 稳定可靠 |

---

## 下一步行动

1. **立即体验**: 用 KikiVoice 或 SpeechGen 免费体验声音克隆
2. **评估 MiniMax**: 注册 MiniMax 账号，测试 TTS API
3. **本地部署**: 如果有 GPU，部署 GPT-SoVITS 进行深度定制
4. **集成到 Bot**: 将 TTS 能力接入小星/小乐 Bot

---

## 参考链接

- MiniMax 官网: https://www.minimaxi.com/
- ElevenLabs: https://elevenlabs.io/
- GPT-SoVITS GitHub: https://github.com/RVC-Boss/GPT-SoVITS
- Fish Audio: https://fish.audio/
- KikiVoice: https://kikivoice.ai/
- SpeechGen: https://speechgen.io/

---

*调研完成于 2026-05-27*
*小红书笔记: http://xhslink.com/o/lDh382f3oj*
