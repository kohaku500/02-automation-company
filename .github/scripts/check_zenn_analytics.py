#!/usr/bin/env python3
"""Zenn 公開API でアナリティクスを取得"""
import os
import json
import requests
from datetime import datetime

ZENN_USERNAME = os.environ.get('ZENN_USERNAME', 'kohaku500')
today = datetime.now().strftime('%Y-%m-%d')
os.makedirs('運営ログ', exist_ok=True)

print(f"📊 Zenn アナリティクス取得: @{ZENN_USERNAME}")

# 記事一覧を取得
resp = requests.get(
    f'https://zenn.dev/api/articles?username={ZENN_USERNAME}&order=latest',
    timeout=15
)

if resp.status_code != 200:
    print(f"❌ API エラー: {resp.status_code}")
    exit(1)

articles = resp.json().get('articles', [])
print(f"  記事数: {len(articles)}")

if not articles:
    print("ℹ️ まだ記事がありません")
    exit(0)

# 集計
total_likes     = sum(a.get('liked_count', 0) for a in articles)
total_bookmarks = sum(a.get('bookmarks_count', 0) for a in articles)
total_comments  = sum(a.get('comments_count', 0) for a in articles)

# レポート生成
report = f"# Zenn アナリティクスレポート {today}\n\n"
report += f"## サマリー\n\n"
report += f"| 指標 | 数値 |\n|------|------|\n"
report += f"| 記事数 | {len(articles)} |\n"
report += f"| 総いいね数 | {total_likes} |\n"
report += f"| 総ブックマーク数 | {total_bookmarks} |\n"
report += f"| 総コメント数 | {total_comments} |\n\n"

report += f"## 記事別データ\n\n"
report += f"| タイトル | いいね | ブックマーク | 公開日 |\n"
report += f"|---------|--------|------------|--------|\n"

for a in articles[:10]:
    title     = a.get('title', '(タイトルなし)')[:40]
    likes     = a.get('liked_count', 0)
    bookmarks = a.get('bookmarks_count', 0)
    published = a.get('published_at', '')[:10]
    report += f"| {title} | {likes} | {bookmarks} | {published} |\n"

path = f'運営ログ/zenn_アナリティクス_{today}.md'
with open(path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ レポート保存: {path}")
print(f"  総いいね: {total_likes} / ブックマーク: {total_bookmarks}")
