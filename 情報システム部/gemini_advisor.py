#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude-Gemini 連携アドバイザー
システム運用中の判断が必要な質問を Gemini に投げ、3つの解決案を導出
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Tuple

try:
    from google import genai
except ImportError:
    print("⚠️ google-genai をインストールしてください: pip install google-genai")
    genai = None


class GeminiAdvisor:
    """Gemini を利用した意思決定補助エンジン"""

    def __init__(self):
        # .env ファイルから API キーを読み込む
        from dotenv import load_dotenv
        load_dotenv('.env')

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY が設定されていません")

        if genai:
            self.client = genai.Client(api_key=api_key)
            self.model = "gemini-2.5-flash"  # 最新モデルを使用
        else:
            self.client = None
            self.model = None
            print("⚠️ Gemini モデルが利用できません")

        self.advice_log = {
            "timestamp": datetime.now().isoformat(),
            "advices": []
        }

    def ask_for_advice(self, question: str, context: str = "") -> Dict:
        """
        Gemini に質問を投げて、3つの解決案を取得

        Args:
            question: 質問内容
            context: 背景情報（オプション）

        Returns:
            {
                "question": str,
                "context": str,
                "options": [...],
                "recommendation": "案B",
                "rationale": "理由...",
                "timestamp": str
            }
        """

        if not self.client:
            return self._fallback_response(question, context)

        prompt = self._build_prompt(question, context)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            advice = self._parse_response(question, context, response.text)
            self.advice_log["advices"].append(advice)
            return advice

        except Exception as e:
            print(f"❌ Gemini API エラー: {e}")
            return self._error_response(question, context, str(e))

    def _build_prompt(self, question: str, context: str) -> str:
        """Gemini 用のプロンプトを構築"""

        base_prompt = f"""
あなたは AI 収益化システムの意思決定補助アドバイザーです。
システム運用中の質問に対して、3つの異なるアプローチを提案してください。

【質問】
{question}

【背景情報】
{context if context else "なし"}

【回答フォーマット】
以下の形式で、A案・B案・C案を提案してください：

## 案A: [タイトル]
- 説明: [内容]
- メリット: [複数行]
- デメリット: [複数行]
- リスク度: 低/中/高

## 案B: [タイトル]
- 説明: [内容]
- メリット: [複数行]
- デメリット: [複数行]
- リスク度: 低/中/高

## 案C: [タイトル]
- 説明: [内容]
- メリット: [複数行]
- デメリット: [複数行]
- リスク度: 低/中/高

## 推奨案
[A/B/C のいずれか] を推奨します。理由：[具体的な理由]

---

重要な注意事項：
- 3つの案は本当に異なるアプローチである必要があります
- 推奨案を必ず1つ選定してください
- 理由は明確で、判断基準を示してください
"""
        return base_prompt

    def _parse_response(self, question: str, context: str, response_text: str) -> Dict:
        """Gemini の回答をパースして構造化"""

        advice = {
            "question": question,
            "context": context if context else "",
            "raw_response": response_text,
            "options": [],
            "recommendation": "",
            "rationale": "",
            "timestamp": datetime.now().isoformat()
        }

        # 簡易パース（実装時にはより堅牢にする）
        lines = response_text.split('\n')
        current_option = None

        for line in lines:
            if line.startswith('## 案'):
                if current_option:
                    advice["options"].append(current_option)
                current_option = {
                    "label": line.replace('## ', '').replace(':', ''),
                    "description": "",
                    "pros": [],
                    "cons": [],
                    "risk": "不明"
                }
            elif line.startswith('## 推奨案'):
                if current_option:
                    advice["options"].append(current_option)
                current_option = None
                # 推奨案を抽出
                idx = response_text.find('## 推奨案')
                recommendation_section = response_text[idx:]
                lines_rec = recommendation_section.split('\n')
                if len(lines_rec) > 1:
                    rec_line = lines_rec[1].strip()
                    if rec_line.startswith('[') and ']' in rec_line:
                        advice["recommendation"] = rec_line.split(']')[0].replace('[', '')
                    if '理由：' in recommendation_section:
                        advice["rationale"] = recommendation_section.split('理由：')[1].split('\n')[0].strip()

        return advice

    def _fallback_response(self, question: str, context: str) -> Dict:
        """Gemini API が利用できない場合のフォールバック"""

        return {
            "question": question,
            "context": context,
            "status": "⚠️ Gemini API が利用できません",
            "message": "GEMINI_API_KEY を確認してください",
            "timestamp": datetime.now().isoformat()
        }

    def _error_response(self, question: str, context: str, error: str) -> Dict:
        """エラー時の応答"""

        return {
            "question": question,
            "context": context,
            "status": "❌ エラー",
            "error": error,
            "timestamp": datetime.now().isoformat()
        }

    def save_advice_log(self, filepath: str = "../運営ログ/gemini_advice_log.json"):
        """アドバイスログを保存"""

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.advice_log, f, ensure_ascii=False, indent=2)

        print(f"✅ アドバイスログを保存: {filepath}")


# テスト用
if __name__ == "__main__":
    import sys

    # 環境変数を読み込み
    from dotenv import load_dotenv
    load_dotenv()

    advisor = GeminiAdvisor()

    # テスト質問
    test_question = "6月のMRR達成が難しい場合、どのように対応すべきですか？"
    test_context = "現在の目標は¥50,000。市場調査で競合商品の価格帯が見えてきた。"

    print("[Gemini アドバイザー] テスト実行中...\n")
    advice = advisor.ask_for_advice(test_question, test_context)

    print(json.dumps(advice, ensure_ascii=False, indent=2))
    advisor.save_advice_log()
