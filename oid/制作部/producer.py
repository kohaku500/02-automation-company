#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
制作部: メインコンテンツ・デジタル商品の自動生成
AIが生成したコンテンツを、販売可能な形式に整形・最適化
"""

import json
import os
from datetime import datetime

class ContentProducer:
    """コンテンツ自動生成エンジン"""

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.market_data_path = os.path.join(base_dir, "市場データ/current_status.json")
        self.output_path = os.path.join(base_dir, "生成物・商品/output_assets/")

    def generate_content(self, business_idea):
        """AIが生成したコンテンツを最適化"""
        platform = business_idea["platform"]

        # プラットフォーム別の本文を生成
        body = self._generate_body(business_idea)

        content = {
            "business_idea_id": business_idea["id"],
            "platform": platform,
            "title": business_idea["title"],
            "price": business_idea.get("optimal_price", "未定"),
            "description": business_idea.get("pain_point", ""),
            "body": body,
            "bonus_pack": business_idea.get("bonus_pack", []),
            "content_version": "1.0",
            "format": self._determine_format(platform),
            "generated_at": datetime.now().isoformat(),
            "status": "ready_for_posting"
        }
        return content

    def _generate_body(self, business_idea):
        """プラットフォーム別に本文を生成"""
        title = business_idea["title"]
        pain_point = business_idea.get("pain_point", "")
        ai_generation = business_idea.get("ai_generation", "")
        bonus_pack = business_idea.get("bonus_pack", [])
        price = business_idea.get("optimal_price", "")

        # 基本フォーマット
        body = f"""# {title}

## このコンテンツが解決する課題
{pain_point}

## 何が手に入るのか
{ai_generation}

## 📦 3大特典パッケージ
"""
        for i, bonus in enumerate(bonus_pack, 1):
            body += f"\n### 特典 {i}: {bonus}\n"

        body += f"""

## 💰 価格
{price}

---

このコンテンツは、あなたが今すぐ使える実践的なツール・テンプレート・チェックリストをセットで提供します。購入後、すぐに業務に活かせる内容です。

**購入者限定の3大特典**もすべてお渡しします。"""

        return body

    def _determine_format(self, platform):
        """プラットフォームに応じた形式を決定"""
        formats = {
            "note": "markdown",
            "BOOTH": "pdf+html",
            "Kindle": "epub"
        }
        return formats.get(platform, "markdown")

    def run(self):
        """制作プロセス実行"""
        print("[制作部] コンテンツ生成開始...")

        # 市場データを読み込み
        try:
            with open(self.market_data_path, 'r', encoding='utf-8') as f:
                market_data = json.load(f)

            # 出力ディレクトリを作成
            os.makedirs(self.output_path, exist_ok=True)

            for idea in market_data["business_ideas"]:
                content = self.generate_content(idea)
                print(f"✓ 生成完了: {idea['title']}")

                # 生成物を保存
                output_file = f"{self.output_path}{idea['id']}-{idea['platform']}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)

        except FileNotFoundError as e:
            print(f"⚠ エラー: {e}")
            print("⚠ 市場データが見つかりません。researcher.py を先に実行してください。")
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")

if __name__ == "__main__":
    producer = ContentProducer()
    producer.run()
