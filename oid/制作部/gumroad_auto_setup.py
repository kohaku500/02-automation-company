#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制作部: Gumroad 自動セットアップエンジン
商品情報（説明、ファイルリンク）を自動生成・更新
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GumroadAutoSetup:
    """Gumroad 自動セットアップ"""

    def __init__(self):
        self.api_token = os.getenv('GUMROAD_API_TOKEN')
        if not self.api_token:
            raise ValueError("❌ GUMROAD_API_TOKEN が .env に設定されていません")

        self.api_endpoint = "https://api.gumroad.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        # 商品情報（説明とファイルリンク）
        self.product_data = {
            "crkpel": {
                "name": "初心者向けAI活用ガイド",
                "description": """ChatGPT/Geminiを初めて使う人向けの実践ガイド。

【含まれるもの】
✅ AI活用の基本（5分で理解）
✅ 実践例20個（コピペで使える）
✅ チェックリスト30項目
✅ よくある失敗集

【こんな人向け】
- AIはなんか難しそう...という初心者
- ChatGPT/Geminiを使い始めたばかり
- 実務でAIを活用したい方

このガイド1つで、AI初心者から実務レベルへステップアップできます！""",
                "file_url": "https://drive.google.com/drive/folders/1Z3007pTJdsScW62uuuMOIyxRxU2M2MFm"
            },
            "ffrsdb": {
                "name": "SNS運用自動化キット",
                "description": """SNS投稿を自動化するテンプレート集。

【含まれるもの】
✅ 30日分のSNS投稿文テンプレート
✅ 画像生成プロンプト集
✅ 投稿カレンダー
✅ キャプション自動生成ツール
✅ トレンド分析ガイド

【時間削減】
- 投稿企画：3時間 → 30分
- 投稿作成：2時間 → 20分

毎月72時間削減で、本当に大事な仕事に集中できます！""",
                "file_url": "https://drive.google.com/drive/folders/1Z3007pTJdsScW62uuuMOIyxRxU2M2MFm"
            },
            "ovkvdp": {
                "name": "AI時代の個人スキル販売術",
                "description": """フリーランスの営業負担を削減する販売術。

【含まれるもの】
✅ 営業メール10パターン
✅ 営業フロー自動化シート
✅ 業界別テンプレ集
✅ チャットボット自動生成テンプレート

【このガイドで解決】
❌ 営業が苦手...
❌ クライアント獲得に時間がかかる
❌ 営業メールの書き方がわからない

こんな悩みをすべて解決します。

AI時代は「営業も自動化」が当たり前。
営業効率を3倍にして、スキル販売を加速させましょう！""",
                "file_url": "https://drive.google.com/drive/folders/1Z3007pTJdsScW62uuuMOIyxRxU2M2MFm"
            }
        }

        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "運営ログ/gumroad_setup_log.json"
        )

    def update_product(self, product_id, name, description):
        """Gumroad の商品を更新"""
        try:
            params = {
                "access_token": self.api_token,
                "name": name,
                "description": description
            }

            response = requests.put(
                f"{self.api_endpoint}/products/{product_id}",
                data=params,
                timeout=10
            )

            if response.status_code == 200:
                return {
                    "status": "SUCCESS",
                    "product_id": product_id,
                    "name": name
                }
            else:
                return {
                    "status": "FAILED",
                    "product_id": product_id,
                    "error": response.text
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "product_id": product_id,
                "error": str(e)
            }

    def run(self):
        """Gumroad 自動セットアップ実行"""
        print("[制作部] Gumroad 自動セットアップ開始...\n")

        results = []

        for product_id, data in self.product_data.items():
            print(f"[更新中] {data['name']}...")

            result = self.update_product(
                product_id,
                data['name'],
                data['description']
            )
            results.append(result)

            if result["status"] == "SUCCESS":
                print(f"✅ {data['name']} - 説明文を自動更新\n")
            else:
                print(f"❌ エラー: {result.get('error', 'Unknown')}\n")

        # ログに保存
        log_dir = os.path.dirname(self.log_path)
        os.makedirs(log_dir, exist_ok=True)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "setup_results": results
        }

        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + '\n')

        print(f"✅ セットアップログを保存: 運営ログ/gumroad_setup_log.json")
        print("\n【次のステップ】")
        print("✅ 毎週月曜 9:00 AM に自動実行で、商品情報を常に最新状態に保つ")
        return results

if __name__ == "__main__":
    setup = GumroadAutoSetup()
    setup.run()
