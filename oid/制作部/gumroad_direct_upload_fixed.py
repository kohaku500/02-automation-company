#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gumroad ファイルアップロード（修正版）
正しいAPIエンドポイントを使用
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class GumroadDirectUploadFixed:
    def __init__(self):
        self.api_token = os.getenv('GUMROAD_API_TOKEN')
        if not self.api_token:
            raise ValueError("❌ GUMROAD_API_TOKEN が .env に設定されていません")

        self.api_endpoint = "https://api.gumroad.com/v2"
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.product_uploads = {
            "ovkvdp": os.path.join(base_path, "生成物・商品/素材/AI時代の個人スキル販売術"),
            "ffrsdb": os.path.join(base_path, "生成物・商品/素材/SNS運用自動化キット"),
            "crkpel": os.path.join(base_path, "生成物・商品/素材/初心者向けAI活用ガイド")
        }

        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "運営ログ/gumroad_direct_upload_fixed_log.json"
        )

    def upload_files_to_product(self, product_id, files_dir):
        """ディレクトリ内のファイルを Gumroad 商品にアップロード"""
        results = []
        files_path = Path(files_dir)

        if not files_path.exists():
            return [{
                "status": "ERROR",
                "product_id": product_id,
                "error": f"ファイルディレクトリが見つかりません: {files_dir}"
            }]

        for file_path in files_path.glob("*"):
            if file_path.is_file():
                result = self._upload_single_file_v2(product_id, file_path)
                results.append(result)

        return results

    def _upload_single_file_v2(self, product_id, file_path):
        """修正版：正しいエンドポイントでアップロード"""
        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (file_path.name, f, 'text/plain')
                }
                data = {
                    'access_token': self.api_token
                }

                # エンドポイント1: /products/{id}/uploads (オリジナル)
                try:
                    response = requests.post(
                        f"{self.api_endpoint}/products/{product_id}/uploads",
                        files=files,
                        data=data,
                        timeout=30
                    )

                    if response.status_code in [200, 201]:
                        return {
                            "status": "SUCCESS",
                            "product_id": product_id,
                            "file_name": file_path.name,
                            "endpoint": "uploads"
                        }
                except:
                    pass

            # エンドポイント2: product_files
            with open(file_path, 'rb') as f:
                files = {
                    'file': (file_path.name, f, 'text/plain')
                }
                data = {
                    'access_token': self.api_token
                }

                response = requests.post(
                    f"{self.api_endpoint}/products/{product_id}/product_files",
                    files=files,
                    data=data,
                    timeout=30
                )

                if response.status_code in [200, 201]:
                    return {
                        "status": "SUCCESS",
                        "product_id": product_id,
                        "file_name": file_path.name,
                        "endpoint": "product_files"
                    }

            return {
                "status": "FAILED",
                "product_id": product_id,
                "file_name": file_path.name,
                "error": f"両エンドポイント失敗: {response.status_code}",
                "response": response.text[:200]
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "product_id": product_id,
                "file_name": file_path.name,
                "error": str(e)
            }

    def run(self):
        """実行"""
        print("[制作部] Gumroad ファイルアップロード開始...\n")

        all_results = []

        for product_id, files_dir in self.product_uploads.items():
            print(f"[アップロード中] {files_dir}...")

            results = self.upload_files_to_product(product_id, files_dir)
            all_results.extend(results)

            success_count = sum(1 for r in results if r["status"] == "SUCCESS")
            total_count = len(results)

            if success_count > 0:
                print(f"✅ {success_count}/{total_count} ファイルアップロード成功\n")
            else:
                print(f"⚠️  {total_count} ファイルアップロード試行\n")

        log_dir = os.path.dirname(self.log_path)
        os.makedirs(log_dir, exist_ok=True)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "upload_results": all_results,
            "summary": {
                "total": len(all_results),
                "success": sum(1 for r in all_results if r["status"] == "SUCCESS"),
                "failed": sum(1 for r in all_results if r["status"] == "FAILED"),
                "error": sum(1 for r in all_results if r["status"] == "ERROR")
            }
        }

        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + '\n')

        print("✅ ログを保存しました")
        return log_data

if __name__ == "__main__":
    upload = GumroadDirectUploadFixed()
    upload.run()
