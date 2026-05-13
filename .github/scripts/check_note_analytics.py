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
            # ログインページを開いてスクショ（デバッグ用）
            print("🔑 ログイン中...")
            os.makedirs('運営ログ', exist_ok=True)
            page.goto('https://note.com/login', wait_until='domcontentloaded', timeout=60000)
            page.wait_for_timeout(3000)
            page.screenshot(path=f'運営ログ/note_login_{today}.png')
            print("  📸 ログインページのスクリーンショット保存")

            # セレクタを複数試す
            email_selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="メール"]',
                'input[placeholder*="mail"]',
                'input[autocomplete="email"]',
            ]
            email_filled = False
            for sel in email_selectors:
                try:
                    page.wait_for_selector(sel, timeout=5000)
                    page.fill(sel, NOTE_EMAIL)
                    print(f"  ✅ メール入力: {sel}")
                    email_filled = True
                    break
                except Exception:
                    continue

            if not email_filled:
                # 全inputタグを列挙してデバッグ
                inputs = page.query_selector_all('input')
                print(f"  ⚠️ inputタグ一覧({len(inputs)}個):")
                for inp in inputs:
                    print(f"    type={inp.get_attribute('type')} name={inp.get_attribute('name')} placeholder={inp.get_attribute('placeholder')}")
                raise Exception("メール入力フィールドが見つかりません")

            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
            ]
            for sel in password_selectors:
                try:
                    page.fill(sel, NOTE_PASSWORD)
                    print(f"  ✅ パスワード入力: {sel}")
                    break
                except Exception:
                    continue

            # ログインボタンをクリック
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("ログイン")',
                'input[type="submit"]',
            ]
            for sel in submit_selectors:
                try:
                    page.click(sel)
                    print(f"  ✅ ログインボタン: {sel}")
                    break
                except Exception:
                    continue

            page.wait_for_load_state('networkidle', timeout=20000)
            print(f"  現在URL: {page.url}")

            # ホームに遷移してダッシュボードリンクを探す
            print("📈 ホームページ取得中...")
            page.goto('https://note.com/', wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)
            page.screenshot(path=f'運営ログ/note_home_{today}.png')
            print("  📸 ホームスクリーンショット保存")

            # クリエイタースタジオ・ダッシュボードのリンクを探してクリック
            dashboard_text = ""
            dashboard_clicked = False
            dashboard_selectors = [
                'a[href*="dashboard"]',
                'a[href*="creator"]',
                'a:has-text("ダッシュボード")',
                'a:has-text("クリエイター")',
                'a:has-text("管理")',
            ]
            for sel in dashboard_selectors:
                try:
                    el = page.query_selector(sel)
                    if el:
                        href = el.get_attribute('href')
                        print(f"  ✅ ダッシュボードリンク発見: {href}")
                        el.click()
                        page.wait_for_load_state('networkidle', timeout=20000)
                        page.wait_for_timeout(3000)
                        page.screenshot(path=f'運営ログ/note_dashboard_{today}.png')
                        dashboard_text = page.inner_text('body')
                        dashboard_clicked = True
                        print(f"  📸 ダッシュボードスクリーンショット保存: {page.url}")
                        break
                except Exception:
                    continue

            if not dashboard_clicked:
                print("  ⚠️ ダッシュボードリンクが見つかりません。ホームの全リンクを列挙:")
                links = page.query_selector_all('a[href]')
                for link in links[:30]:
                    print(f"    {link.get_attribute('href')}")
                dashboard_text = page.inner_text('body')

            # アナリティクス（スタッツ）ページを試す
            stats_text = ""
            page.goto('https://note.com/stats', wait_until='networkidle', timeout=20000)
            page.wait_for_timeout(3000)
            page.screenshot(path=f'運営ログ/note_stats_{today}.png')
            stats_body = page.inner_text('body')
            if '見つかりません' not in stats_body[:200]:
                stats_text = stats_body
                print(f"  ✅ /stats ページ取得成功")
            else:
                stats_text = "（/stats ページが見つかりませんでした）"
                print(f"  ⚠️ /stats は 404")

            analytics = {
                'date': today,
                'dashboard_text': dashboard_text[:3000],
                'stats_text': stats_text[:3000],
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
    report += f"## アナリティクス\n\n"
    report += f"```\n{analytics['stats_text'][:2000]}\n```\n\n"
    report += f"## スクリーンショット\n\n"
    report += f"- `note_home_{today}.png` — ホーム\n"
    report += f"- `note_dashboard_{today}.png` — ダッシュボード\n"
    report += f"- `note_stats_{today}.png` — スタッツページ\n"

    report_path = f'運営ログ/note_アナリティクス_{today}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ レポート保存: {report_path}")
    print("ℹ️ スクリーンショットも 運営ログ/ に保存されています")
else:
    print("❌ アナリティクス取得失敗")
    exit(1)
