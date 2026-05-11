# Gmail AddOn システムアーキテクチャ - ツリー構造

**作成日**: 2026-05-05  
**対象製品**: AI Agent Sales Assistant (Gmail AddOn)  
**バージョン**: 1.0

---

## 📊 全体システムアーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                     Gmail AddOn システム全体像                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                       外部サービス連携層                             │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐             │
│  │  Gmail API  │  │  Claude API  │  │Google Sheets│             │
│  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘             │
└─────────┼─────────────────┼─────────────────┼──────────────────┘
          │                 │                 │
┌─────────▼─────────────────▼─────────────────▼──────────────────┐
│                   Google Apps Script 実行環境                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐     │
│  │  Main.gs       │  │  Config.gs   │  │ Dashboard.gs    │     │
│  │ (エントリーポイント) │  │(設定・定数管理)│  │(UI パネル表示)      │
│  └────┬───────────┘  └──────┬───────┘  └────────┬────────┘     │
│       │                     │                   │               │
│       └─────────────────────┼───────────────────┘               │
│                             │                                   │
│  ┌───────────────────────────▼────────────────────────┐        │
│  │             コア処理エンジン層                         │        │
│  ├────────────────────────────────────────────────────┤        │
│  │                                                    │        │
│  │  ┌──────────────────┐  ┌──────────────────┐     │        │
│  │  │ EmailHandler.gs  │  │ AIAnalyzer.gs    │     │        │
│  │  │(メール受信・検出)    │  │(購入意欲スコア判定)  │     │        │
│  │  └────────┬─────────┘  └────────┬─────────┘     │        │
│  │           │                     │                │        │
│  │  ┌────────▼─────────┐  ┌────────▼─────────┐    │        │
│  │  │StyleLearner.gs   │  │AutoResponder.gs  │    │        │
│  │  │(文体学習・適応)      │  │(自動応答生成)        │    │        │
│  │  └────────────────────┘  └────────────────────┘    │        │
│  │           │                     │                │        │
│  │           └──────────┬──────────┘                │        │
│  │                      │                          │        │
│  │  ┌──────────────────▼─────────────────┐        │        │
│  │  │  CRMLogger.gs                       │        │        │
│  │  │  (顧客情報・メール履歴ログ)            │        │        │
│  │  └──────────────────┬──────────────────┘        │        │
│  │                     │                          │        │
│  └─────────────────────┼──────────────────────────┘        │
│                        │                                    │
│  ┌─────────────────────▼──────────────────┐               │
│  │ PermissionManager.gs                    │               │
│  │ (ロールベース アクセス制御)                │               │
│  └─────────────────────┬──────────────────┘               │
│                        │                                   │
└────────────────────────┼───────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────┐
│                    データ保存層                              │
├────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────────────┐        │
│  │  Google Sheets   │  │  Gmail Labels & Folders  │        │
│  │  (CRM・設定・ログ)   │  │  (メール整理・タグ)        │        │
│  └──────────────────┘  └──────────────────────────┘        │
└────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Google Apps Script ファイル構成と依存関係

### ファイル一覧（9ファイル）

```
AI_Agent_Sales_Assistant/
│
├─ 1️⃣  Main.gs                    [エントリーポイント]
├─ 2️⃣  Config.gs                  [設定・定数・環境変数]
├─ 3️⃣  Dashboard.gs               [UI・パネル表示]
├─ 4️⃣  EmailHandler.gs            [Gmail API 連携]
├─ 5️⃣  AIAnalyzer.gs             [Claude API・購入意欲判定]
├─ 6️⃣  StyleLearner.gs           [文体学習・適応]
├─ 7️⃣  AutoResponder.gs          [自動返信生成]
├─ 8️⃣  CRMLogger.gs              [Google Sheets ログ]
└─ 9️⃣  PermissionManager.gs       [ロール・アクセス制御]
```

### 依存関係グラフ

