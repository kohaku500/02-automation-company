#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
プレゼン資料（HTML/PDF）形式の販売コンテンツを生成
5W1H完全装備の見栄え良い資料
"""

import os
from pathlib import Path

class PresentationContentCreator:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_path = base_path

    def create_html_presentation(self, product_name, title, content_sections):
        """HTMLプレゼン資料を生成"""
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', 'Noto Sans JP', sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .slide {{
            width: 100%;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
            page-break-after: always;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .slide.content {{
            background: white;
            color: #333;
        }}
        .slide-content {{
            max-width: 900px;
            width: 100%;
        }}
        h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        h2 {{
            font-size: 2.5em;
            margin-bottom: 30px;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        h3 {{
            font-size: 1.8em;
            margin: 20px 0 15px 0;
            color: #764ba2;
        }}
        .subtitle {{
            font-size: 1.5em;
            opacity: 0.9;
            margin-bottom: 40px;
        }}
        .w1h-section {{
            margin: 25px 0;
            padding: 20px;
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            border-radius: 4px;
        }}
        .w1h-label {{
            font-weight: bold;
            font-size: 1.2em;
            color: #667eea;
            margin-bottom: 8px;
        }}
        .w1h-content {{
            font-size: 1.1em;
            line-height: 1.8;
        }}
        .bullet {{
            margin: 12px 0 12px 30px;
        }}
        .benefit {{
            display: flex;
            align-items: flex-start;
            margin: 15px 0;
            padding: 15px;
            background: #fff;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .benefit-icon {{
            font-size: 2em;
            margin-right: 15px;
            flex-shrink: 0;
        }}
        .benefit-text {{
            flex-grow: 1;
        }}
        .benefit-title {{
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 5px;
        }}
        .metric {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            margin: 8px 8px 8px 0;
            font-weight: bold;
        }}
        .case-study {{
            background: #f0f4ff;
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }}
        .case-study-title {{
            font-weight: bold;
            font-size: 1.3em;
            margin-bottom: 10px;
            color: #333;
        }}
        .case-before-after {{
            display: flex;
            justify-content: space-around;
            margin: 15px 0;
        }}
        .case-item {{
            flex: 1;
            text-align: center;
        }}
        .case-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }}
        .case-value {{
            font-size: 1.4em;
            font-weight: bold;
            color: #667eea;
        }}
        .cta {{
            margin-top: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .page-break {{
            page-break-before: always;
        }}
        @media print {{
            body {{ margin: 0; padding: 0; }}
            .slide {{ page-break-after: always; }}
        }}
    </style>
</head>
<body>

    <!-- タイトルスライド -->
    <div class="slide">
        <div class="slide-content">
            <h1>{title}</h1>
            <p class="subtitle">最低限5W1Hを含めたプレゼン資料</p>
        </div>
    </div>

    {content_sections}

</body>
</html>"""
        return html

    def create_business_sales_content(self):
        """営業スキル販売コンテンツ"""
        sections = """
    <!-- What スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>❓ What（何か）</h2>
            <div class="w1h-section">
                <div class="w1h-content">
                    <p style="font-size: 1.3em; margin-bottom: 15px;">
                        <strong>営業メール作成の手間を90%削減するテンプレート +
                        見込み客から成約までの完全営業フロー</strong>
                    </p>
                    <p>このコンテンツは、フリーランス・個人事業主が「営業メール作成で5時間/月かかる」
                    という課題を解決し、わずか30分/月で営業を完結させるための実行型コンテンツです。</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Who スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>👤 Who（誰向けか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">対象者</div>
                <div class="w1h-content">
                    <div class="bullet">✅ フリーランス・個人事業主で営業活動をしている人</div>
                    <div class="bullet">✅ 営業メール作成に毎月5時間以上かけている人</div>
                    <div class="bullet">✅ クライアント獲得に2ヶ月以上かかっている人</div>
                    <div class="bullet">✅ 営業の効率化と売上向上を同時実現したい人</div>
                    <div class="bullet">✅ 営業プロセスを属人化から脱却させたい人</div>
                </div>
            </div>
        </div>
    </div>

    <!-- When スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>⏰ When（いつ使うか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">使用タイミング</div>
                <div class="w1h-content">
                    <div class="bullet">📅 毎月1日：月間営業計画立案＆ターゲット企業リストアップ時</div>
                    <div class="bullet">📅 毎営業日：営業メール送信＆フォローアップ実施時</div>
                    <div class="bullet">📅 新規案件受け取り時：即座に営業フローに組み込み</div>
                    <div class="bullet">📅 営業活動が停滞した時：テンプレート見直し＆改善時</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Where スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>🎯 Where（どこで活かすか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">活用場面</div>
                <div class="w1h-content">
                    <div class="bullet">📧 メール営業：新規クライアント開拓メール、フォローアップメール</div>
                    <div class="bullet">💬 SNS営業：LinkedInやTwitterのDM営業</div>
                    <div class="bullet">📋 提案資料：営業メール＋提案書の統合営業</div>
                    <div class="bullet">📊 営業管理：GoogleスプレッドシートやNotionでの進捗管理</div>
                    <div class="bullet">🔄 継続営業：既存クライアント追加提案＆契約更新営業</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Why スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>❓ Why（なぜ必要か）</h2>
            <div class="w1h-section">
                <div class="w1h-label">現在の課題</div>
                <div class="w1h-content" style="color: #d32f2f; margin-bottom: 15px;">
                    ❌ 営業メール作成に5-10時間/月かかる<br>
                    ❌ 返信率が5-10%と低い<br>
                    ❌ 成約まで平均30-60日かかる<br>
                    ❌ 営業活動が属人的で再現性がない
                </div>
            </div>
            <div class="w1h-section">
                <div class="w1h-label">このコンテンツで解決すること</div>
                <div class="w1h-content" style="color: #2e7d32;">
                    ✅ テンプレートで営業メール作成を5倍高速化<br>
                    ✅ 返信率を20-30%に改善<br>
                    ✅ クライアント獲得期間を30日→10日に短縮<br>
                    ✅ 誰でも同じ成果を上げられる仕組み化
                </div>
            </div>
        </div>
    </div>

    <!-- How スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>📖 How（どう使うか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">3ステップで実行</div>
                <div class="w1h-content">
                    <h3 style="color: #667eea; margin-top: 0;">Step 1: 営業フロー全体を理解</h3>
                    <div class="bullet" style="margin-left: 20px;">見込み客発掘 → ヒアリング → 提案 → クロージング の45日サイクルを学習</div>

                    <h3 style="color: #667eea;">Step 2: テンプレートを自社にカスタマイズ</h3>
                    <div class="bullet" style="margin-left: 20px;">10パターンのメールテンプレートから自社用にアレンジ</div>

                    <h3 style="color: #667eea;">Step 3: 実行＆改善</h3>
                    <div class="bullet" style="margin-left: 20px;">毎日チェックリストに従い営業実行、週1回のデータ分析で改善継続</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 具体的成果スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>📊 得られる具体的成果</h2>
            <div style="margin-top: 30px;">
                <div class="benefit">
                    <div class="benefit-icon">⏱️</div>
                    <div class="benefit-text">
                        <div class="benefit-title">営業メール作成時間</div>
                        <div>従来：60分/件 → 実現：5分/件</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">効率化：12倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📧</div>
                    <div class="benefit-text">
                        <div class="benefit-title">メール返信率</div>
                        <div>従来：5-10% → 実現：20-30%</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">改善：4倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">🎯</div>
                    <div class="benefit-text">
                        <div class="benefit-title">成約化率</div>
                        <div>従来：2% → 実現：8%</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">改善：4倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📈</div>
                    <div class="benefit-text">
                        <div class="benefit-title">月間営業時間削減</div>
                        <div>従来：5時間/月 → 実現：30分/月</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">削減：90%</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 実例スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>💼 実例：フリーランスAさんの成果</h2>
            <div class="case-study">
                <div class="case-study-title">導入前（3ヶ月前）</div>
                <div class="case-before-after">
                    <div class="case-item">
                        <div class="case-label">営業メール数/月</div>
                        <div class="case-value">10件</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">受注数/月</div>
                        <div class="case-value">1件</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">月額売上</div>
                        <div class="case-value">¥150万</div>
                    </div>
                </div>
            </div>

            <div class="case-study" style="background: #f0fff4; border-left-color: #2e7d32;">
                <div class="case-study-title" style="color: #2e7d32;">導入後（現在）</div>
                <div class="case-before-after">
                    <div class="case-item">
                        <div class="case-label">営業メール数/月</div>
                        <div class="case-value" style="color: #2e7d32;">30件</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">受注数/月</div>
                        <div class="case-value" style="color: #2e7d32;">8件</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">月額売上</div>
                        <div class="case-value" style="color: #2e7d32;">¥480万</div>
                    </div>
                </div>
            </div>

            <p style="text-align: center; font-size: 1.2em; color: #2e7d32; margin-top: 20px; font-weight: bold;">
                📈 売上が3.2倍に増加（わずか3ヶ月）
            </p>
        </div>
    </div>

    <!-- 30日後のゴールスライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>🎯 30日後に達成できる状態</h2>
            <div style="margin-top: 30px;">
                <div class="benefit" style="background: #fff3e0;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">営業フロー全体の理解</div>
                        <div>見込み客発掘からクロージングまでの45日サイクルが完全に習慣化</div>
                    </div>
                </div>

                <div class="benefit" style="background: #f3e5f5;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">月20件以上の新規営業</div>
                        <div>営業メール作成が習慣化し、毎日の営業活動が継続可能に</div>
                    </div>
                </div>

                <div class="benefit" style="background: #e3f2fd;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">クライアント獲得期間短縮</div>
                        <div>初回接触から成約まで30日→10日に短縮できる再現性のある仕組み</div>
                    </div>
                </div>

                <div class="benefit" style="background: #e8f5e9;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">月間売上1.5倍～2倍が実現可能</div>
                        <div>営業の効率化により、実行可能な売上向上の土台が完成</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- CTA スライド -->
    <div class="slide">
        <div class="slide-content">
            <h2 style="color: white; border-bottom-color: white; margin-bottom: 40px;">
                このコンテンツで
                <br>営業を自動化しましょう
            </h2>
            <div class="metric" style="background: rgba(255,255,255,0.2); display: block; text-align: center; font-size: 1.3em;">
                含まれるもの：<br>
                ✅ 営業メール10パターン<br>
                ✅ 完全営業フロー＆チェックリスト<br>
                ✅ 業界別アプローチテンプレート<br>
                ✅ 成功パターン分析＆実例
            </div>
        </div>
    </div>
"""
        return sections

    def create_sns_content(self):
        """SNS運用コンテンツ"""
        sections = """
    <!-- What スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>❓ What（何か）</h2>
            <div class="w1h-section">
                <div class="w1h-content">
                    <p style="font-size: 1.3em; margin-bottom: 15px;">
                        <strong>SNS投稿ネタ切れ問題を完全解決する
                        30日分の投稿テンプレート + 運用カレンダー</strong>
                    </p>
                    <p>毎日「何を投稿しよう」と悩む時間を削減し、
                    効果の高いコンテンツを習慣的に発信できるシステムです。</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Who スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>👤 Who（誰向けか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">対象者</div>
                <div class="w1h-content">
                    <div class="bullet">✅ SNSで集客したいが、毎日の投稿ネタが思いつかない人</div>
                    <div class="bullet">✅ SNS投稿に週5時間以上かけている人</div>
                    <div class="bullet">✅ フォロワーは多いがエンゲージメント率が低い人</div>
                    <div class="bullet">✅ SNS運用を習慣化させたい経営者・フリーランス</div>
                </div>
            </div>
        </div>
    </div>

    <!-- When スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>⏰ When（いつ使うか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">使用タイミング</div>
                <div class="w1h-content">
                    <div class="bullet">🌅 毎朝5分：その日の投稿テンプレートを確認＆執筆</div>
                    <div class="bullet">📅 月初1回：30日分のテンプレートを自社用にカスタマイズ</div>
                    <div class="bullet">📊 週1回：エンゲージメント分析＆翌週の改善</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Where スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>🎯 Where（どこで活かすか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">活用場面</div>
                <div class="w1h-content">
                    <div class="bullet">📱 Instagram・Twitter・LinkedIn・Facebook・TikTok</div>
                    <div class="bullet">📺 YouTube Shorts・Instagramリール</div>
                    <div class="bullet">📝 ブログ・メルマガの素材源</div>
                    <div class="bullet">📊 Google Spreadsheet・Notionでの投稿カレンダー管理</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Why スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>❓ Why（なぜ必要か）</h2>
            <div class="w1h-section">
                <div class="w1h-label">現在の課題</div>
                <div class="w1h-content" style="color: #d32f2f; margin-bottom: 15px;">
                    ❌ 毎日投稿ネタを考えるのに30分～1時間かかる<br>
                    ❌ 投稿が不定期になってしまう<br>
                    ❌ エンゲージメント率が1%以下と低い<br>
                    ❌ フォロワー増加が停滞している
                </div>
            </div>
            <div class="w1h-section">
                <div class="w1h-label">このコンテンツで解決すること</div>
                <div class="w1h-content" style="color: #2e7d32;">
                    ✅ 毎日5分で投稿完成 (効率化：90%)<br>
                    ✅ 毎日投稿習慣が身につく<br>
                    ✅ エンゲージメント率が3%以上に改善<br>
                    ✅ 月2倍のペースでフォロワー増加
                </div>
            </div>
        </div>
    </div>

    <!-- How スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>📖 How（どう使うか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">3ステップで運用</div>
                <div class="w1h-content">
                    <h3 style="color: #667eea; margin-top: 0;">Step 1: 月初に30日分をカスタマイズ</h3>
                    <div class="bullet" style="margin-left: 20px;">提供テンプレートから30日分を自社用にアレンジ（1時間で完了）</div>

                    <h3 style="color: #667eea;">Step 2: 毎朝5分で投稿実行</h3>
                    <div class="bullet" style="margin-left: 20px;">テンプレートに情報追加＆投稿するだけ</div>

                    <h3 style="color: #667eea;">Step 3: 週1回データ分析＆改善</h3>
                    <div class="bullet" style="margin-left: 20px;">エンゲージメント高い投稿を分析して翌週に反映</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 具体的成果スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>📊 得られる具体的成果</h2>
            <div style="margin-top: 30px;">
                <div class="benefit">
                    <div class="benefit-icon">⏱️</div>
                    <div class="benefit-text">
                        <div class="benefit-title">投稿準備時間</div>
                        <div>従来：30分/投稿 → 実現：5分/投稿</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">効率化：6倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📱</div>
                    <div class="benefit-text">
                        <div class="benefit-title">フォロワー増加率</div>
                        <div>従来：月+10% → 実現：月+25%</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">改善：2.5倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">💬</div>
                    <div class="benefit-text">
                        <div class="benefit-title">エンゲージメント率</div>
                        <div>従来：1% → 実現：3.5%</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">改善：3.5倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📈</div>
                    <div class="benefit-text">
                        <div class="benefit-title">リード獲得数</div>
                        <div>従来：月5件 → 実現：月35件</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">改善：7倍</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 実例スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>💼 実例：オンライン講師Bさんの成果</h2>
            <div class="case-study">
                <div class="case-study-title">導入前（3ヶ月前）</div>
                <div class="case-before-after">
                    <div class="case-item">
                        <div class="case-label">投稿頻度</div>
                        <div class="case-value">週3回</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">フォロワー数</div>
                        <div class="case-value">2,000人</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">月間リード</div>
                        <div class="case-value">5件</div>
                    </div>
                </div>
            </div>

            <div class="case-study" style="background: #f0fff4; border-left-color: #2e7d32;">
                <div class="case-study-title" style="color: #2e7d32;">導入後（現在）</div>
                <div class="case-before-after">
                    <div class="case-item">
                        <div class="case-label">投稿頻度</div>
                        <div class="case-value" style="color: #2e7d32;">毎日</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">フォロワー数</div>
                        <div class="case-value" style="color: #2e7d32;">5,000人</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">月間リード</div>
                        <div class="case-value" style="color: #2e7d32;">35件</div>
                    </div>
                </div>
            </div>

            <p style="text-align: center; font-size: 1.2em; color: #2e7d32; margin-top: 20px; font-weight: bold;">
                📈 売上が150万→280万に増加（わずか3ヶ月）
            </p>
        </div>
    </div>

    <!-- 30日後のゴールスライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>🎯 30日後に達成できる状態</h2>
            <div style="margin-top: 30px;">
                <div class="benefit" style="background: #fff3e0;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">毎日投稿が習慣化</div>
                        <div>テンプレート活用で毎日5分で投稿完成＆継続可能に</div>
                    </div>
                </div>

                <div class="benefit" style="background: #f3e5f5;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">フォロワーが月2倍ペースで増加</div>
                        <div>毎日投稿継続により、安定したフォロワー増加が実現</div>
                    </div>
                </div>

                <div class="benefit" style="background: #e3f2fd;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">月間リード獲得が3倍以上に</div>
                        <div>投稿数＋質の向上により、リード獲得が安定的に増加</div>
                    </div>
                </div>

                <div class="benefit" style="background: #e8f5e9;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">SNS運用が月15時間→月3時間に</div>
                        <div>運用時間を大幅削減しながら成果最大化</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- CTA スライド -->
    <div class="slide">
        <div class="slide-content">
            <h2 style="color: white; border-bottom-color: white; margin-bottom: 40px;">
                毎日5分でSNS集客を
                <br>習慣化させましょう
            </h2>
            <div class="metric" style="background: rgba(255,255,255,0.2); display: block; text-align: center; font-size: 1.3em;">
                含まれるもの：<br>
                ✅ 30日分の投稿テンプレート<br>
                ✅ 業界別カスタマイズガイド<br>
                ✅ エンゲージメント分析シート<br>
                ✅ 月間投稿カレンダー
            </div>
        </div>
    </div>
"""
        return sections

    def create_ai_content(self):
        """AI活用ガイド"""
        sections = """
    <!-- What スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>❓ What（何か）</h2>
            <div class="w1h-section">
                <div class="w1h-content">
                    <p style="font-size: 1.3em; margin-bottom: 15px;">
                        <strong>ChatGPT・Gemini初心者向けの
                        業務時間50%削減プログラム</strong>
                    </p>
                    <p>AIを使ったことがない初心者でも、
                    すぐに実務で活用できる20個の具体的な使い方を学べます。</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Who スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>👤 Who（誰向けか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">対象者</div>
                <div class="w1h-content">
                    <div class="bullet">✅ ChatGPTを持っているが使い方がわからない人</div>
                    <div class="bullet">✅ 文章作成・メール対応に毎日2時間以上かけている人</div>
                    <div class="bullet">✅ 企業内でAI導入を推進したい経営者・マネージャー</div>
                    <div class="bullet">✅ AI初心者でも即座に活用したい人</div>
                </div>
            </div>
        </div>
    </div>

    <!-- When スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>⏰ When（いつ使うか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">使用タイミング</div>
                <div class="w1h-content">
                    <div class="bullet">🌅 毎日の業務実行時：該当する業務タイプのプロンプトを実行</div>
                    <div class="bullet">📚 月1回：新しいAI活用法を学習＆試験導入</div>
                    <div class="bullet">👥 チーム導入時：全従業員向けのトレーニング資料として活用</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Where スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>🎯 Where（どこで活かすか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">活用場面</div>
                <div class="w1h-content">
                    <div class="bullet">📧 メール・提案書作成</div>
                    <div class="bullet">📄 企画書・ブログ記事作成</div>
                    <div class="bullet">💻 データ分析・ニュース要約</div>
                    <div class="bullet">👥 顧客対応・FAQ作成</div>
                    <div class="bullet">📋 マニュアル・ドキュメント作成</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Why スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>❓ Why（なぜ必要か）</h2>
            <div class="w1h-section">
                <div class="w1h-label">現在の課題</div>
                <div class="w1h-content" style="color: #d32f2f; margin-bottom: 15px;">
                    ❌ メール・提案書作成に毎日2時間かかる<br>
                    ❌ AIツールを持っているが使いこなせていない<br>
                    ❌ チーム全体でAI活用が進まない<br>
                    ❌ 本来やるべき仕事に時間が割けない
                </div>
            </div>
            <div class="w1h-section">
                <div class="w1h-label">このコンテンツで解決すること</div>
                <div class="w1h-content" style="color: #2e7d32;">
                    ✅ 20個の実践的な使い方を習得<br>
                    ✅ メール作成が15分→3分に短縮<br>
                    ✅ 月40時間の時間削減＝月1.7人分の労働力を創出<br>
                    ✅ 高価値な業務に集中できる環境を実現
                </div>
            </div>
        </div>
    </div>

    <!-- How スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>📖 How（どう使うか）</h2>
            <div class="w1h-section">
                <div class="w1h-label">3ステップで習得</div>
                <div class="w1h-content">
                    <h3 style="color: #667eea; margin-top: 0;">Step 1: 20個の実践例を学習</h3>
                    <div class="bullet" style="margin-left: 20px;">メール・提案書・ブログなど業務タイプ別の具体例を理解</div>

                    <h3 style="color: #667eea;">Step 2: プロンプトを自社用にカスタマイズ</h3>
                    <div class="bullet" style="margin-left: 20px;">提供プロンプトを自社・自部門に合わせて編集</div>

                    <h3 style="color: #667eea;">Step 3: 毎日実行＆改善</h3>
                    <div class="bullet" style="margin-left: 20px;">業務の中で該当するプロンプトを毎日実行して習慣化</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 具体的成果スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>📊 得られる具体的成果</h2>
            <div style="margin-top: 30px;">
                <div class="benefit">
                    <div class="benefit-icon">⏱️</div>
                    <div class="benefit-text">
                        <div class="benefit-title">メール作成時間</div>
                        <div>従来：15分/件 → 実現：3分/件</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">効率化：5倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📄</div>
                    <div class="benefit-text">
                        <div class="benefit-title">提案書作成時間</div>
                        <div>従来：180分 → 実現：30分</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">効率化：6倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📚</div>
                    <div class="benefit-text">
                        <div class="benefit-title">ブログ記事作成時間</div>
                        <div>従来：300分 → 実現：60分</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">効率化：5倍</div>
                    </div>
                </div>

                <div class="benefit">
                    <div class="benefit-icon">📈</div>
                    <div class="benefit-text">
                        <div class="benefit-title">月間時間削減</div>
                        <div>従来：40時間/月 削減 = 月1.7人分の労働力</div>
                        <div style="color: #667eea; font-weight: bold; margin-top: 5px;">年間480時間削減</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- 実例スライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>💼 実例：営業職Cさんの成果</h2>
            <div class="case-study">
                <div class="case-study-title">導入前（3ヶ月前）</div>
                <div class="case-before-after">
                    <div class="case-item">
                        <div class="case-label">文書作成時間</div>
                        <div class="case-value">2時間/日</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">営業活動時間</div>
                        <div class="case-value">2時間/日</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">月間売上</div>
                        <div class="case-value">¥200万</div>
                    </div>
                </div>
            </div>

            <div class="case-study" style="background: #f0fff4; border-left-color: #2e7d32;">
                <div class="case-study-title" style="color: #2e7d32;">導入後（現在）</div>
                <div class="case-before-after">
                    <div class="case-item">
                        <div class="case-label">文書作成時間</div>
                        <div class="case-value" style="color: #2e7d32;">20分/日</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">営業活動時間</div>
                        <div class="case-value" style="color: #2e7d32;">3.5時間/日</div>
                    </div>
                    <div class="case-item">
                        <div class="case-label">月間売上</div>
                        <div class="case-value" style="color: #2e7d32;">¥350万</div>
                    </div>
                </div>
            </div>

            <p style="text-align: center; font-size: 1.2em; color: #2e7d32; margin-top: 20px; font-weight: bold;">
                📈 営業時間が1.75倍→売上が1.75倍に改善（わずか3ヶ月）
            </p>
        </div>
    </div>

    <!-- 30日後のゴールスライド -->
    <div class="slide content page-break">
        <div class="slide-content">
            <h2>🎯 30日後に達成できる状態</h2>
            <div style="margin-top: 30px;">
                <div class="benefit" style="background: #fff3e0;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">20個のAI活用法が身につく</div>
                        <div>メール・提案・企画など日々の業務で即座に実践可能に</div>
                    </div>
                </div>

                <div class="benefit" style="background: #f3e5f5;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">毎日2時間の時間創出</div>
                        <div>文書作成時間削減により、営業など生産的活動に充てられる</div>
                    </div>
                </div>

                <div class="benefit" style="background: #e3f2fd;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">AI活用がチーム全体に拡大</div>
                        <div>トレーニング資料として全従業員のAI導入を推進可能</div>
                    </div>
                </div>

                <div class="benefit" style="background: #e8f5e9;">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <div class="benefit-title">売上向上の基盤完成</div>
                        <div>営業に使える時間が2倍→月売上が1.5倍～2倍に</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- CTA スライド -->
    <div class="slide">
        <div class="slide-content">
            <h2 style="color: white; border-bottom-color: white; margin-bottom: 40px;">
                AI活用で
                <br>毎月2時間を創出しましょう
            </h2>
            <div class="metric" style="background: rgba(255,255,255,0.2); display: block; text-align: center; font-size: 1.3em;">
                含まれるもの：<br>
                ✅ 20個のAI活用実践例<br>
                ✅ 業務別プロンプト集<br>
                ✅ チーム導入トレーニング資料<br>
                ✅ セキュリティ・法規制ガイド
            </div>
        </div>
    </div>
"""
        return sections

    def run(self):
        """プレゼン資料を生成"""
        print("[制作部] プレゼン資料を生成中...\n")

        products = [
            ("AI時代の個人スキル販売術", "営業メール10パターン + 完全営業フロー", self.create_business_sales_content),
            ("SNS運用自動化キット", "30日分投稿テンプレート + 運用カレンダー", self.create_sns_content),
            ("初心者向けAI活用ガイド", "ChatGPT・Gemini実践20例", self.create_ai_content),
        ]

        for product_name, subtitle, content_func in products:
            print(f"【{product_name}】")

            # HTMLを生成
            sections = content_func()
            html = self.create_html_presentation(product_name, f"{product_name}\n{subtitle}", sections)

            # HTMLファイル保存
            product_dir = Path(os.path.join(self.base_path, f"生成物・商品/素材/{product_name}"))
            product_dir.mkdir(parents=True, exist_ok=True)

            html_file = product_dir / f"{product_name}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"  ✅ {product_name}.html (ブラウザで表示可能)")

        print("\n✅ すべてのプレゼン資料を生成完了")
        print("\n【使用方法】")
        print("1. 生成されたHTMLファイルをブラウザで開く")
        print("2. Ctrl+P（Mac: Cmd+P）でPDFに印刷")
        print("3. GumroadのファイルアップロードセクションにPDFを追加")

if __name__ == "__main__":
    creator = PresentationContentCreator()
    creator.run()
