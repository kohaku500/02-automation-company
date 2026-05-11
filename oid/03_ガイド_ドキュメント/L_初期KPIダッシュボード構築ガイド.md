# L. 初期 KPI ダッシュボード構築ガイド

**制作日**: 2026-05-03  
**概要**: Google Sheets を使った日次・週次・月次 KPI ダッシュボード（リアルタイム追跡）の構築手順。営業進捗の自動集計、グラフ化、アラート設定までの全フロー。

---

## 目次

1. KPI 定義（日次 / 週次 / 月次）
2. Google Sheets ダッシュボーム基本設定
3. 自動集計式（QUERY / SUMIF / COUNTIF）の実装
4. グラフ・ビジュアライゼーション
5. Slack 自動通知設定
6. 日々のメンテナンス手順

---

## L-1. KPI 定義（3 階層）

### 日次 KPI

| KPI 名 | 定義 | 測定方法 | 目標値 |
|---|---|---|---|
| **営業メール送信数** | 本日送信した営業メールの合計 | "Sent-Log" sheet 行数カウント | 20-30 通 |
| **メール返信数** | 本日受け取った返信メール数 | Gmail "Agent-Inbox" ラベル新着件数 | 2-5 通 (返信率 10-15%) |
| **返信率** | 送信数に対する返信の比率 | 返信数 ÷ 送信数 × 100 | 10-15% |
| **AI Agent 処理成功数** | Agent 1-3 が正常に処理した件数 | "Agent-Log" sheet の "Success" 行数 | 100% (エラー 0) |
| **CRM 新規登録数** | 本日 CRM に新規登録された顧客数 | "CRM-Master" sheet の新規行 | 5-10 社 |
| **高優先度返信数** | 返信内容が "関心度: 高" の件数 | Agent 1 の判定スコア集計 | 0-2 通 |
| **システムエラー数** | 本日発生した処理エラー | "Error-Log" sheet の行数 | **0 件** (リスク) |

### 週次 KPI

| KPI 名 | 定義 | 測定方法 | 目標値 |
|---|---|---|---|
| **累計営業メール送信数** | 週計の送信メール合計 | 日次営業メール送信数の合計 | 150-200 通 |
| **累計返信数** | 週計の返信メール合計 | 日次返信数の合計 | 15-30 通 |
| **週次返信率** | 週計送信に対する返信比率 | 累計返信数 ÷ 累計送信数 × 100 | 10-15% ↑ |
| **CRM 新規登録累計** | 週計の新規顧客登録数 | "CRM-Master" sheet 週別集計 | 40-70 社 |
| **A/B テスト勝者** | より高い返信率のテンプレート | パターン A 返信率 vs B 返信率 | A or B 判定 |
| **リスク発生数** | 週内に発生したリスクイベント | "Risk-Log" sheet 行数 | **0 件** (理想) |

### 月次 KPI

| KPI 名 | 定義 | 測定方法 | 目標値 |
|---|---|---|---|
| **月次営業メール送信数** | 月計の送信メール合計 | 週次営業メール送信数の合計 | 600-800 通 |
| **月次返信数** | 月計の返信メール合計 | 週次返信数の合計 | 60-120 通 |
| **月次返信率** | 月計送信に対する返信比率 | 月次返信数 ÷ 月次送信数 × 100 | 10-15% |
| **月次成約数** | 実績ベースの成約件数 | "CRM-Master" の "成約" ステータス | 1-5 件 |
| **月次売上** | 成約ベースの売上（見込み値） | 成約数 × 平均単価 | ¥10万～¥100万 |
| **テンプレート改善回数** | その月内にリリースした改善テンプレート | "Template-Version" sheet 版番号 | 3-5 回 |
| **顧客満足度スコア** | 顧客フィードバック平均値（1-10） | "Feedback-Log" の平均スコア | 7.0 以上 |

---

## L-2. Google Sheets ダッシュボード基本設定

### ステップ 1: Master Sheet 作成（基礎データ）

**Sheet 名**: "KPI-Raw-Data"（全システムがここに記録）

#### Column 定義

```
A: 日付 (YYYY-MM-DD)
B: 曜日 (Monday, Tuesday, ...)
C: 営業メール送信数
D: メール返信数
E: 返信率 (%)
F: AI Agent 処理成功数
G: AI Agent エラー数
H: CRM 新規登録数
I: 高優先度返信数
J: 備考
```

#### サンプルデータ（Day 1-5）

```
2026-06-01,Sunday,50,5,10%,50,0,5,1,"初日営業メール第1陣"
2026-06-02,Monday,50,8,16%,50,0,8,2,"テンプレートv2テスト開始"
2026-06-03,Tuesday,50,12,24%,48,2,10,3,"返信率上向き傾向"
2026-06-04,Wednesday,60,18,30%,60,0,15,4,"新施策テスト開始"
2026-06-05,Thursday,0,8,N/A,0,0,0,0,"Week1振返り日（営業停止）"
```

---

### ステップ 2: サマリーシート作成（日次・週次・月次集計）

**Sheet 名**: "KPI-Summary"

#### 日次サマリー（左列）

