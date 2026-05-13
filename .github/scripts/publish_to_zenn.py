#!/usr/bin/env python3
"""生成されたコンテンツを Zenn 形式に変換して articles/ に出力
   HTML ファイルは docs/ にコピーして GitHub Pages でホスティング"""
import os
import re
import shutil
import hashlib
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
GITHUB_PAGES_BASE = "https://kohaku500.github.io/02-automation-company"

# note_package.md を読み込む
source_file = f'商品パッケージ/{today}/note_package.md'
if not os.path.exists(source_file):
    print(f"❌ ソースファイルが見つかりません: {source_file}")
    exit(1)

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ ソース読み込み: {source_file} ({len(content)}文字)")

# タイトルを抽出
title = "AIで実現する副業・収益化の最新メソッド"
title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
if title_match:
    title = title_match.group(1).strip()
    if len(title) > 70:
        title = title[:67] + "..."
print(f"  タイトル: {title}")

# テーマからトピックを推定
topics = ["副業", "AI活用", "ChatGPT"]
theme_file = '運営ログ/現在テーマ.md'
if os.path.exists(theme_file):
    with open(theme_file, 'r', encoding='utf-8') as f:
        theme_data = f.read()
    if 'プロンプト' in theme_data:
        topics = ["ChatGPT", "プロンプト", "副業", "AI活用"]
    elif '副業' in theme_data:
        topics = ["副業", "AI活用", "自動化"]
    elif 'マーケティング' in theme_data:
        topics = ["マーケティング", "AI活用", "副業"]

# slug・絵文字
slug_hash = hashlib.md5(today.encode()).hexdigest()[:4]
slug = f"{today}-ai-side-hustle-{slug_hash}"

emoji = "🤖"
if 'プロンプト' in title or 'ChatGPT' in title:
    emoji = "💬"
elif '副業' in title or '収益' in title:
    emoji = "💰"
elif 'マーケティング' in title:
    emoji = "📈"

# ---- HTML ファイルを docs/YYYY-MM-DD/ にコピー ----
html_files = {
    'note_app.html':          'アプリ（プロンプト生成ツール）',
    'note_presentation.html': 'プレゼン資料',
    'note_guide.html':        '使用方法ガイド',
}

docs_dir = f'docs/{today}'
os.makedirs(docs_dir, exist_ok=True)

pages_links = []
for filename, label in html_files.items():
    src = f'商品パッケージ/{today}/{filename}'
    dst = f'{docs_dir}/{filename}'
    if os.path.exists(src):
        shutil.copy2(src, dst)
        url = f'{GITHUB_PAGES_BASE}/{today}/{filename}'
        pages_links.append((label, url))
        print(f"  📄 コピー: {dst}")
    else:
        print(f"  ⚠️ ファイルなし: {src}")

# docs/index.html（一覧ページ）を更新
index_path = 'docs/index.html'
index_entries = ""
# 既存エントリを読み込む
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        existing = f.read()
    body_match = re.search(r'<ul id="list">(.*?)</ul>', existing, re.DOTALL)
    if body_match:
        index_entries = body_match.group(1)

new_entry = f'\n  <li><strong>{today}</strong> — {title}<br>'
for label, url in pages_links:
    new_entry += f'<a href="{url}">{label}</a> / '
new_entry = new_entry.rstrip(' / ') + '</li>'
index_entries = new_entry + index_entries

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(f'''<!DOCTYPE html>
<html lang="ja">
<head><meta charset="UTF-8"><title>AI副業コンテンツ一覧</title>
<style>body{{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px}}
li{{margin:12px 0}}a{{margin-right:8px}}</style></head>
<body>
<h1>🤖 AI副業コンテンツ一覧</h1>
<ul id="list">{index_entries}
</ul>
</body></html>''')
print(f"  📋 一覧ページ更新: {index_path}")

# ---- GitHub Pages リンクセクションを作成 ----
links_section = "\n\n---\n\n## 📦 付属ツール・資料\n\n"
links_section += "この記事には以下の付属コンテンツが含まれています：\n\n"
for label, url in pages_links:
    links_section += f"- 🔗 **[{label}]({url})**\n"
links_section += "\n---\n\n"

# ---- Zenn frontmatter ----
topics_str = '", "'.join(topics[:5])
frontmatter = f'''---
title: "{title}"
emoji: "{emoji}"
type: "idea"
topics: ["{topics_str}"]
published: true
---

'''

# 本文整形
body = content
body = re.sub(r'^#\s+note向け.*\n', '', body, flags=re.MULTILINE)
body = re.sub(r'^【最適化されたコンテンツ】\n?', '', body, flags=re.MULTILINE)

zenn_article = frontmatter + links_section + body.strip()

output_path = f'articles/{slug}.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(zenn_article)

print(f"✅ Zenn記事生成: {output_path}")
print(f"  付属リンク数: {len(pages_links)}")