```
┌──────────────┐
│   Main.gs    │ ← エントリーポイント（全機能初期化）
└────┬─────────┘
     │
     ├──────────────────┬──────────────────┬─────────────────┐
     │                  │                  │                 │
     ▼                  ▼                  ▼                 ▼
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────┐
│Config.gs │    │Dashboard.gs  │    │EmailHandler │    │Permission  │
│  ◀────────    │              │    │    .gs      │    │Manager.gs  │
│ 設定初期化 │    │ パネル初期化  │    │ トリガー設定 │    │  権限初期化 │
└──────────┘    └──────┬───────┘    └─────┬──────┘    └────┬───────┘
                       │                  │               │
                       │                  │               │
                       │                  ▼               │
                       │            ┌──────────────┐     │
                       │            │ onOpen()     │     │
                       │            │ onMailReceive│     │
                       │            └──────┬───────┘     │
                       │                   │             │
                       │                   ▼             │
                       │  ┌────────────────────────────┐ │
                       │  │  メール受信時の処理フロー   │ │
                       │  ├────────────────────────────┤ │
                       │  │                            │ │
                       │  │ 1. EmailHandler.gs         │ │
                       │  │    - メール取得             │ │
                       │  │    - 送信者解析             │ │
                       │  │                            │ │
                       │  │ 2. PermissionManager.gs    │ │
                       │  │    - ユーザー権限確認      │ │
                       │  │                            │ │
                       │  │ 3. AIAnalyzer.gs           │ │
                       │  │    - 購入意欲スコア計算    │ │
                       │  │    (Claude API 呼び出し)   │ │
                       │  │                            │ │
                       │  │ 4. StyleLearner.gs         │ │
                       │  │    - 過去メール分析        │ │
                       │  │    - 文体パターン学習      │ │
                       │  │                            │ │
                       │  │ 5. AutoResponder.gs        │ │
                       │  │    - 返信テキスト生成      │ │
                       │  │    (スコア <70 の場合)     │ │
                       │  │                            │ │
                       │  │ 6. CRMLogger.gs            │ │
                       │  │    - Google Sheets 記録    │ │
                       │  │    - メール履歴保存        │ │
                       │  │                            │ │
                       │  │ 7. Gmail API               │ │
                       │  │    - 転送 or 返信送信      │ │
                       │  │    - ラベル付与            │ │
                       │  │                            │ │
                       │  └────┬─────────────────────┘ │
                       │       │                       │
                       └───────┼───────────────────────┘
                               │
                               ▼
                        ┌─────────────┐
                        │Dashboard.gs │
                        │ UI 更新・表示 │
                        └─────────────┘
```

---

## 🔄 データフロー（メール受信から完了まで）

### 1. メール受信～処理フロー（詳細）

