#!/usr/bin/env python3
"""note.com アナリティクス取得スクリプト（Playwright使用）"""
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

NOTE_EMAIL = os.environ.get('NOTE_EMAIL')
NOTE_PASSWORD = os.environ.get('NOTE_PASSWORD')

if not NOTE_EMAIL or not NOTE_PASSWORD:
    print("❌ NOTE_EMAIL または NOTE_PASSWORD が設定されていません")
    exit(1)

today = datetime.now().strftime('%Y-%m-%d')
os.makedirs('運営ログ', exist_ok=True)
print(f"📊 note.com アナリティクス取得開始: {today}")

def get_note_analytics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        try:
            # ---- ログイン ----
            print("🔑 ログイン中...")
            page.goto('https://note.com/login', wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(2000)

            # メール入力
            for sel in ['input[placeholder*="mail"]', 'input[type="email"]']:
                try:
                    page.wait_for_selector(sel, timeout=5000)
                    page.fill(sel, NOTE_EMAIL)
                    print(f"  メール: {sel}")
                    break
                except Exception:
                    continue

            # パスワード入力
            page.fill('input[type="password"]', NOTE_PASSWORD)
            print("  パスワード: input[type=password]")

            # ログインボタンクリック
            page.screenshot(path=f'運営ログ/note_before_submit_{today}.png')
            try:
                page.click('button:has-text("ログイン")')
            except Exception as e:
                print(f"  ⚠️ ボタンクリック失敗: {e}")

            page.wait_for_timeout(3000)
            page.screenshot(path=f'運営ログ/note_after_submit_{today}.png')
            print(f"  クリック後URL: {page.url}")

            # まだloginページなら Enter キーでも試す
            if 'login' in page.url:
                print("  → Enter キーで再試行...")
                page.keyboard.press('Enter')
                page.wait_for_timeout(3000)
                print(f"  Enter後URL: {page.url}")
                page.screenshot(path=f'運営ログ/note_after_enter_{today}.png')

            # エラーメッセージがあれば表示
            try:
                error_el = page.query_selector('[class*="error"], [class*="Error"], [role="alert"]')
                if error_el:
                    print(f"  ⚠️ エラーメッセージ: {error_el.inner_text()}")
            except Exception:
                pass

            if 'login' not in page.url:
                print(f"  ✅ ログイン成功: {page.url}")
            else:
                print(f"  ❌ ログイン失敗（URLが変わらず）: {page.url}")

            page.wait_for_timeout(2000)

            # ---- ホーム ----
            print("🏠 ホームページ...")
            page.goto('https://note.com/', wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(3000)
            page.screenshot(path=f'運営ログ/note_home_{today}.png')
            print("  📸 ホーム保存")

            # 自分のユーザー名を取得（プロフィールリンクから）
            username = ""
            try:
                profile_link = page.query_selector('a[href^="/"][href$="/"]')
                if profile_link:
                    href = profile_link.get_attribute('href')
                    username = href.strip('/')
                    print(f"  ユーザー名候補: {username}")
            except Exception:
                pass

            # ---- ダッシュボード（SPAなのでhrefが/dashboardのリンクを探す）----
            print("📊 ダッシュボード...")
            dashboard_url = None
            links = page.query_selector_all('a[href]')
            for link in links:
                href = link.get_attribute('href') or ''
                if href == '/dashboard' or href.startswith('/dashboard/') or 'dashboard' == href.lstrip('/'):
                    dashboard_url = f'https://note.com{href}' if href.startswith('/') else href
                    print(f"  ✅ ダッシュボードリンク: {dashboard_url}")
                    break

            if dashboard_url:
                page.goto(dashboard_url, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)
            else:
                # フォールバック: /dashboard を直接開く
                page.goto('https://note.com/dashboard', wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)
                print(f"  フォールバック: {page.url}")

            page.screenshot(path=f'運営ログ/note_dashboard_{today}.png')
            dashboard_text = page.inner_text('body')
            print(f"  📸 ダッシュボード保存: {page.url}")

            # ---- 自分のプロフィールページ（記事・スキ数確認）----
            if username:
                print(f"👤 プロフィールページ ({username})...")
                page.goto(f'https://note.com/{username}', wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)
                page.screenshot(path=f'運営ログ/note_profile_{today}.png')
                profile_text = page.inner_text('body')
                print("  📸 プロフィール保存")
            else:
                profile_text = "（ユーザー名取得失敗）"

            return {
                'date': today,
                'dashboard_text': dashboard_text[:3000],
                'profile_text': profile_text[:3000],
            }

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
    report = f"# note.com アナリティクスレポート {today}\n\n"
    report += f"## ダッシュボード\n\n```\n{analytics['dashboard_text']}\n```\n\n"
    report += f"## プロフィール\n\n```\n{analytics['profile_text']}\n```\n\n"
    report += f"## スクリーンショット\n\n"
    report += f"- `note_home_{today}.png`\n"
    report += f"- `note_dashboard_{today}.png`\n"
    report += f"- `note_profile_{today}.png`\n"

    path = f'運営ログ/note_アナリティクス_{today}.md'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ レポート保存: {path}")
else:
    print("❌ アナリティクス取得失敗")
    exit(1)
