#!/usr/bin/env python3
"""
Generate gear picture book audio files using MiMo TTS.
Saves WAV files to audio/gears/ and generates a manifest JSON.
"""

import json
import base64
import os
import sys
import time
import urllib.request

API_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
API_KEY = "tp-c7k6pxt1txvnyi57st58buzqi882cx554fv5dgm7euy48q3h"
OUTPUT_DIR = "/home/deploy/childrens-library/courseware/audio/gears"

VOICES = {
    "narrator": "用温和的叙述声音朗读",
    "steve": "用低沉稳重的男性声音朗读",
    "alex": "用温柔的女声朗读",
    "happy": "用开心的、充满活力的声音朗读",
}

# Page content: (page_id, text)
# Should match what the HTML files reference
TEXTS = [
    ("cover", "齿轮传动的秘密。 The secret of gears."),
    ("intro", "齿轮是什么？轮子上长了牙齿！齿轮是一种机械零件，靠牙齿传递运动和力量。 What is a gear? A wheel with teeth! A gear is a mechanical part that uses teeth to transmit motion and force."),
    ("speed", "大齿轮转得慢，小齿轮转得快。 Big gears turn slowly, small gears turn fast."),
    ("mesh", "两个齿轮咬合在一起，一个转动，另一个也会跟着转！这就是齿轮传动。 When two gears mesh together, when one turns, the other turns too! That's gear transmission."),
    ("drag", "请拖动齿轮到空位上，拼装传动链。 Drag the gears into the empty spaces to build a transmission chain."),
    ("quiz", "小测验时间！来检查一下你学会了什么。 Quiz time! Let's check what you've learned."),
    ("vocab", "词汇表：齿轮是带齿的轮子。传动是传递运动。旋转就是转动。齿是齿轮上的凸起。 Vocabulary: Gear is a wheel with teeth. Transmission means passing along motion. Rotation means turning. Teeth are the bumps on a gear."),
    ("review", "知识回顾：齿轮是带齿的轮子，大齿轮转得慢，小齿轮转得快。齿轮传动可以把动力从一个地方传到另一个地方，比如自行车和钟表。 Review: Gears are wheels with teeth. Big gears turn slowly, small gears turn fast. Gears transmit power from one place to another, like in bicycles and clocks."),
    ("celebrate", "恭喜你！你学会了齿轮传动！你真是个小工程师！ Congratulations! You've learned about gears! You're a little engineer!"),
]


def call_tts(text, voice_prompt):
    """Call MiMo TTS API and return base64 audio data."""
    payload = json.dumps({
        "model": "mimo-v2-tts",
        "messages": [
            {"role": "user", "content": text},
            {"role": "assistant", "content": voice_prompt},
        ],
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ✗ API request failed: {e}")
        return None

    # Check for errors
    if "error" in data:
        print(f"  ✗ API error: {data['error'].get('message', 'unknown')}")
        return None

    try:
        audio_data = data["choices"][0]["message"]["audio"]["data"]
        return audio_data
    except (KeyError, IndexError) as e:
        print(f"  ✗ Unexpected response format: {e}")
        print(f"  Response: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
        return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"=== Generating gear audio files ===")
    print(f"Output: {OUTPUT_DIR}\n")

    total = len(TEXTS) * len(VOICES)
    current = 0
    success = 0
    skip = 0
    fail = 0

    for page_id, text in TEXTS:
        for voice_name, voice_prompt in VOICES.items():
            current += 1
            outfile = os.path.join(OUTPUT_DIR, f"{page_id}_{voice_name}.wav")

            # Skip if already exists
            if os.path.isfile(outfile) and os.path.getsize(outfile) > 100:
                print(f"[{current}/{total}] ⏩  {page_id}_{voice_name}.wav (already exists)")
                skip += 1
                continue

            print(f"[{current}/{total}]  🎤  {page_id}_{voice_name}...  ", end="", flush=True)

            audio_b64 = call_tts(text, voice_prompt)
            if audio_b64 is None:
                print("✗")
                fail += 1
                continue

            # Decode and save
            try:
                audio_bytes = base64.b64decode(audio_b64)
                with open(outfile, "wb") as f:
                    f.write(audio_bytes)
                size_kb = len(audio_bytes) / 1024
                print(f"✓ ({size_kb:.0f} KB)")
                success += 1
            except Exception as e:
                print(f"✗ decode error: {e}")
                fail += 1

            # Rate limit: small delay between calls
            time.sleep(0.5)

    print(f"\n=== Complete ===")
    print(f"  Success: {success}")
    print(f"  Skipped: {skip}")
    print(f"  Failed:  {fail}")
    print(f"  Total:   {total}")
    print(f"  Size:    {round(sum(os.path.getsize(os.path.join(OUTPUT_DIR, f)) for f in os.listdir(OUTPUT_DIR) if f.endswith('.wav')) / 1024)} KB")


if __name__ == "__main__":
    main()
