/**
 * セットアップウィザード - 全自動初期化スクリプト
 *
 * 使用方法:
 * 1. Google Apps Script エディタを開く (https://script.google.com)
 * 2. 新規プロジェクト作成: "セットアップウィザード"
 * 3. このコードをコピペ
 * 4. 関数を実行: runFullSetup()
 * 5. 初回実行時は認可が求められるので「許可」をクリック
 *
 * 実行時間: 5-10 分
 * 作成される内容:
 * - Gmail ラベル 3 個
 * - Google Sheets テンプレート 8 個
 * - サンプルデータ＆ヘッダー行
 * - 自動集計式
 */

// ========== メイン実行関数 ==========
function runFullSetup() {
  try {
    Logger.log("🚀 セットアップウィザード開始...");

    // ステップ 1: Gmail ラベル作成
    Logger.log("\n【Step 1】Gmail ラベル作成中...");
    createGmailLabels();

    // ステップ 2: Google Drive フォルダ作成
    Logger.log("\n【Step 2】Google Drive フォルダ作成中...");
    const folderId = createDriveFolder("収益会社_AI_System");

    // ステップ 3: Google Sheets テンプレート作成
    Logger.log("\n【Step 3】Google Sheets テンプレート作成中...");
    const spreadsheetIds = createAllSpreadsheets(folderId);

    // ステップ 4: 環境変数設定
    Logger.log("\n【Step 4】環境変数を設定中...");
    setEnvironmentVariables(spreadsheetIds);

    // ステップ 5: トリガー設定
    Logger.log("\n【Step 5】トリガー設定中...");
    createTriggers();

    Logger.log("\n✅ セットアップ完了！");
    Logger.log("\n【重要】次のステップ:");
    Logger.log("1. Google Apps Script 設定 → Project Properties を開く");
    Logger.log("2. SLACK_WEBHOOK_URL を設定（オプション）");
    Logger.log("3. Google Apps Script の Code.gs に Agent コードをコピペ");
    Logger.log("4. 明日 5/5 にテスト実行を開始");

  } catch (error) {
    Logger.log("❌ エラーが発生しました: " + error.toString());
    throw error;
  }
}

// ========== Gmail ラベル作成 ==========
function createGmailLabels() {
  const labels = [
    { name: "Agent-Inbox", description: "営業メール自動応答用" },
    { name: "Customer-Conversation", description: "顧客会話記録用" },
    { name: "応答済み", description: "自動応答完了メール" }
  ];

  labels.forEach((label) => {
    try {
      // 既存ラベルをチェック
      const existing = GmailApp.getUserLabelByName(label.name);
      if (existing) {
        Logger.log(`  ⚠️  ラベル '${label.name}' は既に存在します。スキップ。`);
        return;
      }

      GmailApp.createLabel(label.name);
      Logger.log(`  ✅ ラベル '${label.name}' を作成しました`);
    } catch (error) {
      Logger.log(`  ⚠️  ラベル '${label.name}' の作成に失敗: ${error.toString()}`);
    }
  });
}

// ========== Google Drive フォルダ作成 ==========
function createDriveFolder(folderName) {
  try {
    // 既存フォルダをチェック
    const existing = DriveApp.getFoldersByName(folderName);
    if (existing.hasNext()) {
      const folder = existing.next();
      Logger.log(`  ⚠️  フォルダ '${folderName}' は既に存在します。既存フォルダを使用します。`);
      return folder.getId();
    }

    // 新規フォルダ作成
    const folder = DriveApp.createFolder(folderName);
    Logger.log(`  ✅ フォルダ '${folderName}' を作成しました`);
    Logger.log(`     フォルダ ID: ${folder.getId()}`);
    return folder.getId();
  } catch (error) {
    Logger.log(`  ❌ フォルダ作成失敗: ${error.toString()}`);
    throw error;
  }
}