```
セクション: Today's KPI
─────────────────────────────
送信メール数:        =FILTER(Raw!C:C, Raw!A:A = TODAY())
返信メール数:        =FILTER(Raw!D:D, Raw!A:A = TODAY())
返信率:              =IFERROR(返信数/送信数*100, 0)
CRM新規登録:         =FILTER(Raw!H:H, Raw!A:A = TODAY())
Agent エラー:        =FILTER(Raw!G:G, Raw!A:A = TODAY())
ステータス:          =IF(返信率 >= 10%, "✓ On Target", "✗ Below Target")
```

#### 週次サマリー（中列）

```
セクション: This Week's KPI
─────────────────────────────
送信メール計:        =SUMIFS(Raw!C:C, Raw!A:A, ">="&WEEKDAY(TODAY(),-1)-6, Raw!A:A, "<="&TODAY())
返信メール計:        =SUMIFS(Raw!D:D, Raw!A:A, ">="&WEEKDAY(TODAY(),-1)-6, Raw!A:A, "<="&TODAY())
週次返信率:          =IFERROR(週計返信数/週計送信数*100, 0)
CRM登録累計:         =SUMIFS(Raw!H:H, Raw!A:A, ">="&DATE(2026,6,1))
テンプレート版:      =MAX(Template!B:B)
A/B テスト勝者:      =IF(PatternA_Rate > PatternB_Rate, "Pattern A", "Pattern B")
```

#### 月次サマリー（右列）

```
セクション: This Month's KPI (June)
─────────────────────────────────────
送信メール計:        =SUMIFS(Raw!C:C, Raw!A:A, ">="&DATE(2026,6,1), Raw!A:A, "<="&DATE(2026,6,30))
返信メール計:        =SUMIFS(Raw!D:D, Raw!A:A, ">="&DATE(2026,6,1), Raw!A:A, "<="&DATE(2026,6,30))
月次返信率:          =IFERROR(月計返信数/月計送信数*100, 0)
成約件数（見込み）: =COUNTIF(CRM!G:G, "成約")
売上（見込み値）:   =成約件数 * ¥50,000
```

---

### ステップ 3: トレンドシート作成（日別推移）

**Sheet 名**: "KPI-Trends"

#### Column 定義

```
A: 日付
B: 送信数
C: 返信数
D: 返信率 (%)
E: CRM登録累計
F: Agent エラー数
G: 7日移動平均（返信率）
```

#### 式の例（7日移動平均）

```
G2: =IFERROR(AVERAGE(D1:D7), 0)
G3: =IFERROR(AVERAGE(D2:D8), 0)
```

---

## L-3. 自動集計式の実装

### 日次データの自動投入

**Google Apps Script（毎日 23:59 実行）**

```javascript
function logDailyKPI() {
  // 1. Google Sheets "KPI-Raw-Data" のアクティブシートを取得
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("KPI-Raw-Data");
  
  // 2. 本日の KPI を計算
  const sentCount = getMailSentCount(new Date());
  const replyCount = getMailReplyCount(new Date());
  const replyRate = (replyCount / sentCount * 100).toFixed(2);
  const agentSuccess = getAgentSuccessCount(new Date());
  const agentError = getAgentErrorCount(new Date());
  const crmNewCount = getCRMNewCount(new Date());
  
  // 3. 新規行を追加
  sheet.appendRow([
    Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd"),
    Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "EEEE"),
    sentCount,
    replyCount,
    replyRate,
    agentSuccess,
    agentError,
    crmNewCount,
    0, // 高優先度は手動入力
    ""  // 備考
  ]);
  
  // 4. 本日のアラート確認
  checkDailyAlert(replyRate, agentError);
}

function checkDailyAlert(replyRate, agentError) {
  // リスク判定: エラーが 3 件以上なら Slack 通知
  if (agentError >= 3) {
    const webhook = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL";
    const payload = {
      text: "⚠️ Agent エラーが " + agentError + " 件発生しました。確認してください。"
    };
    // Slack への POST リクエスト...
  }
}
```

---

## L-4. グラフ・ビジュアライゼーション

### グラフ 1: 日次返信率推移（折れ線グラフ）

**データ範囲**: KPI-Trends!A:D（日付、返信数、返信率）

**設定**:
- X 軸: 日付
- Y 軸: 返信率 (%)
- 目標ラインを引く: y = 10% （基準値）
- トレンドライン: 7 日移動平均

**挿入手順**:
1. KPI-Trends シートを開く
2. A:D を選択（日付～返信率列）
3. メニュー → 挿入 → グラフ
4. グラフタイプ: 折れ線グラフ
5. グラフエディタで目標ラインを追加（y = 10）

### グラフ 2: 営業メール送信 vs 返信（積み上げ棒グラフ）

**データ範囲**: KPI-Trends!A, B, C（日付、送信数、返信数）

**設定**:
- X 軸: 日付
- Y 軸: メール数（左軸）
- 送信数: 青色
- 返信数: 緑色（積み上げ）

### グラフ 3: CRM 登録数累計（面積グラフ）

**データ範囲**: KPI-Trends!A:E（日付、CRM登録累計）

