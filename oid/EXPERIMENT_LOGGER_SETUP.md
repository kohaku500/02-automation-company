# 実験記録自動化アプリ セットアップガイド

**完成日**: 2026-05-10  
**対象ファイル**:
- `experiment-gas.gs` - Google Apps Script バックエンド
- `experiment-logger.html` - フロントエンド（HTML SPA）

---

## 全体の流れ

```
1. Google Sheet 作成
   ↓
2. Google Apps Script にコードを貼り付け
   ↓
3. プロパティに API キーと Sheet ID を設定
   ↓
4. Web App としてデプロイ
   ↓
5. HTML に デプロイ URL を設定
   ↓
6. ブラウザで HTML を開く
```

---

## Step 1: Google Sheets の作成

1. **Google Sheets を新規作成**
   - https://sheets.google.com → **「＋」（新規）** をクリック
   
2. **シート名を変更** (必須)
   - デフォルトの "Sheet1" を **「実験ログ」** に変更
   - 右クリック → 「シートの名前変更」

3. **Sheet ID を確認** (後で必要)
   - URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`
   - 例: `https://docs.google.com/spreadsheets/d/1-AB_cdefGH1ijklmnOpQr2StUVwxyzABC/edit`
   - **[SHEET_ID]** の部分をコピーして保存

---

## Step 2: Google Apps Script のセットアップ

### 2.1 Google Apps Script エディタを開く

1. Google Sheets で **「ツール」→「Apps Script」** をクリック
   
2. 新しいタブが開き、Apps Script エディタが表示されます

### 2.2 コードを貼り付け

1. デフォルトの `Code.gs` を**全て削除**

2. `experiment-gas.gs` の全コードをコピーして貼り付け

3. **保存** (Ctrl+S または Cmd+S)

### 2.3 スクリプトプロパティに設定

1. **「プロジェクト設定」** をクリック（ツールアイコン）

2. **「プロパティ」タブ** で 「スクリプトプロパティ」を開く

3. **以下を追加**（「行を追加」ボタン）:

| プロパティ名 | 値 |
|---|---|
| `SPREADSHEET_ID` | Step 1 で確認した Sheet ID |
| `GEMINI_API_KEY` | (次の Step で取得) |

4. 一度は `GEMINI_API_KEY` を仮の値（例: `temp`）で設定して進めて、後で更新

---

## Step 3: Google AI Studio で API キー取得

1. **Google AI Studio を開く**
   - https://aistudio.google.com/

2. **「API key」** をクリック

3. **「Create API key」** → **「In a new project」** をクリック

4. **生成されたキーをコピー** (紫色のボタン)

5. **Apps Script に設定**
   - 前のタブに戻る（Apps Script エディタ）
   - 「プロジェクト設定」→ 「スクリプトプロパティ」
   - `GEMINI_API_KEY` の値を **生成されたキー** に変更
   - 保存

---

## Step 4: Web App として Deploy

### 4.1 Deploy を実行

1. Apps Script エディタで **「Deploy」** をクリック

2. **「New Deployment」** をクリック

3. **デプロイ設定**:
   - **Deployment type**: Web app
   - **Execute as**: 自分のアカウント（メールアドレス）
   - **Who has access**: Anyone

4. **「Deploy」** をクリック

### 4.2 デプロイ URL を確認

**重要**: デプロイ URL をコピーします

```
https://script.google.com/macros/s/[SCRIPT_ID]/usercontent
```

デプロイ後、以下の形式で表示されます:
```
Deployment ID: AKfycbz...
New URL: https://script.google.com/macros/s/AKfycbz.../usercontent
```

**この URL（`usercontent` の部分）をコピーして保存**

---

## Step 5: HTML に URL を設定

1. `experiment-logger.html` を**テキストエディター**で開く

2. **以下を検索**:
   ```javascript
   const GAS_WEB_APP_URL = "YOUR_GAS_WEB_APP_URL_HERE";
   ```

3. **Step 4 で取得した URL に置き換え**:
   ```javascript
   const GAS_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz.../usercontent";
   ```

4. **保存** (Ctrl+S)

---

## Step 6: 動作確認

### 6.1 HTML を開く

1. `experiment-logger.html` をダブルクリック
   - またはブラウザにドラッグ&ドロップ
   - またはブラウザで「File → Open」で選択

2. **画面が表示される**:
   ```
   📋 実験記録自動化
   手書き実験記録をAIが自動で定形化します
   ```

### 6.2 テスト記録を作成

1. **試験種別を選択** → 「性能試験」をクリック

2. **フォームに入力**:
   - 試験日時: `2026-05-10 14:30`
   - 製品名: `M5 Core S3`
   - 型番: `M5-CSU001`
   - その他: 適当に入力

