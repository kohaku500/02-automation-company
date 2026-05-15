import os
from datetime import datetime
import requests

api_key = os.environ.get('GEMINI_API_KEY')
today = datetime.now().strftime('%Y-%m-%d')

# 部署間連携：当日のコンテンツ出力を読み込む
content_dir = f'商品パッケージ/{today}'
content_summary = ""
if os.path.exists(f'{content_dir}/complete_package.md'):
    with open(f'{content_dir}/complete_package.md', 'r', encoding='utf-8') as f:
        content_summary = f.read()[:3000]
    print(f"✅ 当日のコンテンツを読み込み: {content_dir}")
else:
    print(f"⚠️ 当日のコンテンツが見つかりません: {content_dir}")

# COO判定も読み込む
coo_file = f'運営ログ/COO判定_{today}.md'
coo_judgment = ""
if os.path.exists(coo_file):
    with open(coo_file, 'r', encoding='utf-8') as f:
        coo_judgment = f.read()

prompt = f"""あなたはクライアント管理部です。本日（{today}）の顧客管理レポートを生成してください。

# 本日のコンテンツ概要（クライアント反応を予測する材料）
{content_summary if content_summary else "（コンテンツ未生成）"}

# COO判定からの指示
{coo_judgment if coo_judgment else "（COO判定なし）"}

上記の情報を踏まえて、本日のコンテンツに対する顧客反応を予測し、レポートを生成してください。

# 顧客サマリーレポート（{today}）

## 数値サマリー
- 新規顧客: X人
- 総顧客数: X人
- 平均満足度: X.X / 5.0
- チャーンレート: X%
- 返金申請: X件

## プラットフォーム別パフォーマンス
### note
- 新規: X人
- MRR: ¥XXXXX

### BOOTH
- 新規: X人
- MRR: ¥XXXXX

### Kindle
- 新規: X人
- MRR: ¥XXXXX

## 顧客満足度分析
- 5.0点: X人
- 4.0点: X人
- 3.0点: X人
- 2.0点以下: X人

## 課題・対応予定
- （該当があれば記載）

レポート生成完了"""

headers = {'Content-Type': 'application/json'}
payload = {'contents': [{'parts': [{'text': prompt}]}]}

response = requests.post(
    f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
    headers=headers,
    json=payload
)

if response.status_code == 200:
    result = response.json()
    report = result['candidates'][0]['content']['parts'][0]['text']
    os.makedirs('運営ログ', exist_ok=True)
    with open(f'運営ログ/顧客レポート_{today}.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ 顧客レポート生成完了")
else:
    print(f"❌ エラー: {response.status_code}")
