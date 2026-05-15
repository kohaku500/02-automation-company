import os
import json
from datetime import datetime, timedelta
import requests

# Gemini API を呼び出してToDoリスト生成
api_key = os.environ.get('GEMINI_API_KEY')
today = datetime.now().strftime('%Y-%m-%d')

# 前日の結果を読み込む（部署間連携）
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

previous_results = {}

# 前日の日報
yesterday_report = f'運営ログ/日報_{yesterday}.md'
if os.path.exists(yesterday_report):
    with open(yesterday_report, 'r', encoding='utf-8') as f:
        previous_results['前日日報'] = f.read()[:2000]
    print(f"✅ 前日日報読み込み")

# 前日の COO判定
yesterday_coo = f'運営ログ/COO判定_{yesterday}.md'
if os.path.exists(yesterday_coo):
    with open(yesterday_coo, 'r', encoding='utf-8') as f:
        previous_results['前日COO判定'] = f.read()[:2000]
    print(f"✅ 前日COO判定読み込み")

# 前日のクライアントレポート
yesterday_client = f'運営ログ/顧客レポート_{yesterday}.md'
if os.path.exists(yesterday_client):
    with open(yesterday_client, 'r', encoding='utf-8') as f:
        previous_results['前日クライアントレポート'] = f.read()[:1500]
    print(f"✅ 前日クライアントレポート読み込み")

previous_context = "\n\n".join([f"## {k}\n{v}" for k, v in previous_results.items()])

# 秘書室のプロンプト
prompt = f"""あなたは秘書室です。本日（{today}）のToDoリストを生成してください。

# 前日（{yesterday}）の各部署結果
{previous_context if previous_context else "（前日のデータなし）"}

上記の前日の結果を踏まえて、本日の優先タスクを生成してください。テンプレートではなく、具体的な状況に基づいた実行可能なタスクを書いてください。

フォーマット：
# 本日のToDoリスト（{today}）

## 優先度S（売上直結・緊急）
- [ ] 秘書室: システムの状態確認
- [ ] マーケティング部: 本日の投稿ネタ提案準備

## 優先度A（重要）
- [ ] 各部署: 昨日の課題フォローアップ

## 優先度B（通常）
- [ ] 秘書室: 日報準備

実行完了後、「ToDoリスト生成完了」と出力してください。"""

# Gemini API に呼び出し
headers = {
    'Content-Type': 'application/json'
}

payload = {
    'contents': [
        {
            'parts': [
                {'text': prompt}
            ]
        }
    ]
}

response = requests.post(
    f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
    headers=headers,
    json=payload
)

if response.status_code == 200:
    result = response.json()
    todo_content = result['candidates'][0]['content']['parts'][0]['text']

    # ファイル保存
    os.makedirs('運営ログ', exist_ok=True)
    file_path = f'運営ログ/ToDoリスト_{today}.md'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(todo_content)

    print(f"✅ ToDoリスト生成完了: {file_path}")
else:
    print(f"❌ API呼び出し失敗: {response.status_code}")
    print(response.text)
