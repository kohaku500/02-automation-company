#!/usr/bin/env python3
"""Kindle向け: プレゼン・アプリ・ガイドを生成"""
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
source_file = f'{package_dir}/kindle_manuscript.md'

if not os.path.exists(source_file):
    print(f"❌ kindle_manuscript.md が見つかりません: {source_file}")
    exit(1)

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ kindle_manuscript.md 読み込み完了（{len(content)}文字）")

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

# Pass 2: Kindle向けプレゼン（電子書籍の内容紹介）
print("🔄 Kindle向けプレゼンを生成中...")
pres_res = call_gemini(f"""以下のKindle電子書籍の内容をベースに、書籍紹介・要約スライドをHTMLで生成してください。

【電子書籍内容（抜粋）】
{content[:2500]}

【要件】
- 完全自己完結型HTML（CSS・JS埋め込み）
- 矢印キー/ボタンでスライド切り替え
- 12〜15スライド構成
- 読者向け：書籍の章立てと主要メッセージを体系的に紹介
- ビジネス書・専門書らしい洗練されたデザイン
- Font Awesomeのみ外部CDN可
- スマホ対応
- <!DOCTYPE html>から</html>までのHTMLのみ出力""")

if pres_res.status_code == 200:
    code = clean_html(pres_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/kindle_presentation.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ kindle_presentation.html 生成完了")
else:
    exit(1)

time.sleep(30)

# Pass 3: Kindle向けアプリ（読書補助ツール）
print("🔄 Kindle向けアプリを生成中...")
app_res = call_gemini(f"""以下のKindle電子書籍のテーマに関連する、読者の学習・実践をサポートするツールをHTMLで生成してください。

【テーマ】
{content[:800]}

【要件】
- 完全自己完結型HTML（外部ファイル参照なし）
- 書籍の内容を実践するためのツール（チェックリスト・学習記録・ワークシート・振り返りツール等）
- 読書後の行動変容を促すもの
- スマホ対応
- Bootstrap・Chart.jsのみ外部CDN可
- 個人情報を収集しない
- <!DOCTYPE html>から</html>までのHTMLのみ出力""")

if app_res.status_code == 200:
    code = clean_html(app_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/kindle_app.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ kindle_app.html 生成完了")
else:
    exit(1)

time.sleep(30)

# Pass 4: Kindle向けガイド
print("🔄 Kindle向けガイドを生成中...")
guide_res = call_gemini(f"""Kindle電子書籍の読者向けに、補助ツールの使い方と書籍の効果的な活用方法を説明するHTMLを生成してください。

【内容】
- ツールの概要と書籍との連携方法
- 各章に対応したツールの使い方
- 学習効果を高めるための活用法
- よくある質問

【形式】
- 完全自己完結型HTML、スマホ対応
- 知的・洗練されたデザイン
- 日本語

<!DOCTYPE html>から</html>までのHTMLのみ出力してください。""")

if guide_res.status_code == 200:
    code = clean_html(guide_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/kindle_guide.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ kindle_guide.html 生成完了")
else:
    exit(1)

print(f"\n✅ Kindle向け全アセット生成完了: {package_dir}")
