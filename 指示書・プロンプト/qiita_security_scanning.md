---
title: Python + Gemini APIで実装する「機密情報自動検出エンジン」：正規表現×JSONスキャンの実務ガイド
tags: Python,Gemini,セキュリティ,自動化,正規表現
private: false
---

# Python + Gemini APIで実装する「機密情報自動検出エンジン」：正規表現×JSONスキャンの実務ガイド

## はじめに

AIが自動生成するコンテンツが増えるにつれ、**機密情報の漏洩リスク**が急速に高まっています。

本記事では、**複数のパターンマッチングレイヤーを持つ自動セキュリティスキャンシステムの実装方法**を、実装コード付きで詳解します。

用途例：
- ✅ AI生成コンテンツの検査
- ✅ 外部公開前の機密情報チェック
- ✅ 複数部門での情報セグメンテーション
- ✅ コンプライアンス要件への自動対応

---

## 背景：なぜ自動セキュリティスキャンが必要か

### 従来の課題

```
人間による目視チェック
├─ 時間がかかる（スケールしない）
├─ 見落としのリスク（属人的）
└─ 複数ルールの並行管理が困難
```

### 解決策：自動スキャンエンジン

```
AIが自動生成したコンテンツ
  ↓
自動スキャン（正規表現 + JSON再帰探索）
  ↓
複数レイヤーの検査ルール並行実行
  ↓
PASS/FAIL 判定 + 違反内容ログ
```

---

## 実装コード：3層スキャンシステム

### 前提

JSONベースのコンテンツを扱い、複数の「検査ルール」を定義する場合を想定します。

### レイヤー1：パターン定義（セキュリティポリシー）

```python
class SecuritySanitizer:
    """複数のセキュリティポリシーを並行管理"""

    def __init__(self):
        # ルール1：内部機密情報
        self.internal_security_patterns = [
            r"person@company\.com",         # 個人メール
            r"president_name",              # 経営者名
            r"previous_company_name",       # 前職企業
            r"core_technology_keyword",     # コア技術
            r"proprietary_product_name",    # 独自商品
        ]

        # ルール2：外部公開禁止項目
        self.external_disclosure_patterns = [
            r"platform_A|platform_B",       # 販売プラットフォーム
            r"product_title_1",             # 商品名
            r"¥\d+,?\d*",                  # 価格情報
            r"business_strategy_keyword",   # ビジネス戦略
        ]

        self.scan_results = []
```

### レイヤー2：再帰的スキャン実装

```python
    def _find_pattern_in_obj(self, obj, pattern):
        """
        JSONオブジェクトをDFS探索し、パターンマッチングを実行
        
        ポイント：
        - リスト、辞書の再帰処理
        - すべてのテキスト値を対象に正規表現マッチング
        """
        import json
        # JSONに変換して、全テキストを統一的に検索
        text = json.dumps(obj, ensure_ascii=False)
        return bool(re.search(pattern, text, re.IGNORECASE))

    def scan_content(self, content_file, scan_type="internal"):
        """
        JSONファイルをスキャン
        
        scan_type:
        - "internal": 内部機密情報の流出チェック
        - "external": 外部公開禁止情報のチェック
        """
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = json.load(f)

            violations = []

            # 検査ルールを選択
            if scan_type == "external":
                patterns = self.external_disclosure_patterns
            else:
                patterns = self.internal_security_patterns

            # 全パターンを並行スキャン
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
                "status": "ERROR",
                "error": str(e)
            }
```

### レイヤー3：バッチ実行＆ロギング

```python
    def run(self, scan_type="internal"):
        """複数ファイルをスキャンしログに記録"""
        print(f"[セキュリティ] {scan_type} スキャン開始...")

        output_path = "./output_assets/"
        
        try:
            files = [f for f in os.listdir(output_path) 
                     if f.endswith('.json')]
            
            for content_file in files:
                result = self.scan_content(
                    f"{output_path}{content_file}",
                    scan_type=scan_type
                )
                self.scan_results.append(result)

                # 結果を即座に表示
                if result["status"] == "PASS":
                    print(f"✓ {content_file}")
                else:
                    print(f"✗ {content_file}")
                    print(f"  違反: {result.get('violations', [])}")

        except FileNotFoundError:
            print("⚠ ファイルが見つかりません")

        # ログを保存
        log_file = f"scan_results_{scan_type}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.scan_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ ログ保存: {log_file}")
        return self.scan_results
```

---

## 実装時のベストプラクティス

### 1. パターン管理の工夫

**❌ ベタ書き（保守困難）**
```python
forbidden = [r"email1", r"email2", r"email3", ...]
```

**✅ グループ化（保守性向上）**
```python
security_groups = {
    "internal": [...],      # 内部秘密
    "external": [...],      # 公開禁止
    "compliance": [...]     # コンプライアンス
}
```

### 2. 正規表現パターンの精度

**❌ 曖昧なパターン**
```python
r"secret"  # 誤マッチが多い
```

**✅ 具体的なパターン**
```python
r"person_name|product_id|price_\d+"  # 精度が高い
```

### 3. スキャン結果の活用

```python
# PASS/FAIL に基づいた分岐
if result["status"] == "FAIL":
    print("❌ 公開禁止: 機密情報が検出されました")
    # 公開をブロック
else:
    print("✅ 安全確認: 公開許可")
    # 次のフェーズへ
```

---

## 実務での活用シーン

### シーン1：AI生成コンテンツの自動検査

```
AI生成コンテンツ
  ↓
sanitizer.run(scan_type="external")
  ↓
PASS → 公開可（Qiita投稿へ）
FAIL → 修正必須（内容見直し）
```

### シーン2：複数部門での情報セグメンテーション

```
部門A（営業戦略）
  検査ルール: 価格、キャンペーン情報
  
部門B（技術）
  検査ルール: ソースコード、内部設計

部門C（人事）
  検査ルール: 給与、人事情報
```

### シーン3：コンプライアンス対応

```
GDPR、個人情報保護法への対応
  ├─ メールアドレス検出
  ├─ 電話番号検出
  ├─ ID番号検出
  └─ 自動フラグ & ログ記録
```

---

## パフォーマンス最適化

### 大規模データでの処理速度

```python
# 複数ファイルを並行処理
from concurrent.futures import ThreadPoolExecutor

def scan_parallel(self, files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(
            self.scan_content,
            files
        )
    return list(results)
```

### メモリ効率

```python
# JSONをそのままメモリに格納しない（大規模データ）
def scan_large_file(self, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # ストリーム処理で行単位にスキャン
        for line in f:
            self._scan_line(line)
```

---

## まとめ：セキュリティ自動化の3つのメリット

| 従来 | 自動スキャン |
|---|---|
| 手動チェック | 全件自動検査 |
| 属人的 | 統一基準適用 |
| スケール困難 | スケーラブル |

**機密情報の漏洩は、会社の信用失墜に直結します。**

本記事で紹介した正規表現ベースのスキャンシステムは、実装も簡単で、カスタマイズも容易です。ぜひ自社のセキュリティ体制に組み込んでみてください。

---

## 参考資料

- [Python正規表現リファレンス](https://docs.python.org/ja/3/library/re.html)
- [Qiita 月間トレンド記事](https://qiita.com/Qiita/items/616e8f6d4f69bd582ab5)
- [JSON処理ベストプラクティス](https://qiita.com)

---

**投稿予定**: 2026-05-03 20:00 JST
**記事ID**: qiita_security_scanning_001
