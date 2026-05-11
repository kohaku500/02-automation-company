#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gumroad セレニウム自動ファイルアップロード
Web UI を自動化してファイルをアップロード
"""

import os
import json
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time

load_dotenv()

class GumroadSeleniumUpload:
    def __init__(self):
        # セレニウムドライバー設定
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')  # ヘッドレスモード

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        # 商品情報
        self.products = {
            "ovkvdp": {
                "name": "AI時代の個人スキル販売術",
                "url": "https://gumroad.com/products/ovkvdp",
                "files_dir": "生成物・商品/素材/AI時代の個人スキル販売術"
            },
            "ffrsdb": {
                "name": "SNS運用自動化キット",
                "url": "https://gumroad.com/products/ffrsdb",
                "files_dir": "生成物・商品/素材/SNS運用自動化キット"
            },
            "crkpel": {
                "name": "初心者向けAI活用ガイド",
                "url": "https://gumroad.com/products/crkpel",
                "files_dir": "生成物・商品/素材/初心者向けAI活用ガイド"
            }
        }

        self.log_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "運営ログ/gumroad_selenium_upload_log.json"
        )

    def login(self):
        """Gumroadにログイン"""
        try:
            self.driver.get('https://gumroad.com/login')
            time.sleep(3)

            # ログイン画面が表示されたかチェック
            self.wait.until(EC.presence_of_element_located((By.NAME, 'email')))

            # メール入力
            email_input = self.driver.find_element(By.NAME, 'email')
            email_input.send_keys('your_email@example.com')

            # パスワード入力
            password_input = self.driver.find_element(By.NAME, 'password')
            password_input.send_keys(os.getenv('GUMROAD_PASSWORD', ''))

            # ログインボタンをクリック
            login_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Log in")]')
            login_button.click()

            time.sleep(5)
            return True

        except Exception as e:
            print(f"❌ ログイン失敗: {e}")
            return False

    def upload_product_files(self, product_id, product_name, files_dir):
        """商品にファイルをアップロード"""
        results = []

        # 編集ページに移動
        product_url = f"https://gumroad.com/products/{product_id}/edit"
        self.driver.get(product_url)
        time.sleep(3)

        # ファイルディレクトリを確認
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files_path = Path(os.path.join(base_path, files_dir))

        if not files_path.exists():
            return [{
                "status": "ERROR",
                "product_id": product_id,
                "error": f"ファイルディレクトリが見つかりません: {files_dir}"
            }]

        # ファイルをアップロード
        for file_path in files_path.glob("*.txt"):
            try:
                # ファイルアップロード入力を見つけ
                file_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
                file_input.send_keys(str(file_path.absolute()))

                time.sleep(2)

                results.append({
                    "status": "SUCCESS",
                    "product_id": product_id,
                    "file_name": file_path.name
                })

            except Exception as e:
                results.append({
                    "status": "ERROR",
                    "product_id": product_id,
                    "file_name": file_path.name,
                    "error": str(e)
                })

        return results

    def run(self):
        """実行"""
        print("[制作部] Gumroad セレニウム自動ファイルアップロード開始...\n")

        all_results = []

        # ログイン
        if not self.login():
            print("❌ ログイン失敗。スキップします。")
            self.driver.quit()
            return

        # 各商品にファイルをアップロード
        for product_id, product_info in self.products.items():
            print(f"[アップロード中] {product_info['name']}...")

            results = self.upload_product_files(
                product_id,
                product_info['name'],
                product_info['files_dir']
            )
            all_results.extend(results)

            success_count = sum(1 for r in results if r["status"] == "SUCCESS")
            total_count = len(results)

            if success_count > 0:
                print(f"✅ {success_count}/{total_count} ファイルアップロード成功\n")
            else:
                print(f"⚠️  {total_count} ファイルアップロード試行\n")

        # ドライバーを終了
        self.driver.quit()

        # ログに保存
        log_dir = os.path.dirname(self.log_path)
        os.makedirs(log_dir, exist_ok=True)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "upload_results": all_results,
            "summary": {
                "total": len(all_results),
                "success": sum(1 for r in all_results if r["status"] == "SUCCESS"),
                "error": sum(1 for r in all_results if r["status"] == "ERROR")
            }
        }

        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_data, ensure_ascii=False) + '\n')

        print("✅ アップロード完了")
        return all_results

if __name__ == "__main__":
    # 注意: GUMROAD_PASSWORDが.envに設定されている必要があります
    uploader = GumroadSeleniumUpload()
    uploader.run()
