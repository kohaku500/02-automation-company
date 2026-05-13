#!/usr/bin/env python3
"""note向け: プレゼン・アプリ・ガイドを生成"""
import os
import time
from datetime import datetime
import requests

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY が設定されていません")
    exit(1)

today = datetime.now().strftime('%Y-%m-%d')
package_dir = f'商品パッケージ/{today}'
source_file = f'{package_dir}/note_package.md'

if not os.path.exists(source_file):
    print(f"❌ note_package.md が見つかりません: {source_file}")
    exit(1)

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ note_package.md 読み込み完了（{len(content)}文字）")

def call_gemini(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    for attempt in range(3):
        try:
            res = requests.post(
                f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
                headers=headers, json=payload, timeout=300
            )
            if res.status_code == 200:
                return res
            elif res.status_code == 503 and attempt < 2:
                print(f"⚠️ 503 エラー。30秒待機後リトライ...")
                time.sleep(30)
            else:
                print(f"❌ API エラー: {res.status_code}")
                print(res.text[:300])
                return res
        except Exception as e:
            if attempt < 2:
                time.sleep(30)
            else:
                raise
    return res

def clean_html(code):
    for prefix in ['```html', '```']:
        if code.startswith(prefix):
            code = code[len(prefix):]
    if code.endswith('```'):
        code = code[:-3]
    return code.strip()

# Pass 2: note向けプレゼン
print("🔄 note向けプレゼンを生成中...")
pres_res = call_gemini(f"""以下のnote記事の内容をベースに、読者向けの紹介スライドをHTMLで生成してください。

【note記事（抜粋）】
{content[:2500]}

【要件】
- 完全自己完結型HTML（CSS・JS埋め込み）
- 矢印キー/ボタンでスライド切り替え
- 10〜12スライド構成
- note読者向け：親しみやすくシンプルなデザイン
- 1スライド1メッセージ、テキスト最大150文字
- Font Awesomeのみ外部CDN可
- スマホ対応
- <!DOCTYPE html>から</html>までのHTMLのみ出力""")

if pres_res.status_code == 200:
    code = clean_html(pres_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/note_presentation.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ note_presentation.html 生成完了")
else:
    exit(1)

time.sleep(30)

# Pass 3: note向けアプリ
print("🔄 note向けアプリを生成中...")
app_res = call_gemini(f"""以下のnote記事のテーマに関連する、読者がすぐ使える実用ツールをHTMLで生成してください。

【テーマ】
{content[:800]}

【要件】
- 完全自己完結型HTML（外部ファイル参照なし）
- note読者が記事を読んだ後すぐ使えるツール（チェックリスト・診断・計算機等）
- スマホ対応
- Bootstrap・Chart.jsのみ外部CDN可
- 個人情報を収集しない
- <!DOCTYPE html>から</html>までのHTMLのみ出力""")

if app_res.status_code == 200:
    code = clean_html(app_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/note_app.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ note_app.html 生成完了")
else:
    exit(1)

time.sleep(30)

# Pass 4: note向けガイド
print("🔄 note向けガイドを生成中...")
guide_res = call_gemini(f"""上記のツールの使い方を、note読者向けにわかりやすく説明するHTMLを生成してください。

【内容】
- ツールの概要と目的
- 使用手順（ステップバイステップ）
- よくある質問
- note記事との活用方法

【形式】
- 完全自己完結型HTML、スマホ対応
- 親しみやすいデザイン、日本語

<!DOCTYPE html>から</html>までのHTMLのみ出力してください。""")

if guide_res.status_code == 200:
    code = clean_html(guide_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/note_guide.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ note_guide.html 生成完了")
else:
    exit(1)

print(f"\n✅ note向け全アセット生成完了: {package_dir}")
