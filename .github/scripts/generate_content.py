#!/usr/bin/env python3
import os
import time
from datetime import datetime
import requests
import json

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY が設定されていません")
    exit(1)

print(f"✅ API キーが設定されている（長さ: {len(api_key)}文字）")

def call_gemini_api(prompt, max_retries=3, retry_delay=10):
    """リトライ機能付き Gemini API 呼び出し"""
    headers = {'Content-Type': 'application/json'}
    payload = {'contents': [{'parts': [{'text': prompt}]}]}

    print(f"📊 [デバッグ] プロンプト長: {len(prompt)}文字, リトライ回数: {max_retries}")

    for attempt in range(max_retries):
        try:
            print(f"📊 [デバッグ] API 呼び出し試行 {attempt+1}/{max_retries}")
            response = requests.post(
                f'https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}',
                headers=headers,
                json=payload,
                timeout=300
            )

            print(f"📊 [デバッグ] ステータスコード: {response.status_code}")

            if response.status_code == 200:
                print(f"✅ API 呼び出し成功")
                return response
            elif response.status_code == 503:
                if attempt < max_retries - 1:
                    print(f"⚠️ API 過負荷（503）。{retry_delay}秒待機後に再試行します...（試行 {attempt+1}/{max_retries}）")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"❌ 最終試行でも 503 エラー")
                    return response
            else:
                print(f"❌ API エラー: {response.status_code}")
                print(f"📊 [デバッグ] レスポンス: {response.text[:500]}")
                return response
        except Exception as e:
            print(f"❌ 例外エラー: {str(e)}")
            if attempt < max_retries - 1:
                print(f"⚠️ {retry_delay}秒待機後に再試行します...（試行 {attempt+1}/{max_retries}）")
                time.sleep(retry_delay)
            else:
                raise

    return response

today = datetime.now().strftime('%Y-%m-%d')
marketing_file = f'商品企画/企画案_{today}.md'
marketing_content = ""

if os.path.exists(marketing_file):
    with open(marketing_file, 'r', encoding='utf-8') as f:
        marketing_content = f.read()

# 学習データ（過去7日間の成功・失敗事例）を読み込む
from datetime import timedelta
success_cases = ""
failure_cases = ""
for i in range(1, 8):
    past_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    if os.path.exists(f'成功事例/{past_date}.md'):
        with open(f'成功事例/{past_date}.md', 'r', encoding='utf-8') as f:
            success_cases += f.read()[:600] + "\n\n"
    if os.path.exists(f'失敗事例/{past_date}.md'):
        with open(f'失敗事例/{past_date}.md', 'r', encoding='utf-8') as f:
            failure_cases += f.read()[:600] + "\n\n"
if success_cases:
    print(f"✅ 過去7日の成功事例を読み込み")
if failure_cases:
    print(f"✅ 過去7日の失敗事例を読み込み")

prompt = f"""あなたはコンテンツ制作部です。3プラットフォーム向けパッケージを生成してください。

マーケティング企画:
{marketing_content if marketing_content else "（企画案ファイルが見つかりません）"}

# 過去7日間の成功事例（再現すべきパターン）
{success_cases if success_cases else "（過去事例なし）"}

# 過去7日間の失敗事例（避けるべきパターン）
{failure_cases if failure_cases else "（過去事例なし）"}

以下の3種類を生成:
1. note向け記事（5000文字以上）
2. BOOTH向け（7000文字以上）
3. Kindle向け原稿（10000文字以上）

成功事例のパターンを活用し、失敗事例のパターンを避けてください。"""

print("🔄 Gemini API を呼び出し中...")