// ========== Google Sheets テンプレート作成 ==========
function createAllSpreadsheets(folderId) {
  const folder = DriveApp.getFolderById(folderId);
  const spreadsheetIds = {};

  // 1. KPI-Raw-Data
  Logger.log("  → KPI-Raw-Data 作成中...");
  spreadsheetIds.kpiRawData = createKPIRawData(folder);

  // 2. CRM-Master
  Logger.log("  → CRM-Master 作成中...");
  spreadsheetIds.crmMaster = createCRMMaster(folder);

  // 3. Agent-Log
  Logger.log("  → Agent-Log 作成中...");
  spreadsheetIds.agentLog = createAgentLog(folder);

  // 4. Agent-Templates
  Logger.log("  → Agent-Templates 作成中...");
  spreadsheetIds.agentTemplates = createAgentTemplates(folder);

  // 5. Sent-Log
  Logger.log("  → Sent-Log 作成中...");
  spreadsheetIds.sentLog = createSentLog(folder);

  // 6. KPI-Summary
  Logger.log("  → KPI-Summary 作成中...");
  spreadsheetIds.kpiSummary = createKPISummary(folder);

  // 7. Lead-Extraction-Log
  Logger.log("  → Lead-Extraction-Log 作成中...");
  spreadsheetIds.leadExtraction = createLeadExtractionLog(folder);

  // 8. Conversation-Summary
  Logger.log("  → Conversation-Summary 作成中...");
  spreadsheetIds.conversationSummary = createConversationSummary(folder);

  // 9. Error-Log
  Logger.log("  → Error-Log 作成中...");
  spreadsheetIds.errorLog = createErrorLog(folder);

  return spreadsheetIds;
}

// ========== 各 Spreadsheet 作成関数 ==========

function createKPIRawData(folder) {
  const ss = SpreadsheetApp.create("KPI-Raw-Data", 10, 10);
  const sheet = ss.getSheets()[0];
  sheet.setName("Daily-Metrics");

  // ヘッダー行
  sheet.getRange(1, 1, 1, 10).setValues([[
    "日付",
    "曜日",
    "営業メール送信数",
    "メール返信数",
    "返信率(%)",
    "AI Agent 成功",
    "AI Agent エラー",
    "CRM 新規登録",
    "高優先度返信",
    "備考"
  ]]);

  // サンプルデータ（Day 1-5）
  const sampleData = [
    ["2026-06-01", "Sunday", 50, 5, 10, 50, 0, 5, 1, "初日営業メール第1陣"],
    ["2026-06-02", "Monday", 50, 8, 16, 50, 0, 8, 2, "テンプレートv2テスト開始"],
    ["2026-06-03", "Tuesday", 50, 12, 24, 48, 2, 10, 3, "返信率上向き傾向"],
    ["2026-06-04", "Wednesday", 60, 18, 30, 60, 0, 15, 4, "新施策テスト開始"],
    ["2026-06-05", "Thursday", 0, 8, 0, 0, 0, 0, 0, "Week1振返り日"]
  ];
  sheet.getRange(2, 1, 5, 10).setValues(sampleData);

  // フォルダに移動
  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ KPI-Raw-Data (ID: ${ss.getId()})`);
  return ss.getId();
}

function createCRMMaster(folder) {
  const ss = SpreadsheetApp.create("CRM-Master", 10, 13);
  const sheet = ss.getSheets()[0];

  // ヘッダー行
  sheet.getRange(1, 1, 1, 13).setValues([[
    "顧客ID",
    "企業名",
    "代表メール",
    "従業員数",
    "電話番号",
    "部門",
    "ステータス",
    "関心度",
    "初回接触日",
    "最終更新日",
    "主なニーズ",
    "副次ニーズ",
    "抽出スコア"
  ]]);

  // サンプルデータ
  sheet.getRange(2, 1, 1, 13).setValues([[
    1, "(株)サンプルA", "contact@sample-a.co.jp", 50, "090-1234-5678",
    "開発部", "新規", "高", "2026-06-01", "2026-06-01", "自動化", "効率化", 5
  ]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ CRM-Master (ID: ${ss.getId()})`);
  return ss.getId();
}