**設定**:
- X 軸: 日付
- Y 軸: 累計登録数
- 目標ラインを引く: y = 70 社（月末目標）

### グラフ 4: A/B テスト結果（円グラフ）

**データ範囲**: Template!返信率 別集計

**設定**:
- Pattern A の返信率: ○%
- Pattern B の返信率: ○%
- 勝者を大きくハイライト

---

## L-5. Slack 自動通知設定

### 設定 1: 日次レポート（毎日 08:00）

**Slack ウェブフック設定**:

```javascript
function sendDailyKPIToSlack() {
  const yesterday = new Date(new Date().setDate(new Date().getDate() - 1));
  
  // 昨日の KPI 取得
  const sent = getSentCountByDate(yesterday);
  const replied = getReplyCountByDate(yesterday);
  const rate = (replied / sent * 100).toFixed(1);
  
  const message = {
    "text": "📊 昨日の営業 KPI レポート",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*昨日（" + Utilities.formatDate(yesterday, Session.getScriptTimeZone(), "MM/dd") + "）の成績*\n\n" +
                  "📤 送信: " + sent + "通\n" +
                  "📩 返信: " + replied + "通\n" +
                  "📈 返信率: *" + rate + "%* " + (rate >= 10 ? "✓" : "✗") + "\n" +
                  "🔧 エラー: 0 件\n" +
                  "💼 CRM 登録: " + getCRMCountByDate(yesterday) + "社"
        }
      }
    ]
  };
  
  // Slack に POST
  postToSlack(message);
}
```

### 設定 2: リスクアラート（エラー 3 件以上で即時通知）

```javascript
function sendErrorAlertToSlack(errorCount) {
  if (errorCount >= 3) {
    const message = {
      "text": "🚨 Agent エラーアラート",
      "blocks": [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "*エラーが " + errorCount + " 件発生しました*\n詳細は KPI ダッシュボードを確認してください。\nError-Log シートを確認し、即座に対応してください。"
          }
        }
      ]
    };
    postToSlack(message);
  }
}
```

---

## L-6. 日々のメンテナンス手順

### 朝の確認（06:00）

- [ ] Google Sheets "KPI-Summary" を開く
- [ ] "Today's KPI" セクションを確認
- [ ] 前日の返信率が目標以上か確認（10% 以上か）
- [ ] エラーが 0 件か確認
- [ ] Slack の朝礼レポートをスクリーンショット（記録用）

### 昼の確認（12:00）

- [ ] "KPI-Trends" グラフを開く
- [ ] 本日の返信数が目標ペース（2-3 通以上）にあるか確認
- [ ] CRM 登録が進んでいるか確認
- [ ] Agent 処理にエラーがないか確認

### 夜の確認（18:00）

- [ ] 本日の KPI を "KPI-Raw-Data" に手動入力（自動化前）
- [ ] 返信メールの内容を確認し、"高優先度" フラグを付与
- [ ] テンプレート改善が必要か判断（返信メールの傾向から）

### 週末の確認（金曜 19:00）

- [ ] "KPI-Summary" の "This Week's KPI" を確認
- [ ] 週次返信率が 10% 以上か確認
- [ ] A/B テスト結果を比較し、勝者テンプレートを確定
- [ ] 来週の営業メール送信予定を確認

### 月末の確認（月末 23:00）

- [ ] "KPI-Summary" の "This Month's KPI" を確認
- [ ] 月次返信率 / CRM 登録数 / 売上予想を最終確定
- [ ] 6 つの月次 KPI すべてが目標以上か確認
- [ ] 来月への改善施策を整理

---

## L-7. ダッシュボード完成版の構成

### 最終的なシート構成（推奨）

```
Workbook: "KPI-Master"
├─ Sheet 1: KPI-Summary（メインダッシュボード）← 毎日確認
├─ Sheet 2: KPI-Raw-Data（生データ保管）← 自動投入
├─ Sheet 3: KPI-Trends（グラフ用データ）← 自動更新
├─ Sheet 4: Template-Version（テンプレート管理）
├─ Sheet 5: Error-Log（エラー記録）
└─ Sheet 6: Feedback-Log（顧客フィードバック）
```

### 各シートのリンク

**KPI-Summary の上部に以下のリンクを配置**:

```
[📊 詳細データを見る] → KPI-Raw-Data
[📈 トレンドグラフ] → KPI-Trends
[⚠️ エラーログ] → Error-Log
[🎯 テンプレート版管理] → Template-Version
```

---

## 補足: API 自動化（Google Apps Script）

**実装時間**: 60-90 分

**自動化できる項目**:
1. 日次 KPI の自動計算（毎日 23:59）
2. Slack への日次レポート配信（毎朝 08:00）
3. 週次サマリーメール送信（毎週金曜 17:00）
4. 月次レポート PDF 作成（毎月末 23:00）
5. エラーアラート自動通知（発生時即時）

**初期段階推奨**: 項目 1, 2, 5 から開始（手動入力の負担削減と重要アラート対応）

---

**制定日**: 2026-05-03  
**バージョン**: v1.0  
**次の改版予定**: Week 1 運用開始後（2026-06-07）