try:
    response = call_gemini_api(prompt)

    if response.status_code == 200:
        result = response.json()
        package_content = result['candidates'][0]['content']['parts'][0]['text']
        package_dir = f'商品パッケージ/{today}'
        os.makedirs(package_dir, exist_ok=True)

        with open(f'{package_dir}/complete_package.md', 'w', encoding='utf-8') as f:
            f.write(package_content)

        print(f"✅ 統合パッケージ生成完了")

        # Pass 1.5: プラットフォーム別最適化
        print("🔄 Pass 1.5: プラットフォーム別最適化中...")

        # note向け最適化
        print("  → note向けパッケージを最適化中...")
        note_prompt = f"""上記の統合パッケージコンテンツを、noteプラットフォーム向けに最適化してください。

【元の統合パッケージ】
{package_content[:3000]}

【note向け最適化の指針】
- 文字数: 5000文字以上
- フォーマット: noteのマークダウン仕様に最適化
- スタイル: 個人的で親しみやすいトーン
- 見出し: 3～5階層で体系化
- CTA: noteの有料マガジン・サポート機能への導線を明示
- 引用・参照: note内での記事の相互参照も含める

【出力】
# note向けパッケージ

【最適化されたコンテンツ】"""

        note_response = call_gemini_api(note_prompt)
        if note_response.status_code == 200:
            note_result = note_response.json()
            note_content = note_result['candidates'][0]['content']['parts'][0]['text']
            with open(f'{package_dir}/note_package.md', 'w', encoding='utf-8') as f:
                f.write(note_content)
            print(f"  ✅ note向けパッケージ完成")
        else:
            print(f"  ❌ note向け最適化失敗: {note_response.status_code}")
            exit(1)

        # booth向け最適化
        print("  → BOOTH向けパッケージを最適化中...")
        booth_prompt = f"""上記の統合パッケージコンテンツを、BOOTHプラットフォーム向けに最適化してください。

【元の統合パッケージ】
{package_content[:3000]}

【BOOTH向け最適化の指針】
- 文字数: 7000文字以上
- フォーマット: BOOTHの商品説明書仕様
- スタイル: 商品の有用性と信頼性を強調
- 構成: 理論的背景→ステップバイステップガイド→ワークシート→FAQ
- ビジュアル: テーブル・箇条書きで見やすく整理
- 価格設定への含意: 「この商品の価値」を明確に提示
- サポート: 購入後のサポート体制を記載

【出力】
# BOOTH向けパッケージ

【最適化されたコンテンツ】"""

        booth_response = call_gemini_api(booth_prompt)
        if booth_response.status_code == 200:
            booth_result = booth_response.json()
            booth_content = booth_result['candidates'][0]['content']['parts'][0]['text']
            with open(f'{package_dir}/booth_package.md', 'w', encoding='utf-8') as f:
                f.write(booth_content)
            print(f"  ✅ BOOTH向けパッケージ完成")
        else:
            print(f"  ❌ BOOTH向け最適化失敗: {booth_response.status_code}")
            exit(1)

        # kindle向け最適化
        print("  → Kindle向け原稿を最適化中...")
        kindle_prompt = f"""上記の統合パッケージコンテンツを、Kindle電子書籍向けに最適化してください。

【元の統合パッケージ】
{package_content[:3000]}

【Kindle向け最適化の指針】
- 文字数: 10000文字以上
- フォーマット: 電子書籍の目次・章立て構成（全5章以上）
- スタイル: 体系的で奥行きのある解説
- 構成: 目次→本文（複数章）→付録（テンプレート・チェックリスト）
- 見出し: 階層的で読みやすい構成（第1章 → 1-1 → 1-1-1）
- ページ分け: 各章が適度な長さで完結
- 付録: テンプレート・ワークシート・チェックリストを明記

【出力】
# Kindle向け原稿

【最適化されたコンテンツ】"""

        kindle_response = call_gemini_api(kindle_prompt)
        if kindle_response.status_code == 200:
            kindle_result = kindle_response.json()
            kindle_content = kindle_result['candidates'][0]['content']['parts'][0]['text']
            with open(f'{package_dir}/kindle_manuscript.md', 'w', encoding='utf-8') as f:
                f.write(kindle_content)
            print(f"  ✅ Kindle向け原稿完成")
        else:
            print(f"  ❌ Kindle向け最適化失敗: {kindle_response.status_code}")
            exit(1)

        print(f"✅ Pass 1.5 完了: プラットフォーム別最適化完成")
        print(f"\n✅ ベースコンテンツ生成完了: {package_dir}")
        print("ℹ️ プレゼン・アプリ・ガイドは各プラットフォーム用ワークフローで生成されます")
    else:
        print(f"❌ API エラー: {response.status_code}")
        print(f"レスポンス: {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ エラー: {str(e)}")
    exit(1)