```
【Phase 1: 受信検出】
┌─────────────────────────────────────┐
│ Gmail メール受信                      │
│ (tanaka.agent@abc.com)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ EmailHandler.gs::onMailReceive()     │
│                                     │
│ - メール ID 取得                     │
│ - 送信者メール取得                    │
│ - 件名・本文取得                      │
│ - 日時記録                           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Config.gs の定数確認                 │
│ (API キー、スコア閾値、ラベル等)      │
└────────────┬────────────────────────┘
             │
             │
【Phase 2: 権限確認】
             ▼
┌─────────────────────────────────────┐
│ PermissionManager.gs::checkAccess()  │
│                                     │
│ - 受取人のロール確認                  │
│ - 閲覧権限チェック                    │
│   (管理職 → 全表示                   │
│    営業 → 個人+ Team表示)            │
└────────────┬────────────────────────┘
             │
             │
【Phase 3: AI 分析】
             ▼
┌──────────────────────────────────────┐
│ AIAnalyzer.gs::analyzeEmail()         │
│                                      │
│ Claude API へ送信：                   │
│ ┌──────────────────────────────────┐ │
│ │ Prompt:                          │ │
│ │ "このメールから購入意欲を分析し、  │ │
│ │  0-100 スコアで返してください"    │ │
│ │                                  │ │
│ │ 入力テキスト：                    │ │
│ │ - メール本文                      │ │
│ │ - 件名                           │ │
│ │ - 送信者情報（会社・役職など）    │ │
│ └──────────────────────────────────┘ │
│                                      │
│ ← Claude API からスコア返却            │
│   例: { score: 85, signals: [...] }  │
└────────────┬───────────────────────┘
             │
             │
【Phase 4: 文体学習・適応】
             ▼
┌──────────────────────────────────────┐
│ StyleLearner.gs::analyzeSenderStyle()│
│                                      │
│ Google Sheets から検索：              │
│ - この送信者の過去メール              │
│ - 文体・キーワード・口調パターン      │
│                                      │
│ ↓ 文体情報見つかった場合             │
│ StyleLearner.gs::extractPatterns()   │
│                                      │
│ - 句点の使い方                       │
│ - よく使う表現                       │
│ - 敬語 vs カジュアル度               │
│ - 段落の作り方                       │
│                                      │
│ → スタイル プロファイル生成          │
└────────────┬───────────────────────┘
             │
             │
【Phase 5: 応答判定】
             ▼
        ┌────────────────────┐
        │ スコア ≥ 70 ?      │
        └────┬───────────┬──┘
             │           │
             │ YES       │ NO
             ▼           ▼
     ┌────────────┐  ┌────────────────────┐
     │ 転送処理   │  │ 自動応答処理        │
     └────────────┘  └──────────┬─────────┘
             │                  │
             ▼                  ▼
     ┌────────────────────────────────────┐
     │ AutoResponder.gs::generateResponse()│
     │                                    │
     │ Claude API へ送信：                 │
     │ ┌──────────────────────────────┐   │
     │ │ Prompt:                      │   │
     │ │ "以下の送信者のメール返信を、  │   │
     │ │  この文体で生成してください"  │   │
     │ │                              │   │
     │ │ 文体情報: {style_profile}    │   │
     │ │ メール内容: {email_body}     │   │
     │ └──────────────────────────────┘   │
     │                                    │
     │ ← Claude から自動応答テキスト       │
     └────────────┬─────────────────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Gmail API で返信送信│
         │ (ラベル付与)       │
         └────────┬─────────┘
                  │


【Phase 6: ログ記録・UI 更新】
             ▼
┌──────────────────────────────────────┐
│ CRMLogger.gs::logToSheets()           │
│                                      │
│ Google Sheets に記録：                │
│ - メール ID、日時                     │
│ - 送信者情報                          │
│ - スコア、スコア根拠                  │
│ - 処理結果（転送/自動応答)            │
│ - 文体学習の有無                      │
└────────────┬───────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Dashboard.gs::updateUI()              │
│                                      │
│ Gmail パネルに表示：                   │
│ ✅ スコア（星評価）                    │
│ ✅ 処理結果ステータス                  │
│ ✅ 検出シグナル（購入意欲の根拠)       │
│ ✅ 推奨アクション                      │
└────────────────────────────────────┘
```

---

## 📋 各ファイルの機能仕様

### 1. **Main.gs** - エントリーポイント・初期化

| 関数 | 役割 |
|------|------|
| `onOpen()` | AddOn 起動時実行（Dashboard 初期化） |
| `onMailReceive(event)` | メール受信時トリガー（処理開始） |
| `runDailyMaintenance()` | 日次メンテナンス（キャッシュ更新） |

**フロー**:
```
onOpen() 
  ↓ Config 読み込み
  ↓ PermissionManager.checkUser()
  ↓ Dashboard.initialize()
  ↓ UI パネル描画

onMailReceive(event)
  ↓ EmailHandler.extractEmailData()
  ↓ AIAnalyzer.analyzeEmail()
  ↓ (スコア分岐)
  ↓ AutoResponder or ForwardEmail
  ↓ CRMLogger.log()
  ↓ Dashboard.updateUI()
```

---

### 2. **Config.gs** - 設定・定数・環境変数管理

