// ==================== Google Apps Script ====================
// 実験記録自動化アプリ データ受信・Google Sheets 追記スクリプト
//
// このコードを Google Apps Script エディタに貼り付けてください
// https://script.google.com/home
//
// セットアップ手順:
// 1. Google Sheets を作成
// 2. Tools → Apps Script を開く
// 3. このコードを Code.gs に貼り付け
// 4. スクリプトプロパティに設定:
//    - SPREADSHEET_ID = シートのID
//    - GEMINI_API_KEY = Google AI StudioのAPIキー
// 5. Deploy → New Deployment (Web app)
//    - Execute as: your account
//    - Allow access to: Anyone
// 6. HTML の GAS_WEB_APP_URL に デプロイURL を設定
// =========================================================

// ==================== Configuration ====================

function getConfig() {
  const props = PropertiesService.getScriptProperties();
  return {
    spreadsheetId: props.getProperty("SPREADSHEET_ID"),
    sheetName: "実験ログ",
    geminiApiKey: props.getProperty("GEMINI_API_KEY")
  };
}

// ==================== Main Handlers ====================

function doGet(e) {
  try {
    const config = getConfig();

    if (!config.geminiApiKey) {
      return createResponse("error", "GEMINI_API_KEY not configured in script properties");
    }

    // フロントエンドからのAPIキー取得リクエストに応答
    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      apiKey: config.geminiApiKey,
      timestamp: new Date().toISOString()
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    Logger.log("Error in doGet: " + error.toString());
    return createResponse("error", error.toString());
  }
}

function doPost(e) {
  try {
    Logger.log("Request received: " + e.postData.contents);

    // JSON ペイロードを解析
    const data = JSON.parse(e.postData.contents);

    if (!data || !data.record) {
      return createResponse("error", "No record data provided");
    }

    const config = getConfig();

    if (!config.spreadsheetId) {
      return createResponse("error", "SPREADSHEET_ID not configured");
    }

    // Google Sheets を開く
    const sheet = SpreadsheetApp.openById(config.spreadsheetId).getSheetByName(config.sheetName);

    if (!sheet) {
      // シートが存在しない場合は作成
      initHeaderIfNeeded(config.spreadsheetId, config.sheetName);
      const newSheet = SpreadsheetApp.openById(config.spreadsheetId).getSheetByName(config.sheetName);
      appendRecord(newSheet, data.record);
    } else {
      appendRecord(sheet, data.record);
    }

    // 成功レスポンス
    Logger.log("Successfully added record");
    return createResponse("success", "Record saved successfully");

  } catch (error) {
    Logger.log("Error in doPost: " + error.toString());
    return createResponse("error", error.toString());
  }
}

// ==================== Helper Functions ====================

function createResponse(status, message) {
  return ContentService.createTextOutput(JSON.stringify({
    status: status,
    message: message,
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

function appendRecord(sheet, record) {
  // 記録ID生成
  const recordId = "exp-" + new Date().getTime();
  const registeredAt = new Date().toLocaleString('ja-JP');

  // JSON文字列化（測定値用）
  const measurementsJson = JSON.stringify(record.measurements || []);
  const measurementsDisplay = (record.measurements || [])
    .map(m => `${m.item}: ${m.value}${m.unit}`)
    .join(" / ");

  // 行を追記
  sheet.appendRow([
    recordId,                           // A: 記録ID
    registeredAt,                       // B: 登録日時
    record.testType || "",              // C: 試験種別
    record.testDateTime || "",          // D: 試験日時
    record.productName || "",           // E: 製品名
    record.modelNumber || "",           // F: 型番
    (record.testConditions || []).join("\n"),  // G: 試験条件
    measurementsJson,                   // H: 測定値（JSON）
    measurementsDisplay,                // I: 測定値（表示用）
    record.observations || "",          // J: 観察事項
    record.aiAnalysis || "",            // K: AI考察
    record.inputMethod || "画像OCR",    // L: 入力方式
    record.remarks || "",               // M: 備考
    "確認済み"                          // N: ステータス
  ]);
}

function initHeaderIfNeeded(spreadsheetId, sheetName) {
  const ss = SpreadsheetApp.openById(spreadsheetId);
  let sheet = ss.getSheetByName(sheetName);

  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }

  // ヘッダー行を追加（1行目が空の場合）
  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      "記録ID",
      "登録日時",
      "試験種別",
      "試験日時",
      "製品名",
      "型番",
      "試験条件",
      "測定値（JSON）",
      "測定値（表示用）",
      "観察事項",
      "AI考察",
      "入力方式",
      "備考",
      "ステータス"
    ]);
  }
}

// ==================== Utility Functions ====================

/**
 * スプレッドシート ID を確認するための関数
 * Apps Script エディタで実行してログを見る
 */
function getSpreadsheetInfo() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  Logger.log("Current Spreadsheet ID: " + ss.getId());
  Logger.log("Spreadsheet URL: " + ss.getUrl());

  const sheets = ss.getSheets();
  Logger.log("Sheets in this spreadsheet:");
  for (let i = 0; i < sheets.length; i++) {
    Logger.log("  - " + sheets[i].getName());
  }
}

/**
 * スクリプトプロパティを確認
 */
function checkProperties() {
  const props = PropertiesService.getScriptProperties();
  const spreadsheetId = props.getProperty("SPREADSHEET_ID");
  const geminiKey = props.getProperty("GEMINI_API_KEY");

  Logger.log("SPREADSHEET_ID: " + (spreadsheetId ? "✓ Set" : "✗ Not set"));
  Logger.log("GEMINI_API_KEY: " + (geminiKey ? "✓ Set" : "✗ Not set"));
}

/**
 * デプロイ情報を確認するための関数
 */
function getDeploymentUrl() {
  const scriptId = ScriptApp.getScriptId();
  const url = "https://script.google.com/macros/s/" + scriptId + "/usercontent";
  Logger.log("Web App URL (for doGet): " + url);
  Logger.log("Web App URL (for doPost): " + url);
  Logger.log("\nCopy this URL to experiment-logger.html (GAS_WEB_APP_URL constant)");
  return url;
}

/**
 * テストデータで動作確認
 */
function testPost() {
  Logger.log("Testing GAS data receiver...");

  const testRecord = {
    testType: "性能試験",
    testDateTime: "2026-05-10 14:30",
    productName: "M5 Core S3",
    modelNumber: "M5-CSU001",
    testConditions: ["温度: 25°C", "湿度: 60%"],
    measurements: [
      { item: "動作電圧", value: "5.01", unit: "V" },
      { item: "消費電流", value: "0.5", unit: "A" }
    ],
    observations: "画面表示が正常に動作した",
    aiAnalysis: "センサは正常に動作しており、電力消費は仕様内である",
    inputMethod: "テキスト直接入力",
    remarks: "テストデータ"
  };

  const mockEvent = {
    postData: {
      contents: JSON.stringify({ record: testRecord })
    }
  };

  const result = doPost(mockEvent);
  Logger.log("Response: " + result.getContent());
}
