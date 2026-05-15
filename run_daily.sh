#!/bin/bash
# ローカル自動実行スクリプト
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
echo "① コンテンツ生成..."
python3 .github/scripts/generate_content.py
echo ""

echo "② Zennアナリティクス..."
python3 .github/scripts/check_zenn_analytics.py
echo ""

echo "========================================"
echo "自動実行完了: $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "【次のステップ】"
echo "  生成ファイルを確認 → 問題なければ git add & git push"
echo "========================================"
