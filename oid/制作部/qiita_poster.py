#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制作部: Qiita 自動投稿エンジン
生成した記事を Qiita API 経由で自動投稿
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class QiitaPoster:
    """Qiita API 自動投稿エンジン"""

    def __init__(self):
        self.api_token = os.getenv('QIITA_API_TOKEN')
        if not self.api_token:
            raise ValueError("❌ QIITA_API_TOKEN が .env に設定されていません")

        self.api_endpoint = "https://qiita.com/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "運営ログ/qiita_posting_log.json"
        )

    def extract_article_content(self, article_file):
        """マークダウンから Qiita 投稿用データを抽出"""
        with open(article_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # YAML フロントマッター解析
        lines = content.split('\n')
        metadata = {}
        body_start = 0

        if lines[0].strip() == '---':
            in_frontmatter = True
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    body_start = i + 1
                    break
                key_value = lines[i].split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()

                    # リスト型フィールドの処理
                    if key == 'tags':
                        metadata[key] = [tag.strip() for tag in value.split(',')]
                    else:
                        metadata[key] = value

        body = '\n'.join(lines[body_start:]).strip()

        return {
            "title": metadata.get("title", "Untitled"),
            "body": body,
            "tags": [
                {"name": tag} for tag in metadata.get("tags", [])
            ],
            "private": metadata.get("private", "false").lower() == "true"
        }

    def post_to_qiita(self, article_data):
        """Qiita API に投稿"""
        try:
            print(f"[Qiita投稿] {article_data['title']} を投稿中...")

            response = requests.post(
                f"{self.api_endpoint}/items",
                json=article_data,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 201:
                result = response.json()
                post_url = result.get('url', '')
                print(f"✅ 投稿成功: {article_data['title']}")
                print(f"   URL: https://qiita.com{post_url}")
                return {
                    "status": "SUCCESS",
                    "title": article_data['title'],
                    "url": f"https://qiita.com{post_url}",
                    "posted_at": datetime.now().isoformat()
                }
            else:
                print(f"❌ 投稿失敗 (HTTP {response.status_code})")
                print(f"   エラー: {response.text}")
                return {
                    "status": "FAILED",
                    "title": article_data['title'],
                    "error": response.text,
                    "posted_at": datetime.now().isoformat()
                }

        except requests.exceptions.RequestException as e:
            print(f"❌ ネットワークエラー: {str(e)}")
            return {
                "status": "ERROR",
                "title": article_data['title'],
                "error": str(e),
                "posted_at": datetime.now().isoformat()
            }

    def run(self, article_file_name):
        """Qiita 投稿実行"""
        print("[制作部] Qiita 自動投稿開始...\n")

        article_draft = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            f"指示書・プロンプト/{article_file_name}"
        )

        if not os.path.exists(article_draft):
            print(f"⚠ 記事ファイルが見つかりません: {article_draft}")
            return

        try:
            # 記事データを抽出
            article_data = self.extract_article_content(article_draft)

            # Qiita に投稿
            result = self.post_to_qiita(article_data)

            # ログに記録
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(result, ensure_ascii=False) + '\n')

            print(f"\n✅ Qiita 投稿ログを保存: {self.log_path}")

        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            error_result = {
                "status": "ERROR",
                "error": str(e),
                "posted_at": datetime.now().isoformat()
            }
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(error_result, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    import sys
    article_name = sys.argv[1] if len(sys.argv) > 1 else "qiita_security_scanning.md"
    poster = QiitaPoster()
    poster.run(article_name)
