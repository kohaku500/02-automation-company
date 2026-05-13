#!/usr/bin/env python3
"""BOOTH向け: プレゼン・アプリ・ガイドを生成"""
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
source_file = f'{package_dir}/booth_package.md'

if not os.path.exists(source_file):
    print(f"❌ booth_package.md が見つかりません: {source_file}")
    exit(1)

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"✅ booth_package.md 読み込み完了（{len(content)}文字）")

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

# Pass 2: BOOTH向けプレゼン（購入を促す価値提案スライド）
print("🔄 BOOTH向けプレゼンを生成中...")
pres_res = call_gemini(f"""以下のBOOTH商品の内容をベースに、購入者向けの価値提案スライドをHTMLで生成してください。

【BOOTH商品内容（抜粋）】
{content[:2500]}

【要件】
- 完全自己完結型HTML（CSS・JS埋め込み）
- 矢印キー/ボタンでスライド切り替え
- 12〜15スライド構成
- 購入者向け：「この商品で何が得られるか」を明確に伝えるデザイン
- 商品価値・特典・使い方の流れを示す
- Font Awesomeのみ外部CDN可
- スマホ対応
- <!DOCTYPE html>から</html>までのHTMLのみ出力""")

if pres_res.status_code == 200:
    code = clean_html(pres_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/booth_presentation.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ booth_presentation.html 生成完了")
else:
    exit(1)

time.sleep(30)

# Pass 3: BOOTH向けアプリ（購入特典ツール）
print("🔄 BOOTH向けアプリを生成中...")
app_res = call_gemini(f"""以下のBOOTH商品テーマに関連する、購入者向けの特典ツールをHTMLで生成してください。

【テーマ】
{content[:800]}

【要件】
- 完全自己完結型HTML（外部ファイル参照なし）
- 購入者が即座に活用できる実用ツール（テンプレート・計算機・診断・ワークシート等）
- 商品の価値を高める特典として機能するもの
- スマホ対応
- Bootstrap・Chart.jsのみ外部CDN可
- 個人情報を収集しない
- <!DOCTYPE html>から</html>までのHTMLのみ出力""")

if app_res.status_code == 200:
    code = clean_html(app_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/booth_app.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ booth_app.html 生成完了")
else:
    exit(1)

time.sleep(30)

# Pass 4: BOOTH向けガイド
print("🔄 BOOTH向けガイドを生成中...")
guide_res = call_gemini(f"""購入者向けに、特典ツールの使い方と商品の活用方法を説明するHTMLを生成してください。

【内容】
- 特典ツールの概要と活用シーン
- ステップバイステップの使用手順
- 商品全体の活用ロードマップ
- よくある質問とサポート情報

【形式】
- 完全自己完結型HTML、スマホ対応
- 信頼感・プロフェッショナルなデザイン
- 日本語

<!DOCTYPE html>から</html>までのHTMLのみ出力してください。""")

if guide_res.status_code == 200:
    code = clean_html(guide_res.json()['candidates'][0]['content']['parts'][0]['text'])
    with open(f'{package_dir}/booth_guide.html', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ booth_guide.html 生成完了")
else:
    exit(1)

print(f"\n✅ BOOTH向け全アセット生成完了: {package_dir}")
