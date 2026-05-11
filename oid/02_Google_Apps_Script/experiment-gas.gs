/**
 * 実験記録自動化アプリ GAS バックエンド v1.0
 *
 * 機能:
 * 1. experiment-logger.html からのAPIキー取得リクエストを処理
 * 2. Gemini API キーを動的に配信
 * 3. 実験記録データをGoogle Sheetsに記録
 */

// ========== グローバル設定 ==========
// PropertiesService から取得（App Script設定画面で事前設定）
const SPREADSHEET_ID = PropertiesService.getScriptProperties().getProperty('SPREADSHEET_ID') || "";
const GEMINI_API_KEY = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY') || "";

// ========== HTTP GETエンドポイント: APIキー配信 ==========
function doGet(e) {
  try {
    // CORS対応 + リクエストバリデーション
    const response = {
      success: true,
      apiKey: GEMINI_API_KEY,
      timestamp: new Date().toISOString()
    };

    return ContentService.createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: error.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

// ========== HTTP POSTエンドポイント: 実験データをSheetsに保存 ==========
function doPost(e) {
  try {
    // リクエストボディをパース
    const data = JSON.parse(e.postData.contents);

    // スプレッドシートを開く
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const logSheet = ss.getSheetByName("実験ログ");

    if (!logSheet) {
      return createErrorResponse("シート '実験ログ' が見つかりません");
    }

    // ヘッダー行がなければ自動作成
    initHeaderIfNeeded(logSheet);

    // データを1行追加
    logSheet.appendRow([
      data.id,                      // A: 記録ID
      new Date(),                   // B: 登録日時
      data.testType,                // C: 試験種別
      data.testDateTime,            // D: 試験日時（手書き）
      data.productName,             // E: 製品名
      data.modelNumber,             // F: 型番
      data.conditions,              // G: 試験条件
      data.measurementsJson,        // H: 測定値（JSON）
      data.measurementsText,        // I: 測定値（表示用）
      data.observations,            // J: 観察事項
      data.aiAnalysis,              // K: AI考察
      data.inputMethod,             // L: 入力方式
      data.notes || "",             // M: 備考
      "確認済み"                    // N: ステータス
    ]);

    // 成功レスポンス
    return ContentService.createTextOutput(
      JSON.stringify({
        success: true,
        row: logSheet.getLastRow(),
        recordId: data.id,
        message: "実験記録を保存しました"
      })
    ).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return createErrorResponse(error.toString());
  }
}

// ========== ヘルパー関数 ==========

/**
 * ヘッダー行がなければ自動作成
 */
function initHeaderIfNeeded(sheet) {
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
    // ヘッダー行を太字にする
    const headerRange = sheet.getRange(1, 1, 1, 14);
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#E8E8E8");
  }
}

/**
 * エラーレスポンスを作成
 */
function createErrorResponse(errorMsg) {
  return ContentService.createTextOutput(
    JSON.stringify({
      success: false,
      error: errorMsg,
      timestamp: new Date().toISOString()
    })
  ).setMimeType(ContentService.MimeType.JSON);
}
