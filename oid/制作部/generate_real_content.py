#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実際の販売コンテンツを生成（Gemini API使用）
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

class ContentGenerator:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_path = base_path

        self.products = {
            "AI時代の個人スキル販売術": {
                "dir": "生成物・商品/素材/AI時代の個人スキル販売術",
                "files": {
                    "営業メール10パターン.txt": "フリーランスが実際に使える営業メール10パターン。具体的なメール文をテンプレート形式で提供。改変可能な形式。",
                    "営業フロー自動化シート.txt": "営業プロセスをステップバイステップで自動化するためのチェックリストとフロー図。ExcelやGoogleスプレッドシート対応。",
                    "業界別テンプレ集.txt": "IT、マーケティング、デザイン、コンサルなど業界別の営業アプローチテンプレート。すぐに使える具体例。"
                }
            },
            "SNS運用自動化キット": {
                "dir": "生成物・商品/素材/SNS運用自動化キット",
                "files": {
                    "30日分SNS投稿テンプレート.txt": "30日分のSNS投稿文テンプレート。毎日のコンテンツアイデア、ハッシュタグ、投稿タイミング付き。",
                    "キャプション自動生成ツール.txt": "Gemini/ChatGPTに渡すプロンプト集。これを使えば誰でも自動生成できるキャプション文。",
                    "トレンド分析ガイド.txt": "SNS市場トレンドの分析方法と、実際の成功事例から学べる内容。バイラルコンテンツの特徴分析。",
                    "投稿カレンダー.txt": "月間投稿スケジュール。最適な投稿時間、曜日別テーマ、キャンペーン計画表。"
                }
            },
            "初心者向けAI活用ガイド": {
                "dir": "生成物・商品/素材/初心者向けAI活用ガイド",
                "files": {
                    "ChatGPT実践例.txt": "ChatGPTを使った実務20個の実践例。ビジネスメール作成、企画書作成、コード生成など。",
                    "Gemini実践例.txt": "Googleが提供するGeminiの実践例。画像解析、長文処理、実際のビジネスケーススタディ。",
                    "実務チェックリスト.txt": "AI導入時のチェックリスト。セキュリティ確認、著作権、データ管理、コンプライアンス。",
                    "よくある失敗集.txt": "AI初心者が陥る10個の失敗パターンと、その対策方法。実例ベースのトラブルシューティング。",
                    "業務別プロンプト集.txt": "営業、企画、カスタマーサポート、HR、経営企画など業務別のプロンプト集。コピペで使える。"
                }
            }
        }

    def generate_content_for_file(self, product_name, file_name, description):
        """1つのファイルの内容をGeminiで生成"""
        prompt = f"""
あなたはプロのコンテンツライターです。

商品: {product_name}
ファイル: {file_name}
内容: {description}

このファイルの詳細な内容を日本語で生成してください。

要件:
1. 実際に使えるテンプレート、チェックリスト、実例を含める
2. すぐに実務に活かせる具体的な内容
3. フォーマットはテキスト形式（Markdown可）
4. 長さ: 1000-2000文字程度
5. タイトルと章立てを含める
6. コピー&ペーストで使えるテンプレートや例文を含める

生成してください:
"""

        response = model.generate_content(prompt)
        return response.text

    def run(self):
        """すべての商品コンテンツを生成"""
        print("[制作部] 実際の販売コンテンツを生成中...\n")

        for product_name, product_info in self.products.items():
            print(f"【{product_name}】")

            dir_path = Path(os.path.join(self.base_path, product_info["dir"]))
            dir_path.mkdir(parents=True, exist_ok=True)

            for file_name, file_description in product_info["files"].items():
                print(f"  生成中: {file_name}...")

                try:
                    # コンテンツ生成
                    content = self.generate_content_for_file(
                        product_name,
                        file_name,
                        file_description
                    )

                    # ファイルに書き込み
                    file_path = dir_path / file_name
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"    ✅ 完成")

                except Exception as e:
                    print(f"    ❌ エラー: {e}")

            print()

        print("✅ すべてのコンテンツ生成完了")

if __name__ == "__main__":
    generator = ContentGenerator()
    generator.run()
