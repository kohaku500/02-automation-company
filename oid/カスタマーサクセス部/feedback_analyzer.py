#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
カスタマーサクセス部: アンケート収集・分析
購入者の満足度を数値化し、課題を経営企画部へフィードバック
"""

import json
from datetime import datetime

class FeedbackAnalyzer:
    """フィードバック分析エンジン"""

    def __init__(self):
        self.feedback_data = []
        self.satisfaction_score = 0.0

    def collect_feedback(self, survey_responses):
        """アンケート回答を収集"""
        for response in survey_responses:
            self.feedback_data.append({
                "timestamp": datetime.now().isoformat(),
                "content": response["content"],
                "satisfaction": response.get("satisfaction", 5),
                "pain_points": response.get("pain_points", [])
            })

    def analyze_satisfaction(self):
        """満足度を数値化"""
        if not self.feedback_data:
            return 0.0

        total = sum(f["satisfaction"] for f in self.feedback_data)
        self.satisfaction_score = total / len(self.feedback_data)
        return self.satisfaction_score

    def extract_issues(self):
        """課題を抽出（購入者の「不平・不満」）"""
        all_pain_points = []
        for feedback in self.feedback_data:
            all_pain_points.extend(feedback.get("pain_points", []))

        # 頻出順に集計
        issue_counts = {}
        for issue in all_pain_points:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

        return sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)

    def generate_feedback_report(self):
        """経営企画部へのフィードバック報告書を生成"""
        satisfaction = self.analyze_satisfaction()
        issues = self.extract_issues()

        report = {
            "generated_at": datetime.now().isoformat(),
            "satisfaction_score": satisfaction,
            "satisfaction_level": self._level_from_score(satisfaction),
            "top_issues": [issue[0] for issue in issues[:5]],
            "recommendations": [
                {
                    "issue": issue[0],
                    "frequency": issue[1],
                    "suggested_improvement": f"次期版で『{issue[0]}』を解決する機能を追加"
                }
                for issue in issues[:3]
            ]
        }

        return report

    def _level_from_score(self, score):
        """スコアから満足度レベルを判定"""
        if score >= 4.5:
            return "excellent"
        elif score >= 4.0:
            return "good"
        elif score >= 3.0:
            return "fair"
        else:
            return "needs_improvement"

    def run(self, survey_responses=None):
        """フィードバック分析プロセス実行"""
        print("[カスタマーサクセス部] フィードバック分析開始...")

        if survey_responses:
            self.collect_feedback(survey_responses)

        report = self.generate_feedback_report()

        # 報告書を保存
        with open("feedback_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"✓ 満足度スコア: {report['satisfaction_score']:.2f}")
        print(f"✓ 解決すべき課題: {', '.join([r['issue'] for r in report['recommendations']])}")

        return report

if __name__ == "__main__":
    analyzer = FeedbackAnalyzer()
    analyzer.run()
