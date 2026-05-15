#!/bin/bash
# ローカル自動実行スクリプト（全部署）
# 実行後、内容を確認してから手動でgit pushしてください

cd /home/makoto1234/makoto_projects/02_完全自動化_収益化会社

# APIキー設定（.envファイルから読み込み）
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | xargs)
fi

echo "========================================"
echo "自動実行開始: $(date '+%Y-%m-%d %H:%M')"
echo "========================================"

echo ""
echo "① COO判定..."
python3 .github/scripts/coo_judgment.py
echo ""

echo "② 秘書室（ToDoリスト生成）..."
python3 .github/scripts/secretary.py
echo ""

echo "③ マーケティング..."
python3 .github/scripts/marketing.py
echo ""

echo "④ コンテンツ生成..."
python3 .github/scripts/generate_content.py
echo ""

echo "⑤ Kindleアセット生成..."
python3 .github/scripts/generate_kindle_assets.py
echo ""

echo "⑥ noteアセット生成..."
python3 .github/scripts/generate_note_assets.py
echo ""

echo "⑦ Zenn公開..."
python3 .github/scripts/publish_to_zenn.py
echo ""

echo "⑧ クライアント管理..."
python3 .github/scripts/client_management.py
echo ""

echo "⑨ ダッシュボード更新..."
python3 .github/scripts/dashboard.py
echo ""

echo "⑩ 学習データ抽出..."
python3 .github/scripts/extract_learning.py
echo ""

echo "⑪ Zennアナリティクス..."
python3 .github/scripts/check_zenn_analytics.py
echo ""

echo "⑫ 秘書室レポート..."
python3 .github/scripts/secretary_report.py
echo ""

echo "========================================"
echo "自動実行完了: $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "【次のステップ】"
echo "  生成ファイルを確認 → 問題なければ git add & git push"
echo "========================================"
