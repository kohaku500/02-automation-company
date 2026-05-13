#!/usr/bin/env python3
"""Kindle 出版用ファイル一式を生成
   1. EPUB変換（pandoc使用）
   2. メタデータ.md生成（タイトル・説明文・キーワード）
   3. 出版チェックリスト生成"""
import os
import re
import subprocess
import requests
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
api_key = os.environ.get('GEMINI_API_KEY')

# 最新のKindle原稿を取得
manuscript_path = f'商品パッケージ/{today}/kindle_manuscript.md'
if not os.path.exists(manuscript_path):
    print(f"❌ 原稿が見つかりません: {manuscript_path}")
    exit(1)

with open(manuscript_path, 'r', encoding='utf-8') as f:
    manuscript = f.read()

print(f"✅ 原稿読み込み: {len(manuscript)}文字")

# 出版ディレクトリ作成
pub_dir = f'Kindle出版/{today}'
os.makedirs(pub_dir, exist_ok=True)

# ---- ① EPUB変換 ----
print("📚 EPUB変換中...")
epub_path = f'{pub_dir}/manuscript.epub'

# タイトル抽出
title_match = re.search(r'^#\s+(.+)', manuscript, re.MULTILINE)
title = title_match.group(1).strip() if title_match else f"AI活用ガイド {today}"

# pandoc で md → epub 変換
try:
    subprocess.run([
        'pandoc',
        manuscript_path,
        '-o', epub_path,
        '--metadata', f'title={title}',
        '--metadata', 'lang=ja',
        '--toc',
        '--toc-depth=2',
    ], check=True)
    print(f"  ✅ EPUB生成: {epub_path}")
except subprocess.CalledProcessError as e:
    print(f"  ❌ pandoc失敗: {e}")
except FileNotFoundError:
    print("  ⚠️ pandoc未インストール（ワークフローで apt install pandoc 必須）")

# ---- ② メタデータ生成（Gemini） ----
print("📝 メタデータ生成中...")

metadata_prompt = f"""以下のKindle電子書籍の原稿から、Amazon KDP出版に必要なメタデータを生成してください。

# 原稿（冒頭3000文字）
{manuscript[:3000]}

# 必要なメタデータ
以下の形式で出力してください：

## タイトル
（70文字以内、検索されやすいキーワード含む）

## サブタイトル
（200文字以内、補足説明）

## 著者名
（ペンネーム例: AI副業ラボ）

## 書籍の説明
（4000文字以内、Amazonの商品ページに表示。読者の悩み→解決策→章の概要→誰におすすめか の流れ）

## キーワード（7個）
1. （50文字以内）
2.
3.
4.
5.
6.
7.

## カテゴリー（2つ）
1. メインカテゴリー
2. サブカテゴリー

## 推奨価格
¥XXX（¥250-¥1250の範囲で印税70%対象）"""

headers = {'Content-Type': 'application/json'}
payload = {'contents': [{'parts': [{'text': metadata_prompt}]}]}

resp = requests.post(
    f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
    headers=headers, json=payload, timeout=120
)

if resp.status_code == 200:
    metadata = resp.json()['candidates'][0]['content']['parts'][0]['text']
    metadata_path = f'{pub_dir}/メタデータ.md'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(f"# Kindle出版メタデータ {today}\n\n{metadata}")
    print(f"  ✅ メタデータ: {metadata_path}")
else:
    print(f"  ❌ メタデータ生成失敗: {resp.status_code}")

# ---- ③ 出版チェックリスト ----
print("📋 出版チェックリスト生成中...")

checklist = f"""# Kindle出版チェックリスト {today}

## 提出ファイル

- [ ] EPUB: `Kindle出版/{today}/manuscript.epub`
- [ ] 表紙画像: `Kindle出版/{today}/cover.jpg`（1600x2560px推奨）
- [ ] メタデータ: `Kindle出版/{today}/メタデータ.md` 参照

## KDPアップロード手順

1. https://kdp.amazon.co.jp/ にログイン
2. 「電子書籍を新規作成」をクリック
3. **本の詳細** タブ
   - 言語: 日本語
   - タイトル: メタデータ.md から転記
   - サブタイトル: メタデータ.md から転記
   - 著者: ペンネーム
   - 書籍の説明: メタデータ.md から転記
   - キーワード: 7個
   - カテゴリー: 2個
   - 成人向けコンテンツ: いいえ
4. **本のコンテンツ** タブ
   - 電子書籍のISBN: 不要
   - EPUBをアップロード
   - 表紙画像をアップロード
   - 「電子書籍プレビューア」で確認
5. **本の価格設定** タブ
   - KDP Select に登録: 推奨（Kindle Unlimited 対象に）
   - 主要マーケットプレイス: 日本（Amazon.co.jp）
   - 印税: 70%（¥250-¥1250）
   - 価格: メタデータ.md 参照
6. **出版申請** をクリック
7. 審査待ち（約72時間）

## 出版後

- [ ] Amazon商品URLを `運営ログ/kindle_url.md` に追記
- [ ] Zenn記事の末尾に自動でCTAが追加される
"""

checklist_path = f'{pub_dir}/出版チェックリスト.md'
with open(checklist_path, 'w', encoding='utf-8') as f:
    f.write(checklist)
print(f"  ✅ チェックリスト: {checklist_path}")

print(f"\n✅ Kindle出版準備完了: {pub_dir}/")