| 変数 | 説明 | デフォルト |
|------|------|----------|
| `CLAUDE_API_KEY` | Claude API キー | sk-ant-xxxxx |
| `SPREADSHEET_ID` | Google Sheets ID | (インストール時設定) |
| `SCORE_THRESHOLD` | スコア分岐閾値 | 70 |
| `STYLE_LEARNING_ENABLED` | 文体学習有効化 | true |
| `AUTO_RESPONSE_ENABLED` | 自動応答有効化 | true |
| `FORWARD_TO_PERSONAL` | 個人メールに転送 | true |
| `LOG_ALL_EMAILS` | 全メールログ記録 | true |

**管理関数**:
```
getConfig()         → 全設定取得
updateSetting()     → 設定変更
validateAPIKey()    → API キー検証
getThresholdScore() → 閾値取得
```

---

### 3. **Dashboard.gs** - UI・パネル表示

| コンポーネント | 説明 |
|-------------|------|
| **サイドパネル** | メール分析結果表示 |
| **スコア表示** | 星評価（1～5） |
| **検出シグナル** | 購入意欲の根拠 |
| **アクションボタン** | 手動操作（承認・却下） |
| **ダッシュボード** | メール履歴・KPI |

**UI レイアウト（スクリーンショット）**:
```
┌────────────────────────────┐
│   Gmail AddOn Panel         │
├────────────────────────────┤
│                            │
│  From: sato@client.jp      │
│  Company: XYZ Inc.         │
│  Role: Director            │
│                            │
│  🌟 🌟 🌟 🌟 🌟 (85点)    │
│                            │
│  🎯 検出シグナル：         │
│  ✓ "導入したい" 言及       │
│  ✓ 予算確認            │
│  ✓ 実装タイムライン質問  │
│                            │
│  📋 推奨アクション：        │
│  → 転送（personal）        │
│                            │
│  [✅ 承認] [❌ 却下]      │
│                            │
└────────────────────────────┘
```

**主要関数**:
```
initialize()              → UI 初期化
updateUI()               → UI 更新
displayScore()           → スコア表示
showDetectionSignals()   → シグナル表示
showUserDashboard()      → ダッシュボード表示（ロール別）
```

---

### 4. **EmailHandler.gs** - Gmail API 連携

| 関数 | 入力 | 出力 |
|------|------|------|
| `extractEmailData()` | email event | { from, to, subject, body, timestamp } |
| `getEmailBody()` | messageId | メール本文 テキスト |
| `getSenderInfo()` | メールアドレス | { name, company, previousEmails } |
| `forwardToPersonal()` | messageId, score | 転送完了 ✓ |
| `applyLabel()` | messageId, label | ラベル付与 ✓ |

**処理フロー**:
```
onMailReceive(event)
  ↓
extractEmailData(event.message.getId())
  ├─ messageId → getEmailBody()
  ├─ from → getSenderInfo()
  ├─ subject, body 取得
  └─ return { email object }
  
score ≥ 70?
  ├─ YES → forwardToPersonal()
  │         applyLabel("High-Priority")
  └─ NO  → return to AutoResponder
```

---

### 5. **AIAnalyzer.gs** - Claude API・購入意欲判定

| 関数 | 入力 | 出力 |
|------|------|------|
| `analyzeEmail()` | { subject, body, senderInfo } | { score, signals, reasoning } |
| `callClaudeAPI()` | prompt, emailText | Claude API 応答 |
| `parseScore()` | API 応答 | score (0-100) |
| `extractSignals()` | API 応答 | signals[] |

**Claude Prompt テンプレート**:
```
"""
【タスク】以下のメールから購入意欲を分析し、JSON 形式で返してください。

【分析項目】
1. 購入意欲スコア: 0-100（0=興味なし、100=即決見込み）
2. 検出シグナル: 購入意欲を示すキーワード・表現
3. 分析理由: スコアをつけた根拠

【入力メール】
件名: {subject}
本文: {body}
送信者: {company} / {position}

【出力形式】
{
  "score": 85,
  "signals": [
    "導入したい希望が明示されている",
    "予算・スケジュール確認",
    "競合検討フェーズと推定"
  ],
  "reasoning": "複数の購入シグナルが検出され、検討段階の顧客と判定"
}
"""
```

