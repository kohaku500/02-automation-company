# Google Sheets セットアップ完全ガイド

**実施日**: 2026-05-04  
**所要時間**: 約 30 分  
**目標**: Day 1 に必要な全 Google Sheets テンプレートを準備完了

---

## 📋 作成すべき Google Sheets 一覧

| # | Sheet 名 | 用途 | 優先度 | 作成順序 |
|---|---------|------|--------|---------|
| 1 | KPI-Raw-Data | 日次データ収集（営業メール、返信など） | 🔴 高 | **1番目** |
| 2 | KPI-Summary | KPI 自動集計（日次・週次・月次） | 🔴 高 | 2番目 |
| 3 | CRM-Master | 顧客管理（企業名、メール、ステータス） | 🔴 高 | 3番目 |
| 4 | Agent-Log | Agent 処理ログ | 🟠 中 | 4番目 |
| 5 | Agent-Templates | 自動応答テンプレート管理 | 🟠 中 | 5番目 |
| 6 | Sent-Log | 送信メール記録 | 🟠 中 | 6番目 |
| 7 | Lead-Extraction-Log | リード情報抽出ログ | 🟡 低 | 7番目 |
| 8 | Conversation-Summary | 顧客対応サマリー | 🟡 低 | 8番目 |
| 9 | Error-Log | エラーログ | 🟡 低 | 9番目 |

---

## 🛠️ セットアップ手順

### **Step 0: Google Drive フォルダ準備**

1. Google Drive を開く
2. 新規フォルダ作成: `収益会社_AI_System`
3. このフォルダ内に以下のスプレッドシートを全て作成する

---

### **Step 1: KPI-Raw-Data（日次データ収集）**

**URL**: https://sheets.google.com/create

1. **新規スプレッドシート作成**: 名前は `KPI-Raw-Data`
2. **Sheet1 を削除**して、新規 Sheet を作成: 名前は `Daily-Metrics`

**Column 定義**:

```
A列: 日付 (YYYY-MM-DD)
     └ 例: 2026-06-01

B列: 曜日 (自動計算)
     └ =TEXT(A2,"dddd")

C列: 営業メール送信数
     └ Day 1 目標: 50-100

D列: メール返信数
     └ Day 1 目標: 5-15

E列: 返信率 (%)
     └ =IF(C2=0, 0, D2/C2*100)

F列: AI Agent 処理成功数
     └ Agent-Log から自動集計

G列: AI Agent エラー数
     └ Error-Log から自動集計

H列: CRM 新規登録数
     └ CRM-Master から新規行数をカウント

I列: 高優先度返信数（関心度: 高）
     └ Agent-Log から関心度: 高をカウント

J列: 備考
     └ 手動記入欄
```

**サンプルデータ（Day 1-5 想定値）**:

```
2026-06-01 | Sunday | 50 | 5 | 10% | 50 | 0 | 5 | 1 | 初日営業メール第1陣
2026-06-02 | Monday | 50 | 8 | 16% | 50 | 0 | 8 | 2 | テンプレートv2テスト開始
2026-06-03 | Tuesday | 50 | 12 | 24% | 48 | 2 | 10 | 3 | 返信率上向き傾向
2026-06-04 | Wednesday | 60 | 18 | 30% | 60 | 0 | 15 | 4 | 新施策テスト開始
2026-06-05 | Thursday | 0 | 8 | N/A | 0 | 0 | 0 | 0 | Week1振返り日
```

---

### **Step 2: CRM-Master（顧客管理）**

**新規スプレッドシート作成**: 名前は `CRM-Master`

**Column 定義**:

```
A列: 顧客ID（自動採番）
B列: 企業名
C列: 代表メール
D列: 従業員数
E列: 電話番号
F列: 部門
G列: ステータス (新規 / 検討中 / 提案待ち / 成約)
H列: 関心度 (高 / 中 / 低)
I列: 初回接触日
J列: 最終更新日
K列: 主なニーズ
L列: 副次ニーズ
M列: 抽出スコア
```

**サンプルデータ**:

