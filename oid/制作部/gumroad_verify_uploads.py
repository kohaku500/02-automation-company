#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gumroad ファイルアップロード確認・修正スクリプト
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GumroadVerify:
    def __init__(self):
        self.api_token = os.getenv('GUMROAD_API_TOKEN')
        self.api_endpoint = "https://api.gumroad.com/v2"

        self.products = {
            "ovkvdp": "AI時代の個人スキル販売術",
            "ffrsdb": "SNS運用自動化キット",
            "crkpel": "初心者向けAI活用ガイド"
        }

    def check_product_files(self, product_id):
        """商品のファイル情報を確認"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/products/{product_id}",
                params={"access_token": self.api_token},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json().get('product', {})
                files = data.get('product_files', [])

                return {
                    "status": "SUCCESS",
                    "product_id": product_id,
                    "product_name": data.get('name', 'N/A'),
                    "files_count": len(files),
                    "files": [f.get('filename', 'Unknown') for f in files]
                }
            else:
                return {
                    "status": "FAILED",
                    "product_id": product_id,
                    "error": f"HTTP {response.status_code}: {response.text[:200]}"
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "product_id": product_id,
                "error": str(e)
            }

    def run(self):
        """すべての商品のファイル状況を確認"""
        print("[確認] Gumroad 商品ファイル確認中...\n")

        results = []
        for product_id, product_name in self.products.items():
            result = self.check_product_files(product_id)
            results.append(result)

            if result["status"] == "SUCCESS":
                print(f"✅ {product_name}")
                print(f"   アップロード済みファイル数: {result['files_count']}")
                if result['files']:
                    for file in result['files']:
                        print(f"   - {file}")
                print()
            else:
                print(f"❌ {product_name}: {result.get('error', 'Unknown error')}\n")

        return results

if __name__ == "__main__":
    verify = GumroadVerify()
    verify.run()