---

### 6. **StyleLearner.gs** - 文体学習・適応

| 関数 | 入力 | 出力 |
|------|------|------|
| `analyzeSenderStyle()` | senderEmail | { wordPatterns, tone, expressions } |
| `getPastEmails()` | senderEmail | [ email1, email2, ... ] |
| `extractPatterns()` | [ pastEmails ] | { style_profile } |
| `calculateToneIndex()` | emailText | toneScore (0-100) |

**学習項目**:
```
文体プロファイル {
  punctuation: "。" vs "."（句点の習慣）
  keyphrase: [ "いただきたく", "ご査収" ]（よく使う表現）
  tone: 敬語率 80%（丁寧度）
  paragraph: 2-3 行が平均（段落の長さ）
  greeting: "いつもお世話になっております"（挨拶パターン）
}
```

**フロー**:
```
analyzeSenderStyle(senderEmail)
  ↓
getPastEmails(senderEmail)
  ├─ Google Sheets 検索
  ├─ 件数 < 3 件？ → デフォルト返却
  └─ 件数 ≥ 3 件 → extractPatterns()
  
extractPatterns(pastEmails)
  ├─ 形態素解析（日本語）
  ├─ 句点パターン分析
  ├─ 敬語率計算
  ├─ 段落構造分析
  └─ return { style_profile }
```

---

### 7. **AutoResponder.gs** - 自動返信生成

| 関数 | 入力 | 出力 |
|------|------|------|
| `generateResponse()` | { emailText, styleProfile } | 返信テキスト |
| `callClaudeForResponse()` | prompt | 生成テキスト |
| `sendReply()` | messageId, replyText | 送信完了 ✓ |

**Claude Prompt テンプレート**:
```
"""
【タスク】以下の文体で返信メールを生成してください。

【元のメール】
{original_email}

【返信者の文体情報】
{style_profile}

【返信内容の条件】
- スコアが 70 未満のため自動返信
- 感謝・検討中・対応予定を伝える
- 返信者の文体に完全に合わせる
- 2-3 段落、150-200 字

【出力】
返信メール本文（件名 "Re:" は不要）
"""
```

---

### 8. **CRMLogger.gs** - Google Sheets ログ記録

| シート | 記録内容 |
|-------|---------|
| **Email-Log** | メール ID、日時、送信者、スコア、処理結果 |
| **Sender-History** | 送信者の過去メール（文体学習用） |
| **Score-Statistics** | 日別・週別スコア平均 |
| **Style-Database** | 各送信者の文体プロファイル |

**記録項目**:
```
Email-Log シート:
┌─────────┬─────────┬──────────┬─────────┬────────────┬──────────────┐
│ Date    │ Time    │ Sender   │ Subject │ Score      │ Action       │
├─────────┼─────────┼──────────┼─────────┼────────────┼──────────────┤
│2026-05-05│14:30:00│sato@...  │提案...  │85 (⭐⭐⭐⭐⭐)│Forward       │
│2026-05-05│10:15:00│taro@...  │質問...  │42 (⭐⭐)  │Auto-Reply    │
└─────────┴─────────┴──────────┴─────────┴────────────┴──────────────┘

Style-Database シート:
┌──────────┬────────────────┬─────────┬──────────┬──────────────┐
│ Sender   │ Common-Phrases │ Tone    │ Greeting │ Last-Updated │
├──────────┼────────────────┼─────────┼──────────┼──────────────┤
│sato@...  │ご査収ください  │丁寧 89% │いつもお世話│2026-05-05   │
└──────────┴────────────────┴─────────┴──────────┴──────────────┘
```

