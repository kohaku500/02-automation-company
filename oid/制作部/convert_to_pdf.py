#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdownをプレゼン資料（PDF）に変換（Claude Design）
"""

import os
import re
from pathlib import Path

class MarkdownToPresentationDesign:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_path = base_path

    def markdown_to_html(self, md_content, product_name):
        """MarkdownをデザインされたHTMLに変換"""

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', 'Noto Sans JP', sans-serif;
            line-height: 1.8;
            color: #2c3e50;
            background: #f5f5f5;
        }}
        .page {{
            width: 210mm;
            height: 297mm;
            margin: 10mm auto;
            padding: 20mm;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            page-break-after: always;
            position: relative;
        }}
        h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin: 30mm 0 20mm 0;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10mm;
        }}
        h2 {{
            font-size: 1.8em;
            color: #667eea;
            margin: 15mm 0 10mm 0;
            border-left: 5px solid #667eea;
            padding-left: 10mm;
        }}
        h3 {{
            font-size: 1.3em;
            color: #764ba2;
            margin: 10mm 0 8mm 0;
        }}
        h4 {{
            font-size: 1.1em;
            color: #333;
            margin: 8mm 0 5mm 0;
        }}
        p {{
            margin: 8mm 0;
            font-size: 1em;
        }}
        ul, ol {{
            margin: 8mm 0 8mm 20mm;
        }}
        li {{
            margin: 4mm 0;
            font-size: 0.95em;
        }}
        .section-intro {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20mm;
            border-radius: 5px;
            margin: 15mm 0;
            font-size: 1.1em;
        }}
        .step-box {{
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 10mm;
            margin: 10mm 0;
            border-radius: 3px;
        }}
        .step-number {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3mm 8mm;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 5mm;
            font-size: 0.9em;
        }}
        .evidence {{
            background: #fff3e0;
            border-left: 5px solid #ff9800;
            padding: 10mm;
            margin: 10mm 0;
            border-radius: 3px;
        }}
        .case-study {{
            background: #e8f5e9;
            border-left: 5px solid #4caf50;
            padding: 10mm;
            margin: 10mm 0;
            border-radius: 3px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10mm 0;
            font-size: 0.9em;
        }}
        table th {{
            background: #667eea;
            color: white;
            padding: 8mm;
            text-align: left;
        }}
        table td {{
            border: 1px solid #ddd;
            padding: 8mm;
        }}
        table tr:nth-child(even) {{
            background: #f5f5f5;
        }}
        .metric {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5mm 15mm;
            border-radius: 25px;
            margin: 5mm 5mm 5mm 0;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .highlight {{
            background: #fff9e6;
            padding: 3mm 5mm;
            border-radius: 3px;
        }}
        .footer {{
            position: absolute;
            bottom: 15mm;
            right: 20mm;
            font-size: 0.8em;
            color: #999;
        }}
        .page-number {{
            position: absolute;
            bottom: 10mm;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.8em;
            color: #999;
        }}
        @media print {{
            body {{ background: white; }}
            .page {{
                margin: 0;
                box-shadow: none;
                page-break-after: always;
            }}
        }}
        code {{
            background: #f5f5f5;
            padding: 2mm 5mm;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        strong {{
            color: #667eea;
            font-weight: 600;
        }}
    </style>
</head>
<body>
"""

        # Markdownをセクションに分割
        sections = md_content.split('\n---\n')
        page_count = 0

        for section in sections:
            page_count += 1
            html += f'<div class="page" id="page{page_count}">\n'

            # Markdownを簡易的にHTMLに変換
            section = self._convert_markdown_to_html(section)

            html += section
            html += f'<div class="page-number">- {page_count} -</div>\n'
            html += '</div>\n'

        html += """
</body>
</html>
"""
        return html

    def _convert_markdown_to_html(self, text):
        """簡易的なMarkdown→HTML変換"""

        # h1
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        # h2
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        # h3
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        # h4
        text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)

        # bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

        # code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

        # テーブル変換
        text = self._convert_table(text)

        # リスト変換（複数行対応）
        lines = text.split('\n')
        html_lines = []
        in_list = False
        in_table = False

        for line in lines:
            # テーブル行をスキップ
            if line.startswith('|'):
                in_table = True
                html_lines.append(line)
                continue
            elif in_table and line.strip() == '':
                in_table = False

            if line.startswith('- '):
                if not in_list:
                    html_lines.insert(len(html_lines) - (1 if html_lines and html_lines[-1].startswith('- ') else 0), '<ul>')
                    in_list = True
                html_lines.append(f'<li>{line[2:]}</li>')
            else:
                if in_list and line.strip() != '':
                    html_lines.append('</ul>')
                    in_list = False
                if line.strip() != '':
                    html_lines.append(f'<p>{line}</p>')

        if in_list:
            html_lines.append('</ul>')

        text = '\n'.join(html_lines)

        return text

    def _convert_table(self, text):
        """テーブル変換"""
        lines = text.split('\n')
        result = []
        in_table = False
        table_lines = []

        for line in lines:
            if line.startswith('|'):
                if not in_table:
                    in_table = True
                    table_lines = [line]
                else:
                    table_lines.append(line)
            else:
                if in_table and table_lines:
                    result.append(self._build_html_table(table_lines))
                    table_lines = []
                    in_table = False
                result.append(line)

        if table_lines:
            result.append(self._build_html_table(table_lines))

        return '\n'.join(result)

    def _build_html_table(self, lines):
        """HTMLテーブルを生成"""
        if len(lines) < 2:
            return '\n'.join(lines)

        html = '<table>\n'

        # ヘッダー行
        header = lines[0].split('|')[1:-1]
        html += '<tr>\n'
        for cell in header:
            html += f'<th>{cell.strip()}</th>\n'
        html += '</tr>\n'

        # データ行
        for line in lines[2:]:
            if line.strip().startswith('|'):
                cells = line.split('|')[1:-1]
                html += '<tr>\n'
                for cell in cells:
                    html += f'<td>{cell.strip()}</td>\n'
                html += '</tr>\n'

        html += '</table>'
        return html

    def run(self):
        """実行"""
        print("[Claude Design] プレゼン資料（HTML）を生成中...\n")

        products = [
            "AI時代の個人スキル販売術",
            "SNS運用自動化キット",
            "初心者向けAI活用ガイド"
        ]

        for product_name in products:
            print(f"【{product_name}】")

            product_dir = Path(os.path.join(self.base_path, f"生成物・商品/素材/{product_name}"))
            md_file = product_dir / f"{product_name}_実行手順書.md"

            if not md_file.exists():
                print(f"  ❌ ファイルが見つかりません: {md_file}")
                continue

            # Markdownを読み込み
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # HTMLに変換
            html = self.markdown_to_html(md_content, product_name)

            # HTMLファイルを保存
            html_file = product_dir / f"{product_name}_プレゼン資料.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"  ✅ {product_name}_プレゼン資料.html")
            print(f"     （ブラウザで開いて Ctrl+P で PDF化）")

        print("\n✅ すべてのプレゼン資料生成完了")
        print("\n【次のステップ】")
        print("1. HTMLファイルをブラウザで開く")
        print("2. Ctrl+P (Mac: Cmd+P) でPDF保存")
        print("3. 品質チェック機構で競合分析")
        print("4. Gumroadにアップロード")

if __name__ == "__main__":
    converter = MarkdownToPresentationDesign()
    converter.run()
