#!/usr/bin/env python3
"""Kindle表紙画像を生成（Pillow使用）
   1600x2560px の表紙画像をテキストベースで作成"""
import os
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

today = datetime.now().strftime('%Y-%m-%d')

# 原稿からタイトル抽出（今日→直近の日付の順で探す）
manuscript_path = f'商品パッケージ/{today}/kindle_manuscript.md'
if not os.path.exists(manuscript_path):
    import glob
    candidates = sorted(glob.glob('商品パッケージ/*/kindle_manuscript.md'), reverse=True)
    if candidates:
        manuscript_path = candidates[0]
        print(f"⚠️ 今日の原稿なし。最新を使用: {manuscript_path}")
    else:
        print("❌ 原稿が見つかりません")
        exit(1)

with open(manuscript_path, 'r', encoding='utf-8') as f:
    manuscript = f.read()

title_match = re.search(r'^#\s+(.+)', manuscript, re.MULTILINE)
title = title_match.group(1).strip() if title_match else f"AI活用ガイド"

# 副題（最初の ## 見出し）
subtitle_match = re.search(r'^##\s+(.+)', manuscript, re.MULTILINE)
subtitle = subtitle_match.group(1).strip() if subtitle_match else "プロンプト活用大全"

# 出力先
pub_dir = f'Kindle出版/{today}'
os.makedirs(pub_dir, exist_ok=True)
cover_path = f'{pub_dir}/cover.jpg'

# ---- 表紙生成 ----
W, H = 1600, 2560

# グラデーション背景（紺→紫）
img = Image.new('RGB', (W, H), color=(20, 30, 80))
draw = ImageDraw.Draw(img)

for y in range(H):
    r = int(20 + (80 - 20) * y / H)
    g = int(30 + (40 - 30) * y / H)
    b = int(80 + (140 - 80) * y / H)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# 装飾ライン
draw.rectangle([0, 200, W, 220], fill=(255, 215, 0))
draw.rectangle([0, H-220, W, H-200], fill=(255, 215, 0))

# フォント
font_paths = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',
    '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
]

font_title = None
font_sub = None
for fp in font_paths:
    if os.path.exists(fp):
        font_title = ImageFont.truetype(fp, 110)
        font_sub = ImageFont.truetype(fp, 60)
        font_author = ImageFont.truetype(fp, 50)
        print(f"  ✅ フォント: {fp}")
        break

if not font_title:
    print("  ⚠️ 日本語フォント未検出、デフォルト使用")
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_author = ImageFont.load_default()

# タイトル描画（折り返し）
def wrap_text(text, max_chars):
    lines = []
    current = ""
    for ch in text:
        current += ch
        if len(current) >= max_chars:
            lines.append(current)
            current = ""
    if current:
        lines.append(current)
    return lines

title_lines = wrap_text(title, 10)
y_pos = 600
for line in title_lines[:3]:
    bbox = draw.textbbox((0, 0), line, font=font_title)
    text_w = bbox[2] - bbox[0]
    draw.text(((W - text_w) // 2, y_pos), line, fill=(255, 255, 255), font=font_title)
    y_pos += 140

# サブタイトル
subtitle_short = subtitle[:25] + ("..." if len(subtitle) > 25 else "")
bbox = draw.textbbox((0, 0), subtitle_short, font=font_sub)
text_w = bbox[2] - bbox[0]
draw.text(((W - text_w) // 2, y_pos + 80), subtitle_short, fill=(255, 215, 0), font=font_sub)

# 著者
author = "AI副業ラボ"
bbox = draw.textbbox((0, 0), author, font=font_author)
text_w = bbox[2] - bbox[0]
draw.text(((W - text_w) // 2, H - 350), author, fill=(255, 255, 255), font=font_author)

# 出版日
date_str = f"{today}"
bbox = draw.textbbox((0, 0), date_str, font=font_author)
text_w = bbox[2] - bbox[0]
draw.text(((W - text_w) // 2, H - 280), date_str, fill=(200, 200, 200), font=font_author)

img.save(cover_path, 'JPEG', quality=95)
print(f"✅ 表紙画像生成: {cover_path}")
print(f"  サイズ: {W}x{H}px")
print(f"  タイトル: {title}")
