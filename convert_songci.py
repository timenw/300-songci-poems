#!/usr/bin/env python3
"""Generate 300 Song Ci poems data from structured data file."""
import json, sys

# Read the raw songci data
data = open('/root/300-songci-poems/songci_raw.json', encoding='utf-8').read()
poems_raw = json.loads(data)

output = []
for i, item in enumerate(poems_raw[:300]):
    # chinese-poetry format: {rhythmic, author, paragraphs, note}
    rhythmic = item.get('rhythmic', '')
    author = item.get('author', '')
    paragraphs = item.get('paragraphs', [])
    content = '\n'.join(paragraphs) if paragraphs else ''
    
    poem = {
        'id': i + 1,
        'title': rhythmic,
        'titlePinyin': '',
        'titleEn': '',
        'author': author,
        'authorPinyin': '',
        'authorEn': author,
        'dynasty': '宋',
        'dynastyEn': 'Song',
        'content': content,
        'translation': '',
        'annotation': '',
        'category': '宋词',
        'difficulty': 2
    }
    output.append(poem)

with open('/root/300-songci-poems/app/src/main/assets/poems.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Generated {len(output)} poems')
