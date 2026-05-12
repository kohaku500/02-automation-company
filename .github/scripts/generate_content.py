#!/usr/bin/env python3
import os
from datetime import datetime
import requests
import json

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY が設定されていません")
    exit(1)

today = datetime.now().strftime('%Y-%m-%d')
marketing_file = f'商品企画/企画案_{today}.md'
marketing_content = ""

if os.path.exists(marketing_file):
    with open(marketing_file, 'r', encoding='utf-8') as f:
        marketing_content = f.read()

prompt = f"""あなたはコンテンツ制作部です。3プラットフォーム向けパッケージを生成してください。

マーケティング企画:
{marketing_content if marketing_content else "（企画案ファイルが見つかりません）"}

以下の3種類を生成:
1. note向け記事（5000文字以上）
2. BOOTH向け（7000文字以上）
3. Kindle向け原稿（10000文字以上）"""

headers = {'Content-Type': 'application/json'}
payload = {'contents': [{'parts': [{'text': prompt}]}]}

print("🔄 Gemini API を呼び出し中...")

try:
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code == 200:
        result = response.json()
        package_content = result['candidates'][0]['content']['parts'][0]['text']
        package_dir = f'商品パッケージ/{today}'
        os.makedirs(package_dir, exist_ok=True)

        with open(f'{package_dir}/complete_package.md', 'w', encoding='utf-8') as f:
            f.write(package_content)

        print(f"✅ パッケージ生成完了: {package_dir}")
    else:
        print(f"❌ API エラー: {response.status_code}")
        print(f"レスポンス: {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ エラー: {str(e)}")
    exit(1)
