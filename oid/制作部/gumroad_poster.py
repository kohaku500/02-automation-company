#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制作部: Gumroad 自動投稿エンジン
Gumroad API を使って商品情報を管理・販売
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GumroadPoster:
    """Gumroad API 自動管理エンジン"""

    def __init__(self):
        self.api_token = os.getenv('GUMROAD_API_TOKEN')
        if not self.api_token:
            raise ValueError("❌ GUMROAD_API_TOKEN が .env に設定されていません")

        self.api_endpoint = "https://api.gumroad.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        # 管理対象の商品ID
        self.products = {
            "ai-sales": "crkpel",           # AI時代の個人スキル販売術
            "sns-kit": "ffrsdb",             # SNS運用自動化キット
            "ai-guide": "ovkvdp"             # 初心者向けAI活用ガイド
        }

        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "運営ログ/gumroad_management_log.json"
        )

    def get_product_info(self, product_id):
        """Gumroad から商品情報を取得"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/products/{product_id}",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                product = response.json().get('product', {})
                return {
                    "status": "SUCCESS",
                    "product_id": product_id,
                    "name": product.get('name', 'N/A'),
                    "price": product.get('price', 0),
                    "published": product.get('published', False),
                    "sales": product.get('sales_count', 0)
                }
            else:
                return {
                    "status": "FAILED",
                    "product_id": product_id,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                }

        except Exception as e:
            return {
                "status": "ERROR",
                "product_id": product_id,
                "error": str(e)
            }

    def run(self):
        """Gumroad 管理実行"""
        print("[制作部] Gumroad 商品管理開始...\n")

        results = []

        for product_name, product_id in self.products.items():
            print(f"[確認中] {product_name} ({product_id})...")

            result = self.get_product_info(product_id)
            results.append(result)

            if result["status"] == "SUCCESS":
                print(f"✅ {result['name']}")
                print(f"   価格: {result['price']}")
                print(f"   販売数: {result['sales']}")
                print(f"   公開: {'公開' if result['published'] else '非公開'}\n")
            else:
                print(f"❌ エラー: {result.get('error', 'Unknown error')}\n")

        # ログに保存
        log_dir = os.path.dirname(self.log_path)
        os.makedirs(log_dir, exist_ok=True)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "products": results
        }

        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + '\n')

        print(f"✅ 管理ログを保存: 運営ログ/gumroad_management_log.json")
        return results

if __name__ == "__main__":
    poster = GumroadPoster()
    poster.run()