```
1 | (株)A | contact@a.co.jp | 50 | 090-1234-5678 | 開発部 | 新規 | 高 | 2026-06-01 | 2026-06-01 | 自動化 | 効率化 | 5
2 | (株)B | info@b.co.jp | 100 | 090-9876-5432 | 営業部 | 検討中 | 中 | 2026-06-01 | 2026-06-02 | コスト削減 | デジタル化 | 4
```

---

### **Step 3: Agent-Log（Agent 処理ログ）**

**新規スプレッドシート作成**: 名前は `Agent-Log`

**Column 定義**:

```
A列: タイムスタンプ
B列: 件名
C列: 送信者メール
D列: 関心度（高/中/低）
E列: 対応状況（応答済み/未対応/エラー）
F列: 企業名
G列: 従業員数
H列: 電話番号
I列: 部門
```

**サンプル**: 手動で埋めず、Google Apps Script の実行により自動記入されます

---

### **Step 4: Agent-Templates（テンプレート管理）**

**新規スプレッドシート作成**: 名前は `Agent-Templates`

**Column 定義**:

```
A列: パターン識別キーワード
B列: 判定ステータス（関心度: 高/中/低）
C列: 自動応答テンプレート本文
D列: 先行フォローアップ日
E列: テンプレートバージョン
F列: 更新日
```

**初期データ**:

```
具体的な質問・ユースケース | 関心度: 高 | [H参照] | 3日後 | 1.0 | 2026-05-03
簡潔な問い合わせ | 関心度: 中 | [H参照] | 1日後 | 1.0 | 2026-05-03
自動返信・情報請求のみ | 関心度: 低 | [H参照] | 5日後 | 1.0 | 2026-05-03
```

> **H 参照**: [H_初期営業メールv1.0.md](./H_初期営業メールv1.0.md) のテンプレートから引用

---

### **Step 5: Sent-Log（送信メール記録）**

**新規スプレッドシート作成**: 名前は `Sent-Log`

**Column 定義**:

```
A列: 送信日時
B列: パターン（A/B）
C列: 相手企業
D列: 相手メール
E列: 件名
F列: 送信完了
G列: 開封日時
H列: 開封済み
I列: 返信日時
J列: 返信済み
K列: 返信内容サマリー
L列: 次アクション
```

---

### **Step 6: KPI-Summary（自動集計シート）**

**新規スプレッドシート作成**: 名前は `KPI-Summary`

**複数 Sheet を作成**:
1. `Daily-Summary`（日次 KPI）
2. `Weekly-Summary`（週次 KPI）
3. `Monthly-Summary`（月次 KPI）

#### **Daily-Summary（日次 KPI）**

```
【Today's KPI】
─────────────────────────

本日の日付: =TODAY()

🔵 営業メール送信数:
   =SUMIF('KPI-Raw-Data'!A:A, TODAY(), 'KPI-Raw-Data'!C:C)
   目標: 20-30通

🔵 メール返信数:
   =SUMIF('KPI-Raw-Data'!A:A, TODAY(), 'KPI-Raw-Data'!D:D)
   目標: 2-5通（返信率 10-15%）

🔵 返信率:
   =IF(C5=0, 0, C6/C5*100)&"%"

🟢 AI Agent 処理成功数:
   =COUNTIF('Agent-Log'!E:E, "応答済み")
   目標: エラー 0件

🔴 AI Agent エラー数:
   =COUNTIF('Error-Log'!A:A, TODAY())
   リスク: エラー発生時は即対応

🟡 CRM 新規登録数:
   =COUNTIF('CRM-Master'!I:I, TODAY())
   目標: 5-10社

🟣 高優先度返信数:
   =COUNTIF('Agent-Log'!D:D, "高")
   目標: 0-2通
```

#### **Weekly-Summary（週次 KPI）**

```
【This Week's KPI】
─────────────────────────

週の開始日: =(TODAY() - WEEKDAY(TODAY()) + 2)

📊 週計営業メール送信数:
   =SUMIFS('KPI-Raw-Data'!C:C,
           'KPI-Raw-Data'!A:A, ">=" & (TODAY()-6),
           'KPI-Raw-Data'!A:A, "<=" & TODAY())
   目標: 150-200通

📊 週計返信数:
   =SUMIFS('KPI-Raw-Data'!D:D,
           'KPI-Raw-Data'!A:A, ">=" & (TODAY()-6),
           'KPI-Raw-Data'!A:A, "<=" & TODAY())
   目標: 15-30通

📊 週次返信率:
   =IF(B4=0, 0, B5/B4*100)&"%"
   目標: 10-15% ↑

📊 A/B テスト勝者:
   =IF(COUNTIF('Sent-Log'!B:B, "A") > COUNTIF('Sent-Log'!B:B, "B"), "Pattern A", "Pattern B")
```

