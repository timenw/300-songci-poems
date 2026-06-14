#!/usr/bin/env python3
"""Generate AI audio for 300 Song Ci poems using Edge TTS."""
import json, subprocess, os, sys

AUDIO_DIR = "/root/300-songci-poems/app/src/main/assets/audio"
JSON_FILE = "/root/300-songci-poems/app/src/main/assets/poems.json"
VOICE = "zh-CN-YunxiNeural"

os.makedirs(AUDIO_DIR, exist_ok=True)

with open(JSON_FILE, encoding='utf-8') as f:
    poems = json.load(f)

print(f"Generating audio for {len(poems)} poems...")

success = 0
skip = 0
fail = 0

for poem in poems:
    poem_id = poem['id']
    filename = f"poem_{str(poem_id).zfill(3)}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    
    # Skip if already exists and valid
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
        skip += 1
        continue
    
    # Build text to read: title + content
    title = poem['title']
    content = poem['content']
    text = f"《{title}》。{content}"
    
    # Clean text for TTS (remove newlines, extra spaces)
    text = text.replace('\n', '。').replace('  ', ' ')
    
    try:
        result = subprocess.run(
            ["edge-tts", "--voice", VOICE, "--text", text, "--write-media", filepath],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and os.path.exists(filepath) and os.path.getsize(filepath) > 100:
            success += 1
            if success % 10 == 0:
                print(f"  Progress: {success} generated, {skip} skipped, {fail} failed")
        else:
            fail += 1
            print(f"  Failed poem {poem_id}: {result.stderr[:100]}")
    except subprocess.TimeoutExpired:
        fail += 1
        print(f"  Timeout poem {poem_id}")
    except Exception as e:
        fail += 1
        print(f"  Error poem {poem_id}: {e}")

print(f"\nDone! {success} generated, {skip} skipped, {fail} failed")
print(f"Total audio files: {len(os.listdir(AUDIO_DIR))}")
