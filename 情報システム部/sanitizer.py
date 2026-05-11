#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情報システム部: セキュリティスキャン・聖域保護
生成物にオーナーの個人情報や 🔒-会社 フォルダの技術情報が混入していないか検査
"""

import json
import os
import re
from datetime import datetime

class SecuritySanitizer:
    """聖域保護・セキュリティスキャンエンジン"""

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_path = os.path.join(base_dir, "生成物・商品/output_assets/")

        # グループ1: 🔒-会社（機械設計）の機密情報
        self.sacred_zone_patterns = [
            r"takadamakoto30@gmail\.com",  # オーナーメール
            r"takota.*",                    # オーナー名
            r"ナブテスコ",                   # 前職社名
            r"機械設計",                     # 聖域技術領域
            r"ボルト|ボルト計算|トルク計算",  # 機械設計関連技術
            r"BoltSense|SpringSense|BearingSense|ResonSense",  # 聖域商品
            r"JIS B \d+|VDI \d+",           # 聖域仕様・標準
            r"自動設計|自動化システム.*ボルト",  # 機械系自動化技術
        ]

        # グループ2: 02_完全自動化_収益化会社 のビジネス秘密（外部公開禁止）
        self.business_secret_patterns = [
            # 販売プラットフォーム・商品
            r"note|BOOTH|Kindle",           # 販売プラットフォーム
            r"AI時代の個人スキル販売術",     # 商品タイトル
            r"SNS運用自動化キット",         # 商品タイトル
            r"初心者向けAI活用ガイド",       # 商品タイトル
            r"¥1,?500|¥2,?000|¥980",      # 販売価格
            r"市場リサーチ|価格調査|最適価格", # ビジネスプロセス
            r"6月.*有料化|有料化移行",       # ビジネス戦略
            r"月間.*¥50,?000|MRR",         # 売上目標
            r"3大特典|特典パック",          # 商品パッケージング

            # 🔒-会社 関連（絶対秘密）
            r"🔒-会社|🔒会社",              # フォルダ名
            r"BoltSense|SpringSense|BearingSense|ResonSense",  # 聖域商品
            r"ボルト|トルク|機械設計|自動設計", # 機械設計関連
            r"ナブテスコ",                   # 前職企業
            r"takadamakoto30@gmail\.com",   # オーナーメール
        ]

        self.scan_results = []

    def scan_content(self, content_file, scan_type="internal"):
        """
        コンテンツをスキャン
        scan_type: "internal" = 🔒-会社流出チェック
                   "external" = 外部公開禁止チェック
        """
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = json.load(f)

            violations = []

            # チェック対象パターンを選択
            if scan_type == "external":
                patterns = self.business_secret_patterns
            else:
                patterns = self.sacred_zone_patterns

            for pattern in patterns:
                if self._find_pattern_in_obj(content, pattern):
                    violations.append(pattern)

            return {
                "file": content_file,
                "scan_type": scan_type,
                "status": "PASS" if not violations else "FAIL",
                "violations": violations,
                "scanned_at": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "file": content_file,
                "scan_type": scan_type,
                "status": "ERROR",
                "error": str(e)
            }

    def _find_pattern_in_obj(self, obj, pattern):
        """オブジェクト内でパターンを再帰的に探索"""
        import json
        text = json.dumps(obj, ensure_ascii=False)
        return bool(re.search(pattern, text, re.IGNORECASE))

    def run(self, scan_type="internal"):
        """
        セキュリティスキャン実行
        scan_type: "internal" = 内部流出チェック（デフォルト）
                   "external" = 外部公開チェック
        """
        if scan_type == "internal":
            print("[情報システム部] セキュリティスキャン開始...")
            print("🔒 聖域保護: 🔒-会社フォルダの情報流出チェック")
        else:
            print("[情報システム部] 外部公開チェック開始...")
            print("🔐 ビジネス秘密保護: 02_完全自動化_収益化会社のビジネス情報公開禁止チェック")

        try:
            files = [f for f in os.listdir(self.output_path) if f.endswith('.json')]
            for content_file in files:
                result = self.scan_content(f"{self.output_path}{content_file}", scan_type=scan_type)
                self.scan_results.append(result)

                if result["status"] == "PASS":
                    print(f"✓ 安全確認: {content_file}")
                else:
                    print(f"✗ 違反検出: {content_file}")
                    print(f"  違反内容: {result.get('violations', [])}")

        except FileNotFoundError:
            print("⚠ 生成物フォルダが見つかりません。")

        # スキャン結果を保存
        log_file = f"scan_results_{scan_type}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.scan_results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ スキャン結果を保存: {log_file}")
        return self.scan_results

if __name__ == "__main__":
    sanitizer = SecuritySanitizer()
    sanitizer.run()