#### **Monthly-Summary（月次 KPI）**

```
【This Month's KPI】
─────────────────────────

月次営業メール送信数:
   =SUMIFS('KPI-Raw-Data'!C:C,
           'KPI-Raw-Data'!A:A, ">=" & DATE(YEAR(TODAY()), MONTH(TODAY()), 1),
           'KPI-Raw-Data'!A:A, "<" & DATE(YEAR(TODAY()), MONTH(TODAY())+1, 1))
   目標: 600-800通

月次返信数:
   [同様に SUMIFS で計算]
   目標: 60-120通

月次返信率: 10-15%

月次成約数:
   =COUNTIF('CRM-Master'!G:G, "成約")
   目標: 1-5件

月次売上（見込み値）:
   =COUNTA(成約件数) * 50000  (仮: 平均単価¥50K)
   目標: ¥10万～¥100万
```

---

### **Step 7: その他のログシート（自動生成）**

以下は Google Apps Script の実行により自動作成されるため、手動での準備は不要:

- ✅ **Lead-Extraction-Log**: Agent 2 が作成
- ✅ **Conversation-Summary**: Agent 3 が作成
- ✅ **Error-Log**: エラー発生時に作成
- ✅ **応答済み ラベル**: 対応メールを管理

---

## 📌 Google Apps Script との連携

### セットアップ手順

1. **Google Apps Script エディタを開く**
   - https://script.google.com

2. **新規プロジェクト作成**: 「Gmail 自動応答ボット v1.0」

3. **各ファイルをコピペ**:
   - `GAS_Agent1_完全実装コード.gs`
   - `GAS_Agent2_リード情報抽出.gs`
   - `GAS_Agent3_顧客対応サマリー.gs`

4. **環境変数を設定** (Properties Service):
   ```javascript
   // Project Properties に設定
   SPREADSHEET_ID: "KPI-Raw-Data のスプレッドシート ID"
   SLACK_WEBHOOK_URL: "https://hooks.slack.com/services/..."
   ```

5. **トリガー設定**:
   - **トリガー** → 新規トリガー
   - 関数: `checkAndReplyToEmails`
   - イベントソース: 時間主導型
   - 時間ベース: **1時間ごと**
   - エラー通知: メールで通知

---

## ✅ Day 1 実装チェックリスト

```
[ ] KPI-Raw-Data 作成（Daily-Metrics）
[ ] CRM-Master 作成
[ ] Agent-Log 作成
[ ] Agent-Templates 作成
[ ] Sent-Log 作成
[ ] KPI-Summary 作成（3つの Sub-Sheet）
[ ] Google Apps Script プロジェクト作成
[ ] 各 Agent コードを Google Apps Script にコピペ
[ ] 環境変数（SPREADSHEET_ID, SLACK_WEBHOOK_URL）設定
[ ] トリガー設定（1時間ごと実行）
[ ] テスト実行（Gmail にテストメール送信）
[ ] Gmail ラベル "Agent-Inbox" 確認
```

---

## 📞 トラブルシューティング

### Q: Google Apps Script でエラーが出る

**A**: 
- `SPREADSHEET_ID` が正しく設定されているか確認
- `GmailApp.getUserLabelByName()` で "Agent-Inbox" が見つからない場合、手動で作成してください

### Q: 自動応答メールが送られない

**A**:
- Gmail で "Agent-Inbox" ラベルが作成されているか確認
- テストメールを送信して、ラベルが自動付与されるか確認
- Google Apps Script のトリガーが実行されているか確認（実行履歴を確認）

### Q: 返信メール が "Agent-Inbox" に入らない

**A**:
- Gmail 設定 → フィルタを確認
- テンプレート営業メール の From アドレスを確認（返信が正しく返ってくるアドレスか）

---

**完了後**: Day 1（2026-06-01）の営業メール送信テストを開始してください。
