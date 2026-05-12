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

prompt = f"""あなたはコンテンツ制作部です。3プラットフォーム向けパッケージを生成してください。

マーケティング企画:
{marketing_content if marketing_content else "（企画案ファイルが見つかりません）"}

以下の3種類を生成:
1. note向け記事（5000文字以上）
2. BOOTH向け（7000文字以上）
3. Kindle向け原稿（10000文字以上）"""

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

        # note, booth, kindle パッケージを分割保存
        with open(f'{package_dir}/note_package.md', 'w', encoding='utf-8') as f:
            f.write(f"# note向けパッケージ\n\n{package_content}")
        with open(f'{package_dir}/booth_package.md', 'w', encoding='utf-8') as f:
            f.write(f"# BOOTH向けパッケージ\n\n{package_content}")
        with open(f'{package_dir}/kindle_manuscript.md', 'w', encoding='utf-8') as f:
            f.write(f"# Kindle向け原稿\n\n{package_content}")

        print(f"✅ 3種の神器生成完了")

        # 2パス目：プレゼン資料生成
        print("🔄 プレゼン資料を生成中...")
        pres_prompt = f"""あなたはプレゼン資料制作部です。以下の内容をベースに、高品質なHTMLスライドプレゼンを生成してください。

【内容】
{package_content[:2000]}

【要件】
- 完全自己完結型HTML（CSS・JavaScriptを全て埋め込む）
- 矢印キーまたはボタンでスライド切り替え
- 10〜15スライド構成
- 1スライド1メッセージ（複数のテーマを混在させない）
- テキスト量：最大180文字以内
- リスト項目：最大3〜5個
- ビジュアル要素：各スライドに必ず1つ以上（アイコン・グラフ・図解等）
- スマホ対応（レスポンシブ）
- Font Awesomeのみ外部CDN使用可
- <!DOCTYPE html>から</html>までの完全なHTMLコードを出力

プロフェッショナルで響くプレゼンのHTMLスライドコードのみを出力してください。"""

        pres_response = call_gemini_api(pres_prompt)

        if pres_response.status_code == 200:
            pres_result = pres_response.json()
            pres_code = pres_result['candidates'][0]['content']['parts'][0]['text']

            # HTMLコードをクリーニング
            if pres_code.startswith('```html'):
                pres_code = pres_code[7:]
            if pres_code.startswith('```'):
                pres_code = pres_code[3:]
            if pres_code.endswith('```'):
                pres_code = pres_code[:-3]
            pres_code = pres_code.strip()

            with open(f'{package_dir}/presentation.html', 'w', encoding='utf-8') as f:
                f.write(pres_code)
            print(f"✅ プレゼン資料生成完了")
        else:
            print(f"❌ プレゼン資料生成失敗: API エラー {pres_response.status_code}")
            print(f"レスポンス: {pres_response.text}")
            exit(1)

        # 3パス目：Webアプリ生成
        print("🔄 Webアプリを生成中...")
        app_prompt = f"""あなたはWebアプリ開発部です。以下のテーマに関する実用的なツール（計算機・診断・チェックリスト・シミュレーター等）をHTMLで生成してください。

【テーマ】
{package_content.split('【')[0] if '【' in package_content else package_content[:500]}

【要件】
- 完全自己完結型HTML（CSS・JavaScriptを全て埋め込む、外部ファイル参照なし）
- HTMLのみ（Markdown説明文は含めない）
- スマホ対応（レスポンシブデザイン）
- ブラウザで開くだけで即実行可能
- 実用的で役立つツール（計算機・診断・チェックリスト・シミュレーター等）
- 外部CDNはBootstrap・Chart.jsのみ使用可
- 個人情報を収集しない
- <!DOCTYPE html>から</html>までの完全なHTMLコードを出力

すぐに使えるHTMLアプリコードのみを出力してください。"""

        app_response = call_gemini_api(app_prompt)

        if app_response.status_code == 200:
            app_result = app_response.json()
            app_code = app_result['candidates'][0]['content']['parts'][0]['text']

            if app_code.startswith('```html'):
                app_code = app_code[7:]
            if app_code.startswith('```'):
                app_code = app_code[3:]
            if app_code.endswith('```'):
                app_code = app_code[:-3]
            app_code = app_code.strip()

            with open(f'{package_dir}/app.html', 'w', encoding='utf-8') as f:
                f.write(app_code)
            print(f"✅ Webアプリ生成完了")
        else:
            print(f"❌ Webアプリ生成失敗: API エラー {app_response.status_code}")
            print(f"レスポンス: {app_response.text}")
            exit(1)

        # 4パス目：使用方法生成
        print("🔄 ユーザーガイドを生成中...")
        guide_prompt = f"""上記のWebアプリの使用方法を、初心者向けにわかりやすく説明するHTMLドキュメントを生成してください。

【内容】
- 画面構成の説明（各要素の役割）
- 使用手順（ステップバイステップ）
- よくある質問と答え
- トラブルシューティング
- スクリーンショット説明（テキスト形式）

【形式】
- 完全自己完結型HTML
- スマホ対応
- 読みやすいデザイン
- 日本語で記述

<!DOCTYPE html>から</html>までの完全なHTMLコードを出力してください。"""

        guide_response = call_gemini_api(guide_prompt)

        if guide_response.status_code == 200:
            guide_result = guide_response.json()
            guide_code = guide_result['candidates'][0]['content']['parts'][0]['text']

            if guide_code.startswith('```html'):
                guide_code = guide_code[7:]
            if guide_code.startswith('```'):
                guide_code = guide_code[3:]
            if guide_code.endswith('```'):
                guide_code = guide_code[:-3]
            guide_code = guide_code.strip()

            with open(f'{package_dir}/user_guide.html', 'w', encoding='utf-8') as f:
                f.write(guide_code)
            print(f"✅ ユーザーガイド生成完了")
        else:
            print(f"❌ ユーザーガイド生成失敗: API エラー {guide_response.status_code}")
            print(f"レスポンス: {guide_response.text}")
            exit(1)

        print(f"\n✅ 全コンテンツ生成完了: {package_dir}")
    else:
        print(f"❌ API エラー: {response.status_code}")
        print(f"レスポンス: {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ エラー: {str(e)}")
    exit(1)
