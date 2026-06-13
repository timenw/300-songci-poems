#!/usr/bin/env python3
"""Regenerate TTS audio for poems ID 1-62 using Edge TTS (Yunxi voice)."""
import asyncio
import json
import os
import edge_tts

VOICE = "zh-CN-YunxiNeural"
RATE = "-10%"
OUTPUT_DIR = "app/src/main/assets/audio"
POEMS_FILE = "app/src/main/assets/poems.json"

async def generate_one(poem, semaphore):
    pid = poem["id"]
    title = poem["title"]
    author = poem["author"]
    content = poem["content"]
    # Read title, author, and content clearly
    text = f"《{title}》，{author}。{content.replace(chr(10), '，')}"
    fname = f"poem_{pid:03d}.mp3"
    fpath = os.path.join(OUTPUT_DIR, fname)
    async with semaphore:
        try:
            comm = edge_tts.Communicate(text, VOICE, rate=RATE)
            await comm.save(fpath)
            sz = os.path.getsize(fpath)
            return f"  OK   {fname} ({title} — {author}, {sz//1024}KB)"
        except Exception as e:
            return f"  FAIL {fname} ({title}): {e}"

async def main():
    with open(POEMS_FILE, "r", encoding="utf-8") as f:
        poems = json.load(f)
    
    # Filter poems with ID 1-62
    target_poems = [p for p in poems if isinstance(p.get("id"), int) and 1 <= p["id"] <= 62]
    target_poems.sort(key=lambda p: p["id"])
    
    print(f"Loaded {len(poems)} poems total")
    print(f"Target: {len(target_poems)} poems (ID 1-62)")
    print(f"Voice: {VOICE}")
    print()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    semaphore = asyncio.Semaphore(3)
    tasks = [generate_one(p, semaphore) for p in target_poems]
    results = await asyncio.gather(*tasks)
    
    for r in results:
        print(r)
    
    ok = sum(1 for r in results if "OK" in r)
    fail = sum(1 for r in results if "FAIL" in r)
    print(f"\nDone: {ok} regenerated, {fail} failed")

asyncio.run(main())
