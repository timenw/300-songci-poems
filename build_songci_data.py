#!/usr/bin/env python3
"""Convert chinese-poetry songci data to our app format."""
import json, subprocess, os

RAW_DIR = "/tmp/songci_raw"
OUT_JSON = "/root/300-songci-poems/app/src/main/assets/poems.json"
OUT_DB = "/root/300-songci-poems/app/src/main/assets/poems.db"

os.makedirs(RAW_DIR, exist_ok=True)

# Download songci JSON files from chinese-poetry
# Files: ci.song.0.json, ci.song.1000.json, ci.song.2000.json, etc.
base_url = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%AE%8B%E8%AF%8D"

all_poems = []
for offset in range(0, 22000, 1000):
    url = f"{base_url}/ci.song.{offset}.json"
    out_file = f"{RAW_DIR}/ci.song.{offset}.json"
    
    if not os.path.exists(out_file):
        print(f"Downloading {url}...")
        result = subprocess.run(
            ["curl", "-sL", url, "-o", out_file],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0 or not os.path.exists(out_file):
            print(f"Failed to download {url}")
            continue
    
    try:
        with open(out_file, encoding='utf-8') as f:
            data = json.load(f)
            all_poems.extend(data)
            print(f"  Loaded {len(data)} poems (total: {len(all_poems)})")
    except Exception as e:
        print(f"  Error loading {out_file}: {e}")
    
    if len(all_poems) >= 350:
        break

print(f"\nTotal poems loaded: {len(all_poems)}")

# Convert to our format
output = []
for i, item in enumerate(all_poems[:300]):
    rhythmic = item.get('rhythmic', '')
    author = item.get('author', '')
    paragraphs = item.get('paragraphs', [])
    content = '\n'.join(paragraphs) if paragraphs else ''
    note = item.get('note', [])
    annotation = '\n'.join(note) if isinstance(note, list) else str(note)
    
    # Determine category based on rhythmic name
    category = '宋词'
    
    # Determine difficulty based on content length
    if len(content) < 30:
        difficulty = 1
    elif len(content) < 80:
        difficulty = 2
    else:
        difficulty = 3
    
    poem = {
        'id': i + 1,
        'title': rhythmic,
        'titlePinyin': '',
        'titleEn': rhythmic,
        'author': author,
        'authorPinyin': '',
        'authorEn': author,
        'dynasty': '宋',
        'dynastyEn': 'Song',
        'content': content,
        'translation': '',
        'annotation': annotation,
        'category': category,
        'difficulty': difficulty
    }
    output.append(poem)

# Save JSON
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(output)} poems to {OUT_JSON}")

# Generate SQLite database for Room
import sqlite3

if os.path.exists(OUT_DB):
    os.remove(OUT_DB)

conn = sqlite3.connect(OUT_DB)
c = conn.cursor()

# Create poems table
c.execute('''CREATE TABLE poems (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    titlePinyin TEXT NOT NULL DEFAULT '',
    titleEn TEXT NOT NULL DEFAULT '',
    author TEXT NOT NULL,
    authorPinyin TEXT NOT NULL DEFAULT '',
    authorEn TEXT NOT NULL DEFAULT '',
    dynasty TEXT NOT NULL DEFAULT '宋',
    dynastyEn TEXT NOT NULL DEFAULT 'Song',
    content TEXT NOT NULL DEFAULT '',
    translation TEXT NOT NULL DEFAULT '',
    annotation TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT '宋词',
    difficulty INTEGER NOT NULL DEFAULT 1
)''')

# Create favorites table
c.execute('''CREATE TABLE favorites (
    poemId INTEGER PRIMARY KEY NOT NULL,
    note TEXT NOT NULL DEFAULT '',
    groupName TEXT NOT NULL DEFAULT 'Default',
    createdAt INTEGER NOT NULL DEFAULT 0
)''')

# Insert poems
for poem in output:
    c.execute('''INSERT INTO poems 
        (id, title, titlePinyin, titleEn, author, authorPinyin, authorEn, 
         dynasty, dynastyEn, content, translation, annotation, category, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (poem['id'], poem['title'], poem['titlePinyin'], poem['titleEn'],
         poem['author'], poem['authorPinyin'], poem['authorEn'],
         poem['dynasty'], poem['dynastyEn'], poem['content'],
         poem['translation'], poem['annotation'], poem['category'], poem['difficulty']))

conn.commit()
conn.close()

print(f"Database saved to {OUT_DB}")
print(f"Authors: {len(set(p['author'] for p in output))}")
print(f"Sample: {output[0]['title']} by {output[0]['author']}")
