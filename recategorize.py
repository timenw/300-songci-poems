#!/usr/bin/env python3
"""Re-tag Song Ci poems with proper categories based on title/titleEn keywords, then rebuild poems.db."""
import json, os, sqlite3

JSON_FILE = "/root/300-songci-poems/app/src/main/assets/poems.json"
DB_FILE = "/root/300-songci-poems/app/src/main/assets/poems.db"

# Category mapping: keyword -> category tag (Chinese)
# Ordered by priority (first match wins)
CATEGORY_RULES = [
    # 情感类
    ("婉约", ["婉约", "柔情", "闺怨", "相思", "离愁", "flirt", "love", "yearning"]),
    ("豪放", ["豪放", "壮怀", "慷慨", "heroic", "ambition", "battle"]),
    ("思念", ["念", "思", "想", "怀旧", "miss", "remember", "longing"]),
    ("离别", ["别", "送", "离", "farewell", "parting", "departure"]),
    ("孤独", ["独", "孤", "lonely", "alone", "solitude"]),
    
    # 自然类
    ("月亮", ["月", "moon"]),
    ("春天", ["春", "spring"]),
    ("秋天", ["秋", "autumn"]),
    ("雪", ["雪", "snow"]),
    ("花", ["花", "flower", "bloom"]),
    ("山水", ["山", "水", "river", "mountain"]),
    ("雨", ["雨", "rain"]),
    ("风", ["风", "wind"]),
    ("柳", ["柳", "willow"]),
    
    # 节日/时间
    ("元宵", ["元宵", "lantern"]),
    ("七夕", ["七夕", "qixi"]),
    ("重阳", ["重阳", "double ninth"]),
    ("夜晚", ["夜", "night", "evening"]),
    ("黄昏", ["暮", "昏", "夕", "dusk", "sunset"]),
    
    # 人生/哲理
    ("人生", ["人生", "life", "time", "岁月"]),
    ("怀古", ["怀古", "nostalgia", "ancient", "history"]),
    ("壮志", ["壮", "志", "ambition", "dream"]),
    ("隐逸", ["隐", "逸", "retreat", "hermit", "闲"]),
    ("田园", ["田", "园", "farm", "country"]),
    
    # 社交
    ("友情", ["友", "friend"]),
    ("祝寿", ["寿", "birthday", "longevity"]),
    ("宴饮", ["宴", "饮", "酒", "feast", "wine"]),
]

def categorize(title, titleEn):
    """Assign category based on title keywords."""
    text = (title + titleEn).lower()
    for category, keywords in CATEGORY_RULES:
        for kw in keywords:
            if kw.lower() in text:
                return category
    # Default categories based on difficulty/length
    return "其他"

with open(JSON_FILE, encoding='utf-8') as f:
    poems = json.load(f)

# Apply categories
for poem in poems:
    poem['category'] = categorize(poem['title'], poem.get('titleEn', ''))

with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(poems, f, ensure_ascii=False, indent=2)

# Show distribution
from collections import Counter
cats = Counter(p['category'] for p in poems)
print("Category distribution:")
for cat, count in cats.most_common():
    print(f"  {cat}: {count}")

# Rebuild database
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''CREATE TABLE poems (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, titlePinyin TEXT NOT NULL DEFAULT '',
    titleEn TEXT NOT NULL DEFAULT '', author TEXT NOT NULL, authorPinyin TEXT NOT NULL DEFAULT '',
    authorEn TEXT NOT NULL DEFAULT '', dynasty TEXT NOT NULL DEFAULT '宋',
    dynastyEn TEXT NOT NULL DEFAULT 'Song', content TEXT NOT NULL DEFAULT '',
    translation TEXT NOT NULL DEFAULT '', annotation TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT '宋词', difficulty INTEGER NOT NULL DEFAULT 1
)''')
c.execute('''CREATE TABLE favorites (
    poemId INTEGER PRIMARY KEY NOT NULL, note TEXT NOT NULL DEFAULT '',
    groupName TEXT NOT NULL DEFAULT 'Default', createdAt INTEGER NOT NULL DEFAULT 0
)''')
for p in poems:
    c.execute('INSERT INTO poems VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (p['id'], p['title'], p.get('titlePinyin',''), p.get('titleEn',''),
         p['author'], p.get('authorPinyin',''), p.get('authorEn',''),
         p.get('dynasty','宋'), p.get('dynastyEn','Song'), p.get('content',''),
         p.get('translation',''), p.get('annotation',''), p.get('category','宋词'),
         p.get('difficulty',1)))
conn.commit()
conn.close()
print(f"\nDone! {len(poems)} poems re-categorized. DB rebuilt.")
