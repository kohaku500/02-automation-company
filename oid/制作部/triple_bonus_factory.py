#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
トリプルボーナス工場: 3大特典の自動生成
ライフハック、副業ツール、教育資料をAIが生成
"""

import json
from datetime import datetime

class TripleBonusFactory:
    """3大特典（トリプルボーナス）自動生成"""

    def generate_lifehack(self, business_idea):
        """ライフハック: 作業時間5分短縮のチェックリスト"""
        return {
            "type": "lifehack",
            "title": f"{business_idea['title']} - 実装チェックリスト",
            "format": "markdown",
            "content": {
                "checklist_items": [
                    "ステップ1: 環境セットアップ（2分）",
                    "ステップ2: テンプレート導入（1分）",
                    "ステップ3: 初回テスト実行（1分）",
                    "ステップ4: カスタマイズ（1分）"
                ],
                "time_saving_claim": "5分で業務フローを自動化"
            }
        }

    def generate_side_business_tool(self, business_idea):
        """副業ツール: 0から1を稼ぐテンプレート"""
        return {
            "type": "side_business_tool",
            "title": f"{business_idea['title']} - 実装テンプレート",
            "format": "excel/spreadsheet",
            "content": {
                "template_items": [
                    "顧客リスト管理シート",
                    "価格設定・利益計算ツール",
                    "納品管理チェックリスト",
                    "売上追跡ダッシュボード"
                ],
                "use_case": "そのままコピペで使用可能なテンプレート集"
            }
        }

    def generate_educational_material(self, business_idea):
        """教育資料: 5分で理解できる図解ベースの資料"""
        return {
            "type": "educational_material",
            "title": f"{business_idea['title']} - 図解マスターガイド",
            "format": "pdf",
            "content": {
                "diagram_based": True,
                "learning_time": "5分",
                "structure": [
                    "概要図（全体像）",
                    "ステップ別フロー図",
                    "トラブルシューティング図",
                    "業界別カスタマイズ例"
                ]
            }
        }

    def run(self):
        """3大特典の生成プロセス"""
        print("[制作部] トリプルボーナス生成開始...")

        market_data_path = "../市場データ/current_status.json"
        output_path = "../生成物・商品/output_assets/"

        try:
            with open(market_data_path, 'r', encoding='utf-8') as f:
                market_data = json.load(f)

            for idea in market_data["business_ideas"]:
                bonuses = {
                    "business_idea_id": idea["id"],
                    "platform": idea["platform"],
                    "title": idea["title"],
                    "generated_at": datetime.now().isoformat(),
                    "bonuses": [
                        self.generate_lifehack(idea),
                        self.generate_side_business_tool(idea),
                        self.generate_educational_material(idea)
                    ]
                }

                output_file = f"{output_path}{idea['id']}-bonuses.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(bonuses, f, ensure_ascii=False, indent=2)

                print(f"✓ 3大特典生成完了: {idea['title']}")

        except FileNotFoundError:
            print("⚠ 市場データが見つかりません。researcher.py を先に実行してください。")

if __name__ == "__main__":
    factory = TripleBonusFactory()
    factory.run()