3. **「記録を保存」** をクリック

### 6.3 Google Sheets で確認

1. Google Sheets のタブに戻る（更新ボタン F5）

2. **新しい行が追加されていることを確認**:
   ```
   | 記録ID | 登録日時 | 試験種別 | 製品名 | ...
   | exp-... | 2026/5/10 ... | 性能試験 | M5 Core S3 | ...
   ```

**成功！** ✅

---

## 機能詳細

### 📸 画像アップロード + AI 解析

1. **画像をアップロード** → ドラッグ&ドロップまたはクリック

2. **「🔍 解析を実行」** をクリック

3. **AI（Gemini）が自動抽出**:
   - 試験日時
   - 製品名
   - 測定値
   - 観察事項
   - **AI 考察**（自動生成）

4. フォームが自動入力される（修正可能）

5. **「💾 記録を保存」** → Google Sheets に保存

### 📝 テキスト入力モード

- 「テキストで直接入力する」 をチェック
- 画像の代わりに手動で入力
- AI 考察は表示されない

### 📋 履歴機能

- 過去50件まで **localStorage** に保存
- 「📋 履歴を表示」 で確認可能
- ブラウザのデータをクリアすると消える

---

## トラブルシューティング

### 症状: 画面が開くが、API キーエラー

**原因**: GAS_WEB_APP_URL が間違っている

**対処**:
1. Apps Script のデプロイを確認
2. URL が `usercontent` で終わっているか確認
3. HTML の `GAS_WEB_APP_URL` を再度確認

### 症状: 「解析を実行」をクリックしても何も起こらない

**原因**: API キーが未設定

**対処**:
1. Apps Script → プロジェクト設定 → スクリプトプロパティ
2. `GEMINI_API_KEY` が正しく設定されているか確認
3. 値が空欄でないか確認

### 症状: 「記録を保存」後、Google Sheets に追加されない

**原因**: SPREADSHEET_ID が違う

**対処**:
1. Google Sheets の URL を確認
2. `/d/` と `/edit` の間の ID をコピー
3. Apps Script → プロジェクト設定 → スクリプトプロパティ
4. `SPREADSHEET_ID` を正確に貼り付け

### 症状: 「シートが見つからない」エラー

**原因**: シート名が「実験ログ」ではない

**対処**:
1. Google Sheets を確認
2. シート名を「実験ログ」に変更（必須）
3. または、GAS の `const SHEET_NAME = "実験ログ"` を自分のシート名に変更

### 症状: CORS エラー

**原因**: Web App のデプロイ設定が不適切

**対処**:
1. Apps Script → Deploy → Recent Deployments
2. デプロイ URL の歯車アイコン → 「Edit」
3. Execute as: 自分のアカウント
4. Who has access: **Anyone**
5. 更新

---

## セキュリティ上の注意

⚠️ **API キーの取り扱い**:

- `GEMINI_API_KEY` は **プロジェクトプロパティ** に保存
- HTML には埋め込まれていない
- GAS 経由で安全に配信

⚠️ **Google Sheets へのアクセス**:

- 誰でも Web App URL にアクセスできるので、**リンクは公開しない**
- 必要に応じて、Google Apps Script で認証を追加

---

## 使用例

### 例1: 製品テスト記録

```
1. 手書き実験記録を撮影 📸
2. HTML にアップロード
3. AI が自動抽出
4. 「記録を保存」
5. Google Sheets で集計・分析
```

### 例2: チーム共有

```
1. Google Sheets をチームで共有
2. 複数人が HTML にアクセス
3. 各自が記録をアップロード
4. Google Sheets に集約
```

---

## カスタマイズ

### 試験種別を追加

`experiment-logger.html` で以下を探す:

```html
<div class="chip" data-type="性能試験">性能試験</div>
<div class="chip" data-type="耐久試験">耐久試験</div>
<div class="chip" data-type="動作試験">動作試験</div>
<div class="chip" data-type="その他">その他</div>
```

以下のように追加:

```html
<div class="chip" data-type="品質検査">品質検査</div>
```

### Google Sheets のカラムを追加

`experiment-gas.gs` で以下を探す:

```javascript
function initHeaderIfNeeded(spreadsheetId, sheetName) {
  ...
  sheet.appendRow([
    "記録ID",
    "登録日時",
    ...
    "ステータス"
  ]);
}
```

新しいカラム名を追加し、`appendRecord` 関数でも対応する値を追加。

---

## 次のステップ

- [ ] Google Sheets でグラフを作成
- [ ] AI 考察をさらに詳細に（プロンプトを編集）
- [ ] 認証を追加（特定ユーザーのみ）
- [ ] テンプレート機能（頻出パターンを素早く入力）

---

**セットアップ完了。では実験記録を自動化しましょう！** 🚀