function createAgentLog(folder) {
  const ss = SpreadsheetApp.create("Agent-Log", 50, 9);
  const sheet = ss.getSheets()[0];

  sheet.getRange(1, 1, 1, 9).setValues([[
    "タイムスタンプ",
    "件名",
    "送信者メール",
    "関心度",
    "対応状況",
    "企業名",
    "従業員数",
    "電話番号",
    "部門"
  ]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ Agent-Log (ID: ${ss.getId()})`);
  return ss.getId();
}

function createAgentTemplates(folder) {
  const ss = SpreadsheetApp.create("Agent-Templates", 5, 6);
  const sheet = ss.getSheets()[0];

  // ヘッダー
  sheet.getRange(1, 1, 1, 6).setValues([[
    "パターンキーワード",
    "判定",
    "テンプレート本文",
    "フォローアップ日",
    "バージョン",
    "更新日"
  ]]);

  // 関心度: 高
  sheet.getRange(2, 1, 1, 6).setValues([[
    "具体的な質問",
    "関心度: 高",
    "お疲れ様です。\nご関心ありがとうございます。具体的なご要望をお聞きいただき、心強いです。\n\nより詳細な提案をさせていただくため、15分の無料相談をご提案させていただきたいのですが、\nご都合のつく日時はありますでしょうか？\n\nhttps://calendly.com/takada-makoto/consultation\n\n誠一",
    "3日後",
    "1.0",
    "2026-05-03"
  ]]);

  // 関心度: 中
  sheet.getRange(3, 1, 1, 6).setValues([[
    "簡潔な問い合わせ",
    "関心度: 中",
    "お疲れ様です。\nご問い合わせありがとうございます。\n\n弊社の取り組みについて、より詳しくご説明させていただきたく、\n初回相談をお勧めいたします。\n\nhttps://calendly.com/takada-makoto/consultation\n\n誠一",
    "1日後",
    "1.0",
    "2026-05-03"
  ]]);

  // 関心度: 低
  sheet.getRange(4, 1, 1, 6).setValues([[
    "テンプレート的",
    "関心度: 低",
    "お疲れ様です。\nこの度は情報請求いただき、ありがとうございます。\n\n詳細な資料をお送りいたします。\nご不明な点やご質問があれば、いつでもお気軽にお問い合わせください。\n\n今後ともよろしくお願いいたします。\n誠一",
    "5日後",
    "1.0",
    "2026-05-03"
  ]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ Agent-Templates (ID: ${ss.getId()})`);
  return ss.getId();
}

function createSentLog(folder) {
  const ss = SpreadsheetApp.create("Sent-Log", 100, 12);
  const sheet = ss.getSheets()[0];

  sheet.getRange(1, 1, 1, 12).setValues([[
    "送信日時",
    "パターン",
    "相手企業",
    "相手メール",
    "件名",
    "送信完了",
    "開封日時",
    "開封済",
    "返信日時",
    "返信済",
    "返信内容",
    "次アクション"
  ]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ Sent-Log (ID: ${ss.getId()})`);
  return ss.getId();
}

function createKPISummary(folder) {
  const ss = SpreadsheetApp.create("KPI-Summary", 5, 10);
  const sheet = ss.getSheets()[0];
  sheet.setName("Dashboard");

  // ダッシュボード内容
  const dashboardData = [
    ["【Today's KPI】", ""],
    ["本日の日付:", "=TODAY()"],
    ["営業メール送信数:", "=SUMIF('KPI-Raw-Data'!A:A, TODAY(), 'KPI-Raw-Data'!C:C)"],
    ["メール返信数:", "=SUMIF('KPI-Raw-Data'!A:A, TODAY(), 'KPI-Raw-Data'!D:D)"],
    ["返信率(%):", "=IF(D3=0, 0, D4/D3*100)"],
    ["", ""],
    ["【Week's KPI】", ""],
    ["週計営業メール:", "=SUMIFS('KPI-Raw-Data'!C:C,'KPI-Raw-Data'!A:A,\">=\"&(TODAY()-6),'KPI-Raw-Data'!A:A,\"<=\"&TODAY())"],
    ["週計返信数:", "=SUMIFS('KPI-Raw-Data'!D:D,'KPI-Raw-Data'!A:A,\">=\"&(TODAY()-6),'KPI-Raw-Data'!A:A,\"<=\"&TODAY())"]
  ];

  sheet.getRange(1, 1, dashboardData.length, 2).setValues(dashboardData);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ KPI-Summary (ID: ${ss.getId()})`);
  return ss.getId();
}

function createLeadExtractionLog(folder) {
  const ss = SpreadsheetApp.create("Lead-Extraction-Log", 100, 11);
  const sheet = ss.getSheets()[0];

  sheet.getRange(1, 1, 1, 11).setValues([[
    "抽出タイムスタンプ",
    "メールアドレス",
    "企業名",
    "従業員数",
    "電話番号",
    "部門",
    "業種",
    "主なニーズ",
    "副次ニーズ",
    "抽出スコア",
    "登録ステータス"
  ]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ Lead-Extraction-Log (ID: ${ss.getId()})`);
  return ss.getId();
}

function createConversationSummary(folder) {
  const ss = SpreadsheetApp.create("Conversation-Summary", 100, 8);
  const sheet = ss.getSheets()[0];

  sheet.getRange(1, 1, 1, 8).setValues([[
    "生成タイムスタンプ",
    "スレッドID",
    "メール数",
    "件名",
    "抽出キーワード",
    "優先度",
    "次のステップ",
    "最終更新"
  ]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ Conversation-Summary (ID: ${ss.getId()})`);
  return ss.getId();
}

function createErrorLog(folder) {
  const ss = SpreadsheetApp.create("Error-Log", 100, 2);
  const sheet = ss.getSheets()[0];

  sheet.getRange(1, 1, 1, 2).setValues([["タイムスタンプ", "エラーメッセージ"]]);

  const file = DriveApp.getFileById(ss.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  Logger.log(`    ✅ Error-Log (ID: ${ss.getId()})`);
  return ss.getId();
}

// ========== 環境変数設定 ==========
function setEnvironmentVariables(spreadsheetIds) {
  const props = PropertiesService.getUserProperties();

  // メインの Spreadsheet ID を設定
  props.setProperty("SPREADSHEET_ID", spreadsheetIds.kpiRawData);

  Logger.log(`  ✅ 環境変数を設定しました`);
  Logger.log(`     SPREADSHEET_ID: ${spreadsheetIds.kpiRawData}`);
}

// ========== トリガー作成 ==========
function createTriggers() {
  // 注: このセットアップウィザード用プロジェクトではなく、
  // メインの Google Apps Script プロジェクト（Agent コード）に
  // トリガーを設定する必要があります

  Logger.log(`  ℹ️  トリガー設定は手動で行う必要があります`);
  Logger.log(`     1. メインの Google Apps Script プロジェクト（Code.gs）を開く`);
  Logger.log(`     2. 左メニュー → トリガー → 新規トリガー`);
  Logger.log(`     3. 関数: checkAndReplyToEmails → 1時間ごと`);
  Logger.log(`     4. 同様に Agent 2, Agent 3 のトリガーも設定`);
}

// ========== ユーティリティ: 既存 Spreadsheet を削除 ==========
function deleteExistingSpreadsheets() {
  const sheetNames = [
    "KPI-Raw-Data",
    "CRM-Master",
    "Agent-Log",
    "Agent-Templates",
    "Sent-Log",
    "KPI-Summary",
    "Lead-Extraction-Log",
    "Conversation-Summary",
    "Error-Log"
  ];

  sheetNames.forEach((name) => {
    const files = DriveApp.getFilesByName(name);
    while (files.hasNext()) {
      files.next().setTrashed(true);
      Logger.log(`🗑️  ${name} を削除しました`);
    }
  });
}

// ========== 確認用: 作成済みファイル一覧表示 ==========
function listCreatedFiles() {
  const folder = DriveApp.getFoldersByName("収益会社_AI_System").next();
  const files = folder.getFiles();

  Logger.log("\n【作成済みファイル一覧】");
  while (files.hasNext()) {
    const file = files.next();
    Logger.log(`- ${file.getName()} (${file.getId()})`);
  }
}
