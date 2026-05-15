import os
from datetime import datetime, timedelta
import requests

api_key = os.environ.get('GEMINI_API_KEY')
today = datetime.now().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# フィードバックループ：前日の全部署結果を読み込む
previous_data = {}

# 前日の顧客レポート
yesterday_client = f'運営ログ/顧客レポート_{yesterday}.md'
if os.path.exists(yesterday_client):
    with open(yesterday_client, 'r', encoding='utf-8') as f:
        previous_data['顧客レポート'] = f.read()[:2000]
    print(f"✅ 前日の顧客レポート読み込み")

# 前日のマーケティング企画
yesterday_marketing = f'商品企画/企画案_{yesterday}.md'
if os.path.exists(yesterday_marketing):
    with open(yesterday_marketing, 'r', encoding='utf-8') as f:
        previous_data['マーケティング企画'] = f.read()[:2000]
    print(f"✅ 前日のマーケティング企画読み込み")

# 前日の秘書日報
yesterday_report = f'運営ログ/日報_{yesterday}.md'
if os.path.exists(yesterday_report):
    with open(yesterday_report, 'r', encoding='utf-8') as f:
        previous_data['秘書日報'] = f.read()[:2000]
    print(f"✅ 前日の秘書日報読み込み")

previous_context = "\n\n".join([f"## 前日の{k}\n{v}" for k, v in previous_data.items()])

# 現在テーマ管理ファイルを読み込む
theme_file = '運営ログ/現在テーマ.md'
current_theme_info = ""
if os.path.exists(theme_file):
    with open(theme_file, 'r', encoding='utf-8') as f:
        current_theme_info = f.read()
    print(f"✅ 現在テーマ読み込み")
else:
    current_theme_info = "（テーマ未設定：初回選定が必要）"
    print(f"⚠️ テーマファイルなし。初回選定を実施")

prompt = f"""あなたはCOO（最高執行責任者）です。本日（{today}）の経営判定レポートを生成してください。

# 前日（{yesterday}）の各部署結果（フィードバックループ）
{previous_context if previous_context else "（前日のデータなし）"}

上記の前日の結果を踏まえて、改善点を反映した本日の経営判定を生成してください。

# COO判定レポート（{today}）

## 本日の重要指標
- MRR進捗: ¥XXXXX / ¥50,000目標（XXX%）
- 新規顧客: X人
- 顧客満足度: X.X / 5.0
- チャーンレート: X%

## 各部署への指示
### マーケティング部
- 優先商品開発: X案を推奨
- プロモーション戦略: X
- 次期ターゲット層: X

### コンテンツ制作部
- 月間目標: X～X商品
- 品質基準: X
- 納期厳守: X

### クライアント管理部
- リテンション優先度: X
- 返金対応: X
- 特典充実化: X

### 秘書室
- 明日以降の優先度: X
- 会議スケジュール: X
- 報告体制: X

## 経営判定
### 売上予測
- 当月予想: ¥XXXXX
- 評価: X

### 課題分析
- 最大課題: X
- 対応方針: X

### リスク警告
- 利益率30%以下の商品: なし/X件
- 需要警告: なし/X件

## 部署編成判定

### 現在の稼働部署
- COO判定部、マーケティング部、コンテンツ制作部、クライアント管理部、秘書室

### 部署追加判定
以下の指標で新規部署の必要性を判定してください：
- MRR が ¥30,000 を超えたか → デザイン・品質向上部の追加を検討
- 顧客満足度が 4.0 未満か → カスタマーサポート強化部の追加を検討
- コンテンツ生産量が不足しているか → 第2コンテンツ制作部の追加を検討
- その他、データから判断した部署追加が必要か

### 部署強化判定
- マーケティング部の企画採用率が低い → プロンプト強化・リサーチ強化を指示
- コンテンツ制作部の品質スコアが低い → 品質基準の引き上げ・プロンプト改善を指示
- 各部署の負担が大きい → 業務分担の見直しを提案

### 部署縮小・廃止判定
- 生産コストが高く効果が低い部署 → 廃止を検討
- 重複機能がある部署 → 統合を検討

### 判定結果
- 追加推奨: なし / 部署名（追加理由）
- 強化推奨: なし / 部署名（具体的な改善内容）
- 廃止推奨: なし / 部署名（廃止理由）

## 商品テーマ選定・継続判定

### 現在の商品テーマ
{current_theme_info}

### テーマ継続・変更の判定基準
以下のデータを元に、現在テーマを継続すべきか変更すべきか判定してください：
- 品質スコアが7日連続で80点以上 → テーマ成熟・変更を検討
- 品質スコアが3日連続で60点未満 → テーマ or プロンプト改善が必要
- バージョンが v1.10 を超えた → テーマ変更を検討
- 新しい市場トレンドがある → 新テーマへの移行を検討

### 新テーマ候補（変更が必要な場合）
2026年の市場トレンドを踏まえて、以下の観点で新テーマを3案提案してください：
- 検索需要が高く競合が少ないニッチ
- AIツール活用・副業・生産性向上のカテゴリを優先
- note/BOOTH/Kindle で売れやすいテーマ

### テーマ判定結果
- 判定: 継続 / 変更推奨
- 現在テーマ: [テーマ名]
- バージョン: v[X.X] → v[X.X+1]（継続の場合）または v1.0（変更の場合）
- 変更理由（変更の場合）: [理由]
- 新テーマ（変更の場合）: [新テーマ名]
- 新テーマの根拠: [市場データ・トレンドの根拠]

## 明日の焦点
- X に集中

判定完了"""

headers = {'Content-Type': 'application/json'}
payload = {'contents': [{'parts': [{'text': prompt}]}]}

response = requests.post(
    f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
    headers=headers,
    json=payload
)

if response.status_code == 200:
    result = response.json()
    judgment = result['candidates'][0]['content']['parts'][0]['text']
    os.makedirs('運営ログ', exist_ok=True)
    with open(f'運営ログ/COO判定_{today}.md', 'w', encoding='utf-8') as f:
        f.write(judgment)
    print(f"✅ COO判定レポート生成完了")

    # テーマ更新スクリプトで処理（別ファイルに分離）
    import subprocess
    subprocess.run(['python3', '.github/scripts/update_theme.py'], check=False)
else:
    print(f"❌ エラー: {response.status_code}")