**主要関数**:
```
logToSheets()              → メール情報を記録
updateSenderProfile()      → 送信者プロファイル更新
recordStyleProfile()       → 文体情報保存
queryEmailHistory()        → 過去メール検索
calculateDailyStatistics() → 日別統計計算
```

---

### 9. **PermissionManager.gs** - ロール・アクセス制御

| ロール | 閲覧範囲 | 操作権限 |
|-------|---------|---------|
| **管理職** (admin) | 全スタッフのメール | 全操作可能 |
| **営業** (sales) | 個人メール + チーム勤怠 | 個人メール操作 |
| **マネージャー** (manager) | 自部門スタッフ + メール | 承認・却下 |

**アクセス制御ロジック**:
```
checkAccess(userId, action)
  ↓
getUserRole(userId)
  ├─ Role = "admin"
  │   └─ return TRUE (全アクセス許可)
  │
  ├─ Role = "manager"
  │   └─ checkDepartmentMatch(userId, targetUserId)
  │       ├─ 同部門 → TRUE
  │       └─ 他部門 → FALSE
  │
  └─ Role = "sales"
      └─ checkOwnerMatch(userId, targetUserId)
         ├─ 本人 → TRUE
         ├─ チーム勤怠 → TRUE (閲覧のみ)
         └─ 他人 → FALSE

maskData(userId, data)
  ├─ Role = "admin" → data 全件返却
  ├─ Role = "manager" → 自部門のみ
  └─ Role = "sales" → 個人 + チーム勤怠のみ
```

**主要関数**:
```
checkUserRole()          → ユーザーロール取得
checkAccessPermission()  → アクセス権限チェック
maskSensitiveData()      → 非表示データマスク
recordAuditLog()         → 操作ログ記録
```

---

## 🔌 外部 API 連携

### Claude API（AIAnalyzer, AutoResponder から）

```
呼び出し元: AIAnalyzer.gs, AutoResponder.gs

エンドポイント:
  POST https://api.anthropic.com/v1/messages

認証:
  Header: x-api-key: {CLAUDE_API_KEY}

リクエスト例:
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "【prompt】{emailText}"
    }
  ]
}

レスポンス:
{
  "content": [
    {
      "type": "text",
      "text": "..." 
    }
  ]
}

エラーハンドリング:
  - API キー無効 → ログ記録、スキップ
  - レート制限 → リトライ（3回）
  - タイムアウト → デフォルト応答
```

### Gmail API（EmailHandler から）

```
呼び出し元: EmailHandler.gs, AutoResponder.gs

メソッド:
  - gmail.users.messages.get()     → メール取得
  - gmail.users.messages.send()    → メール送信
  - gmail.users.labels.create()    → ラベル作成
  - gmail.users.labels.list()      → ラベル一覧
  - gmail.users.messages.modify()  → メール属性変更

例: メール転送
{
  raw: base64(RFC 5322 format email)
  threadId: "xxx" (スレッド保持)
}

権限スコープ:
  - https://www.googleapis.com/auth/gmail.modify
  - (読み取り・書き込み・ラベル管理)
```

### Google Sheets API（CRMLogger から）

```
呼び出し元: CRMLogger.gs

メソッド:
  - spreadsheets.values.append()   → データ追加
  - spreadsheets.values.get()      → データ取得
  - spreadsheets.values.update()   → データ更新
  - spreadsheets.batchGet()        → 複数範囲取得

例: Email-Log に行追加
{
  range: "'Email-Log'!A1",
  values: [
    ["2026-05-05", "14:30:00", "sato@...", "提案", 85, "Forward"]
  ]
}
```

---

## 🔐 データフロー＆セキュリティ

### データ暗号化・保存ルール

