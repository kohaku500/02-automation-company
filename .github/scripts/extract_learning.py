#!/usr/bin/env python3
"""
学習システム：前日の結果から成功・失敗事例を抽出
毎日朝7時に実行され、成功事例DBと失敗事例DBを更新する
"""
import os
import re
import time
from datetime import datetime, timedelta
import requests

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY が設定されていません")
    exit(1)

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
print(f"📊 {yesterday} の結果から学習データを抽出中...")

# 前日の全部署の結果を収集
previous_results = {}

files_to_check = {
    'COO判定': f'運営ログ/COO判定_{yesterday}.md',
    'マーケティング企画': f'商品企画/企画案_{yesterday}.md',
    'クライアントレポート': f'運営ログ/顧客レポート_{yesterday}.md',
    '日報': f'運営ログ/日報_{yesterday}.md',
}

for name, filepath in files_to_check.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            previous_results[name] = f.read()
        print(f"✅ {name} 読み込み完了")
    else:
        print(f"⚠️ {name} が見つかりません: {filepath}")

if not previous_results:
    print("❌ 前日の結果がありません。学習スキップ。")
    exit(0)

# 前日の品質スコアを抽出して集計
def extract_quality_scores(report_text):
    """日報テキストから品質スコアを抽出"""
    scores = {}
    for pkg in ['note_package.md', 'booth_package.md', 'kindle_manuscript.md']:
        match = re.search(rf'{re.escape(pkg)}[:\s]+(\d+)/100', report_text)
        if match:
            scores[pkg.replace('.md', '')] = int(match.group(1))
    return scores

quality_scores = {}
if '日報' in previous_results:
    quality_scores = extract_quality_scores(previous_results['日報'])
    if quality_scores:
        avg = sum(quality_scores.values()) / len(quality_scores)
        print(f"📊 前日品質スコア: {quality_scores} / 平均 {avg:.1f}点")

# 品質スコアサマリーを追記
quality_summary = ""
if quality_scores:
    high = [(k, v) for k, v in quality_scores.items() if v >= 80]
    low = [(k, v) for k, v in quality_scores.items() if v < 80]
    quality_summary = f"\n\n## 前日品質スコア\n"
    for k, v in quality_scores.items():
        mark = "✅" if v >= 80 else "⚠️" if v >= 60 else "❌"
        quality_summary += f"- {k}: {v}/100点 {mark}\n"
    if high:
        quality_summary += f"\n**高スコア（成功パターン候補）**: {', '.join([k for k, _ in high])}\n"
    if low:
        quality_summary += f"\n**低スコア（改善優先）**: {', '.join([k for k, _ in low])}\n"

combined_data = "\n\n".join([f"## {k}\n{v[:2000]}" for k, v in previous_results.items()]) + quality_summary

prompt = f"""あなたは経営学習部です。前日（{yesterday}）の各部署の結果と品質スコアを分析し、成功事例・失敗事例・高スコアのパターンを抽出してください。

# 前日の各部署の結果
{combined_data}

# 出力フォーマット（厳守）

## 成功事例
（成功した取り組み、効果的だった戦略、評価が高かったコンテンツなどを3〜5件抽出）

### 事例1: [タイトル]
- 部署: [部署名]
- 内容: [具体的に何が成功したか]
- なぜ成功したか: [理由]
- 再現するためのポイント: [将来活用するためのポイント]

### 事例2: ...

## 失敗事例
（失敗した取り組み、効果のなかった戦略、低評価だったコンテンツなどを3〜5件抽出）

### 事例1: [タイトル]
- 部署: [部署名]
- 内容: [具体的に何が失敗したか]
- なぜ失敗したか: [理由]
- 避けるべきパターン: [将来回避するためのポイント]

### 事例2: ...

## 高スコアパターン分析（品質80点以上の共通要因）
（品質スコアが80点以上のコンテンツに共通する要素を分析してください）

### 共通要因1: [要因タイトル]
- 具体的な特徴: [何が高スコアに貢献したか]
- 次回への活用: [どう再現するか]

### 共通要因2: ...

## 低スコアパターン分析（品質80点未満の改善点）
（品質スコアが80点未満のコンテンツに共通する問題点を分析してください）

### 問題点1: [問題タイトル]
- 具体的な不足: [何が不足していたか]
- 改善方法: [どう改善するか]

### 問題点2: ...

抽出完了"""

headers = {'Content-Type': 'application/json'}
payload = {'contents': [{'parts': [{'text': prompt}]}]}

print("🔄 学習データ抽出中...")
max_retries = 3
retry_delay = 10

for attempt in range(max_retries):
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
            headers=headers,
            json=payload,
            timeout=300
        )

        if response.status_code == 200:
            result = response.json()
            learning_content = result['candidates'][0]['content']['parts'][0]['text']

            # 学習データを保存
            os.makedirs('学習データ', exist_ok=True)
            with open(f'学習データ/分析_{yesterday}.md', 'w', encoding='utf-8') as f:
                f.write(f"# 学習データ分析（{yesterday}）\n\n{learning_content}")
            print(f"✅ 学習データ保存完了: 学習データ/分析_{yesterday}.md")

            # 成功事例と失敗事例を別ファイルに分離保存
            os.makedirs('成功事例', exist_ok=True)
            os.makedirs('失敗事例', exist_ok=True)

            # 簡易的に成功事例セクションを抽出
            if '## 成功事例' in learning_content and '## 失敗事例' in learning_content:
                success_section = learning_content.split('## 失敗事例')[0].replace('## 成功事例', '').strip()
                failure_section = learning_content.split('## 失敗事例')[1].strip()

                with open(f'成功事例/{yesterday}.md', 'w', encoding='utf-8') as f:
                    f.write(f"# 成功事例（{yesterday}）\n\n{success_section}")

                with open(f'失敗事例/{yesterday}.md', 'w', encoding='utf-8') as f:
                    f.write(f"# 失敗事例（{yesterday}）\n\n{failure_section}")

                print(f"✅ 成功事例・失敗事例 分離保存完了")
            break
        elif response.status_code == 503:
            if attempt < max_retries - 1:
                print(f"⚠️ API 過負荷。{retry_delay}秒待機後リトライ...")
                time.sleep(retry_delay)
            else:
                print(f"❌ 最終試行でも 503 エラー")
                exit(1)
        else:
            print(f"❌ API エラー: {response.status_code}")
            print(response.text)
            exit(1)
    except Exception as e:
        print(f"❌ 例外: {str(e)}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            raise
