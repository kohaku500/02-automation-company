#!/usr/bin/env python3
"""note.com アナリティクス取得スクリプト（Playwright使用）"""
import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

NOTE_EMAIL = os.environ.get('NOTE_EMAIL')
NOTE_PASSWORD = os.environ.get('NOTE_PASSWORD')

if not NOTE_EMAIL or not NOTE_PASSWORD:
    print("❌ NOTE_EMAIL または NOTE_PASSWORD が設定されていません")
    exit(1)

today = datetime.now().strftime('%Y-%m-%d')
print(f"📊 note.com アナリティクス取得開始: {today}")

def get_note_analytics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        try:
            # ログイン
            print("🔑 ログイン中...")
            page.goto('https://note.com/login', wait_until='networkidle', timeout=30000)

            page.fill('input[name="email"]', NOTE_EMAIL)
            page.fill('input[name="password"]', NOTE_PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_load_state('networkidle', timeout=15000)

            if 'login' in page.url:
                # 別のセレクタで試みる
                try:
                    page.click('button:has-text("ログイン")')
                    page.wait_for_load_state('networkidle', timeout=15000)
                except Exception:
                    pass

            print(f"  現在URL: {page.url}")

            # ダッシュボード統計ページへ
            print("📈 ダッシュボード取得中...")
            page.goto('https://note.com/dashboard/stats', wait_until='networkidle', timeout=30000)

            # スクリーンショット（デバッグ用）
            os.makedirs('運営ログ', exist_ok=True)
            page.screenshot(path=f'運営ログ/note_screenshot_{today}.png')
            print("  📸 スクリーンショット保存")

            # テキスト全体を取得してデータ抽出
            body_text = page.inner_text('body')

            # フォロワー数ページも確認
            page.goto('https://note.com/dashboard', wait_until='networkidle', timeout=30000)
            dashboard_text = page.inner_text('body')

            analytics = {
                'date': today,
                'dashboard_text': dashboard_text[:3000],
                'stats_text': body_text[:3000],
                'url': page.url
            }

            return analytics

        except Exception as e:
            print(f"❌ エラー: {str(e)}")
            try:
                page.screenshot(path=f'運営ログ/note_error_{today}.png')
            except Exception:
                pass
            return None
        finally:
            browser.close()


analytics = get_note_analytics()

if analytics:
    # マークダウンレポート生成
    report = f"# note.com アナリティクスレポート {today}\n\n"
    report += f"## ダッシュボード情報\n\n"
    report += f"```\n{analytics['dashboard_text'][:2000]}\n```\n\n"
    report += f"## 統計ページ情報\n\n"
    report += f"```\n{analytics['stats_text'][:2000]}\n```\n"

    report_path = f'運営ログ/note_アナリティクス_{today}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ レポート保存: {report_path}")
    print("ℹ️ スクリーンショットも 運営ログ/ に保存されています")
else:
    print("❌ アナリティクス取得失敗")
    exit(1)