```
┌────────────────────────────────────┐
│  取得データ → 処理 → 保存            │
├────────────────────────────────────┤
│                                    │
│ 1. メール本文                      │
│    └─ 保存: Google Sheets (暗号化) │
│       保有期間: 12 ヶ月             │
│                                    │
│ 2. Claude API レスポンス           │
│    └─ 保存: ログのみ               │
│       保有期間: 3 ヶ月              │
│                                    │
│ 3. 個人情報（送信者）              │
│    └─ 保存: Style-Database         │
│       マスク: 企業名のみ            │
│       保有期間: アカウント削除時まで 
│                                    │
│ 4. API キー                        │
│    └─ 保存: Google Apps Script     │
│             スクリプト プロパティ    │
│       暗号化: 自動（Google 側）    │
│                                    │
└────────────────────────────────────┘
```

---

## 📊 実行パフォーマンス指標

### API コール数（1 メール処理あたり）

```
① EmailHandler        : 2 calls  (メール取得 × 2)
② AIAnalyzer (Claude) : 1 call   (スコア判定)
③ StyleLearner        : 1 call   (過去メール検索)
④ AutoResponder       : 1 call   (返信生成) ※スコア <70 のみ
⑤ CRMLogger           : 2 calls  (ログ記録 × 2)
⑥ Gmail API           : 2 calls  (転送or返信送信、ラベル)
───────────────────────────────────
合計: 9 calls / メール（平均）

スコア ≥ 70 の場合: 7 calls
スコア < 70 の場合: 9 calls
```

### 処理時間（目安）

```
EmailHandler        : 500ms
AIAnalyzer          : 2,000ms ← Claude API レイテンシ
StyleLearner        : 1,000ms ← Sheets 検索
AutoResponder       : 2,000ms ← Claude API レイテンシ
CRMLogger           : 800ms   ← Sheets 書き込み
Gmail (転送/返信)    : 1,500ms ← Gmail API
─────────────────────────────
合計: 7～8秒 / メール

※ 複数メールが同時到着: 順序処理（逐次実行）
```

### Google Apps Script クォーター

```
サービス制限（1 日あたり）:

① Gmail API クォーター: 100,000 メール / 日
   → 1,000 メール / 日なら余裕

② Google Sheets: 500,000 書き込み / 日
   → ログ記録で問題なし

③ Google Apps Script 実行時間: 360 分/ 日
   → 8秒/メール × 1,000メール = 135 分 ✓
```

---

## 🚀 デプロイメント順序

```
Phase 1: Local Development
┌──────────────────────┐
│ 1. Config.gs         │ (定数・環境変数)
│ 2. Main.gs           │ (エントリーポイント)
│ 3. EmailHandler.gs   │ (メール取得)
└──────────────────────┘

Phase 2: Core Logic
┌──────────────────────┐
│ 4. AIAnalyzer.gs     │ (スコア判定)
│ 5. StyleLearner.gs   │ (文体学習)
│ 6. AutoResponder.gs  │ (返信生成)
└──────────────────────┘

Phase 3: Infrastructure
┌──────────────────────┐
│ 7. CRMLogger.gs      │ (ログ記録)
│ 8. PermissionManager │ (アクセス制御)
└──────────────────────┘

Phase 4: UI
┌──────────────────────┐
│ 9. Dashboard.gs      │ (UI・表示)
└──────────────────────┘
```

---

## 🔗 ファイル間の呼び出し関係

```
Main.gs
├─ onOpen()
│  ├─→ Config.getConfig()
│  ├─→ PermissionManager.checkUserRole()
│  └─→ Dashboard.initialize()
│
└─ onMailReceive(event)
   ├─→ Config.getConfig()
   ├─→ EmailHandler.extractEmailData(event)
   │  └─→ Gmail API: messages.get()
   ├─→ PermissionManager.checkAccess()
   ├─→ AIAnalyzer.analyzeEmail()
   │  └─→ Claude API: POST /messages
   ├─→ StyleLearner.analyzeSenderStyle()
   │  └─→ CRMLogger.queryEmailHistory()
   │     └─→ Google Sheets API: values.get()
   │
   ├─ スコア ≥ 70?
   │  ├─ YES: EmailHandler.forwardToPersonal()
   │  │       └─→ Gmail API: messages.send()
   │  │
   │  └─ NO:  AutoResponder.generateResponse()
   │          ├─→ Claude API: POST /messages
   │          └─→ AutoResponder.sendReply()
   │             └─→ Gmail API: messages.send()
   │
   ├─→ EmailHandler.applyLabel()
   │  └─→ Gmail API: labels.modify()
   ├─→ CRMLogger.logToSheets()
   │  └─→ Google Sheets API: values.append()
   └─→ Dashboard.updateUI()
```

