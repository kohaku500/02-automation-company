#!/usr/bin/env python3
"""生成されたコンテンツを Zenn 形式に変換して articles/ に出力"""
import os
import re
import hashlib
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')

# note_package.md を読み込む
source_file = f'商品パッケージ/{today}/note_package.md'
if not os.path.exists(source_file):
    print(f"❌ ソースファイルが見つかりません: {source_file}")
    exit(1)

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ ソース読み込み: {source_file} ({len(content)}文字)")

# タイトルを抽出（最初の # 見出し）
title = "AIで実現する副業・収益化の最新メソッド"
title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
if title_match:
    title = title_match.group(1).strip()
    # Zennタイトルの文字数制限（70文字）
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

# Zennのslug（ファイル名）: 日付 + ハッシュ4桁
slug_hash = hashlib.md5(today.encode()).hexdigest()[:4]
slug = f"{today}-ai-side-hustle-{slug_hash}"

# 絵文字をトピックに合わせて選択
emoji = "🤖"
if 'プロンプト' in title or 'ChatGPT' in title:
    emoji = "💬"
elif '副業' in title or '収益' in title:
    emoji = "💰"
elif 'マーケティング' in title:
    emoji = "📈"
elif 'AI' in title:
    emoji = "🤖"

# Zenn frontmatter を付加
topics_str = '", "'.join(topics[:5])
frontmatter = f'''---
title: "{title}"
emoji: "{emoji}"
type: "idea"
topics: ["{topics_str}"]
published: true
---

'''

# note_package.md の本文（最初の # 見出しの後から）
body = content
# 先頭の "# note向けパッケージ" のような行を除去
body = re.sub(r'^#\s+note向け.*\n', '', body, flags=re.MULTILINE)
body = re.sub(r'^【最適化されたコンテンツ】\n?', '', body, flags=re.MULTILINE)

zenn_article = frontmatter + body.strip()

# articles/ に保存
output_path = f'articles/{slug}.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(zenn_article)

print(f"✅ Zenn記事生成: {output_path}")
print(f"  タイトル: {title}")
print(f"  絵文字: {emoji}")
print(f"  トピック: {topics}")
print(f"  文字数: {len(zenn_article)}")
