#!/usr/bin/env python3
"""COO判定からテーマを抽出してテーマ管理ファイルを更新"""
import os
import re
from datetime import datetime, timedelta

today = datetime.now().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# 本日のCOO判定を読み込む
coo_file = f'運営ログ/COO判定_{today}.md'
if not os.path.exists(coo_file):
    print(f"⚠️ COO判定ファイルが見つかりません: {coo_file}")
    exit(0)

with open(coo_file, 'r', encoding='utf-8') as f:
    judgment = f.read()

# 現在のテーマファイルを読み込む
theme_file = '運営ログ/現在テーマ.md'
current_theme_name = "未設定"
current_version = "1.0"
current_start_date = today

if os.path.exists(theme_file):
    with open(theme_file, 'r', encoding='utf-8') as f:
        current = f.read()
    name_match = re.search(r'テーマ名\n(.+)', current)
    ver_match = re.search(r'バージョン\nv([\d.]+)', current)
    date_match = re.search(r'開始日\n(.+)', current)
    if name_match:
        current_theme_name = name_match.group(1).strip()
    if ver_match:
        current_version = ver_match.group(1).strip()
    if date_match:
        current_start_date = date_match.group(1).strip()

# COO判定からテーマ判定結果セクションを抽出
theme_section = ""
if "テーマ判定結果" in judgment:
    match = re.search(r'テーマ判定結果\n(.*?)(?=\n##|\Z)', judgment, re.DOTALL)
    if match:
        theme_section = match.group(1).strip()

# 判定・バージョン・テーマ名を抽出
change_match = re.search(r'判定[：:]\s*(継続|変更推奨)', theme_section)
version_match = re.search(r'v([\d.]+)\s*(?:→\s*v([\d.]+))?', theme_section)
new_theme_match = re.search(r'新テーマ[（(]変更の場合[)）][：:]\s*(.+)', theme_section)
current_theme_match = re.search(r'現在テーマ[：:]\s*(.+)', theme_section)

is_change = change_match and '変更' in change_match.group(1)

if is_change and new_theme_match:
    new_theme_name = new_theme_match.group(1).strip()
    new_version = "1.0"
    new_start_date = today
    status = "新テーマ（変更）"
else:
    new_theme_name = current_theme_match.group(1).strip() if current_theme_match else current_theme_name
    # バージョンをインクリメント
    try:
        major, minor = current_version.split('.')
        new_version = f"{major}.{int(minor) + 1}"
    except:
        new_version = "1.1"
    new_start_date = current_start_date
    status = "継続改善中"

# テーマファイルを更新
os.makedirs('運営ログ', exist_ok=True)
theme_content = f"# 現在の商品テーマ\n\n"
theme_content += f"## テーマ名\n{new_theme_name}\n\n"
theme_content += f"## バージョン\nv{new_version}\n\n"
theme_content += f"## 開始日\n{new_start_date}\n\n"
theme_content += f"## ステータス\n{status}\n\n"
theme_content += f"## 最終更新\n{today}\n\n"
theme_content += f"## COO判定サマリー（{today}）\n{theme_section[:600] if theme_section else '判定データなし'}\n"

with open(theme_file, 'w', encoding='utf-8') as f:
    f.write(theme_content)

print(f"✅ テーマファイル更新: {'変更' if is_change else '継続'} → {new_theme_name} v{new_version}")