---

## ✅ テストシナリオ

### テストケース 1: 高スコアメール（スコア ≥ 70）

```
Input:
  件名: "営業 AI ツール導入の提案についてお伺いしたく"
  本文: "予算確認とスケジュール相談がしたい..."
  送信者: Yamada <yamada@client.jp>

Processing:
  ① EmailHandler: メール取得 ✓
  ② AIAnalyzer: スコア = 85 (高い) ✓
  ③ StyleLearner: 文体取得 or デフォルト ✓
  ④ Auto-respond? NO (スコア >= 70)
  ⑤ Forward: yamada@abc.com へ転送 ✓
  ⑥ CRMLogger: 記録 ✓
  ⑦ Dashboard: UI 更新 ✓

Expected Output:
  ✓ yamada@abc.com に転送完了
  ✓ ラベル "High-Priority" 付与
  ✓ CRM に記録
```

### テストケース 2: 低スコアメール（スコア < 70）

```
Input:
  件名: "一般的な質問です"
  本文: "貴社の営業時間を教えてください..."
  送信者: Suzuki <suzuki@inquiry.jp>

Processing:
  ① EmailHandler: メール取得 ✓
  ② AIAnalyzer: スコア = 35 (低い) ✓
  ③ StyleLearner: 文体取得 or デフォルト ✓
  ④ Auto-respond? YES (スコア < 70)
  ⑤ AutoResponder: 返信テキスト生成 ✓
     (送信者の文体で作成)
  ⑥ Send Reply: suzuki@inquiry.jp へ返信 ✓
  ⑦ CRMLogger: 記録 ✓
  ⑧ Dashboard: UI 更新 ✓

Expected Output:
  ✓ suzuki@inquiry.jp に自動応答送信
  ✓ ラベル "Auto-Replied" 付与
  ✓ CRM に記録
```

---

## 📈 スケーラビリティ

### スケール対応戦略

```
Current (v1.0):
  ├─ メール処理: 逐次処理（順番に）
  ├─ API コール: 同期（待つ）
  ├─ ユーザー数: 5～50 人
  └─ 月間メール: 5,000～10,000 件

Future (v2.0):
  ├─ メール処理: 並列処理（複数同時）
  ├─ API コール: キューイング + 非同期処理
  ├─ ユーザー数: 100～1,000 人
  └─ 月間メール: 50,000～100,000 件

Optimization Points:
  ① Claude API キャッシング
     - 同じ送信者のメール → キャッシュ再利用
     
  ② バッチ処理
     - Google Sheets 書き込みを集約
     - 1 回の API コール = 複数行
     
  ③ マイクロサービス化
     - AIAnalyzer → Cloud Function へ移行
     - StyleLearner → Vertex AI へ移行
```

---

## 🎓 まとめ

このツリー構造は、**Gmail AddOn システム**の完全な技術設計を示しています：

| 層 | ファイル数 | 役割 |
|----|----------|------|
| **Entry** | 1 | Main.gs（初期化・トリガー） |
| **Config** | 1 | Config.gs（設定管理） |
| **Processing** | 5 | EmailHandler, AIAnalyzer, StyleLearner, AutoResponder, CRMLogger |
| **Infrastructure** | 2 | Dashboard.gs, PermissionManager.gs |
| **外部連携** | 3 | Claude API, Gmail API, Google Sheets API |

**実装の開始はこのツリー構造に従い、各ファイルの依存関係を確認しながら段階的に進めてください。**

