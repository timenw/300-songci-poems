#!/usr/bin/env python3
"""Generate a Song Ci Poetry themed APK launcher icon using Pillow."""
from PIL import Image, ImageDraw, ImageFont
import os

# Icon sizes for Android mipmap directories
SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

BASE_DIR = "/root/300-songci-poems/app/src/main/res"

# Color palette - Song Dynasty inspired (青绿山水风格)
TEAL = (0, 128, 128)         # 青绿 - 背景主色
DARK_TEAL = (0, 80, 80)      # 深青绿 - 背景暗部
GOLD = (218, 165, 32)         # 金色 - 文字
LIGHT_GOLD = (255, 215, 0)    # 亮金 - 高光
DARK_GOLD = (184, 134, 11)    # 暗金 - 阴影
CREAM = (255, 248, 220)       # 米白 - 装饰
WHITE = (255, 255, 255)       # 白色

def get_cjk_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJKsc-Bold.otf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                continue
    return ImageFont.load_default()

def create_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background - teal rounded rectangle (青绿山水)
    margin = max(1, size // 24)
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=size // 8,
        fill=TEAL
    )
    
    # Gradient effect - darker at bottom
    for i in range(size // 3):
        alpha = int(30 * (i / (size // 3)))
        y = size - margin - i - 1
        if y > margin:
            draw.line([(margin + 2, y), (size - margin - 2, y)], fill=(0, 60, 60), width=1)
    
    # Inner border - gold
    border = max(1, size // 32)
    inner_margin = margin + border * 2
    draw.rounded_rectangle(
        [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
        radius=size // 10,
        outline=GOLD,
        width=border
    )
    
    # Decorative corner dots
    dot_r = max(1, size // 48)
    corners = [
        (inner_margin + border * 3, inner_margin + border * 3),
        (size - inner_margin - border * 3, inner_margin + border * 3),
        (inner_margin + border * 3, size - inner_margin - border * 3),
        (size - inner_margin - border * 3, size - inner_margin - border * 3),
    ]
    for cx, cy in corners:
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=GOLD)
    
    # Main character "词" (Ci poetry) in center
    char = "词"
    font_size = int(size * 0.55)
    font = get_cjk_font(font_size)
    
    bbox = draw.textbbox((0, 0), char, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    tx = (size - text_w) // 2 - bbox[0]
    ty = (size - text_h) // 2 - bbox[1]
    
    # Shadow
    shadow_offset = max(1, size // 96)
    draw.text((tx + shadow_offset, ty + shadow_offset), char, font=font, fill=DARK_GOLD)
    # Main text
    draw.text((tx, ty), char, font=font, fill=GOLD)
    # Highlight
    draw.text((tx - 1, ty - 1), char, font=font, fill=LIGHT_GOLD)
    
    # Small decorative text at bottom - "宋" (Song)
    small_font = get_cjk_font(int(size * 0.12))
    small_char = "宋"
    sbbox = draw.textbbox((0, 0), small_char, font=small_font)
    sw = sbbox[2] - sbbox[0]
    sh = sbbox[3] - sbbox[1]
    sx = (size - sw) // 2 - sbbox[0]
    sy = size - inner_margin - border * 2 - sh - sbbox[1]
    draw.text((sx, sy), small_char, font=small_font, fill=CREAM)
    
    return img

def create_round_icon(size):
    img = create_icon(size)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size, size], fill=255)
    img.putalpha(mask)
    return img

# Generate all icons
print("Generating Song Ci themed icons (青绿山水风格)...")
for dirname, size in SIZES.items():
    dirpath = os.path.join(BASE_DIR, dirname)
    os.makedirs(dirpath, exist_ok=True)
    
    icon = create_icon(size)
    icon.save(os.path.join(dirpath, "ic_launcher.png"), "PNG")
    print(f"  {dirname}/ic_launcher.png ({size}x{size})")
    
    round_icon = create_round_icon(size)
    round_icon.save(os.path.join(dirpath, "ic_launcher_round.png"), "PNG")
    print(f"  {dirname}/ic_launcher_round.png ({size}x{size})")

print("\nDone! All Song Ci icons generated.")
