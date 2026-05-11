/**
 * Agent 2: リード情報取得エージェント
 *
 * 目的: メール本文から企業情報・ニーズを自動抽出し、CRM システムに登録
 *
 * 機能:
 * 1. メール本文から企業情報を自動抽出（正規表現・キーワード検索）
 * 2. 抽出情報を構造化データとして Google Sheets に登録
 * 3. 重複検知（同一企業の複数メール対応）
 * 4. 企業規模・業種・ニーズを分類
 */

const CRM_SHEET_NAME = "CRM-Master";
const LEAD_EXTRACTION_SHEET = "Lead-Extraction-Log";

// ========== リード情報抽出メイン関数 ==========
function extractAndRegisterLeads() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const agentLogSheet = spreadsheet.getSheetByName("Agent-Log");
    const crmSheet = spreadsheet.getSheetByName(CRM_SHEET_NAME);

    if (!agentLogSheet || !crmSheet) {
      throw new Error("必須シートが見つかりません");
    }

    const logData = agentLogSheet.getDataRange().getValues();
    const extractionSheet = spreadsheet.getSheetByName(LEAD_EXTRACTION_SHEET) ||
                           spreadsheet.insertSheet(LEAD_EXTRACTION_SHEET);

    // ヘッダー行作成
    if (extractionSheet.getLastRow() === 0) {
      createExtractionSheetHeader(extractionSheet);
    }

    // ログデータを処理（ヘッダーを除く）
    for (let i = 1; i < logData.length; i++) {
      const row = logData[i];
      const emailBody = row[7] || ""; // 本文がここにあると仮定
      const sender = row[2]; // 送信者メール

      const leadInfo = extractLeadInfo(emailBody, sender);
      const classification = classifyNeed(emailBody);

      // 重複チェック
      if (!isDuplicateLead(crmSheet, leadInfo.email, leadInfo.company)) {
        registerLead(crmSheet, leadInfo, classification);
        logExtraction(extractionSheet, leadInfo, classification, "成功");
      } else {
        logExtraction(extractionSheet, leadInfo, classification, "重複");
      }
    }

  } catch (error) {
    logError(`extractAndRegisterLeads: ${error.toString()}`);
  }
}

// ========== 企業情報抽出ロジック ==========
function extractLeadInfo(emailBody, senderEmail) {
  const patterns = {
    companyName: [
      /(?:会社名|企業名|弊社|貴社|当社|当団体)[\s：:]*([^\n]*)/i,
      /^([A-Z][a-zA-Z0-9\s\(\)]+?)(?:の|で|にて|です)/m,
    ],
    employeeCount: [
      /(?:従業員数|スタッフ数|従業員)[\s：:]*約?(\d+)/,
      /(\d+)名の企業/,
      /(\d{2,})人規模/
    ],
    phone: [
      /(?:電話|TEL|Phone)[\s：:]*(\d{2,4}-\d{2,4}-\d{4})/,
      /(\d{3}-\d{4}-\d{4})/
    ],
    department: [
      /(?:部門|部|課|チーム|事業部)[\s：:]*(.*?)(?:です|ございます|で|に)/i
    ],
    businessType: [
      /(?:業種|業態|事業内容)[\s：:]*(.*?)(?:です|ございます|で|に)/i
    ]
  };

  const leadInfo = {
    email: senderEmail,
    company: "",
    employees: "",
    phone: "",
    department: "",
    businessType: "",
    extractionScore: 0
  };

  // パターンマッチング（複数パターンから最初に合致したものを採用）
  const tryMatch = (patterns, email) => {
    for (const pattern of patterns) {
      const match = email.match(pattern);
      if (match) return match[1].trim();
    }
    return "";
  };

  leadInfo.company = tryMatch(patterns.companyName, emailBody) || extractCompanyFromEmail(senderEmail);
  leadInfo.employees = tryMatch(patterns.employeeCount, emailBody);
  leadInfo.phone = tryMatch(patterns.phone, emailBody);
  leadInfo.department = tryMatch(patterns.department, emailBody);
  leadInfo.businessType = tryMatch(patterns.businessType, emailBody);

  // 抽出スコア計算（抽出できた項目数）
  leadInfo.extractionScore = [
    leadInfo.company,
    leadInfo.employees,
    leadInfo.phone,
    leadInfo.department,
    leadInfo.businessType
  ].filter(v => v).length;

  return leadInfo;
}

// ========== メールアドレスから企業情報推測 ==========
function extractCompanyFromEmail(email) {
  const parts = email.split('@');
  if (parts.length === 2) {
    const domain = parts[1].replace('.co.jp', '').replace('.com', '').replace('.jp', '');
    return domain.charAt(0).toUpperCase() + domain.slice(1);
  }
  return "";
}

// ========== ニーズ分類 ==========
function classifyNeed(emailBody) {
  const needKeywords = {
    "自動化": /自動化|オートメーション|RPA/i,
    "効率化": /効率|改善|最適化|削減/i,
    "コスト削減": /コスト|経費|削減|節約/i,
    "品質向上": /品質|精度|改善|向上/i,
    "人手不足対応": /人手不足|採用困難|スタッフ不足/i,
    "デジタル化": /デジタル|DX|オンライン化/i
  };

  const classification = {
    primaryNeed: "",
    secondaryNeeds: [],
    keywordsMatched: []
  };

  let maxMatches = 0;

  Object.entries(needKeywords).forEach(([needType, pattern]) => {
    const matches = (emailBody.match(pattern) || []).length;
    if (matches > 0) {
      classification.keywordsMatched.push(needType);
      if (matches > maxMatches) {
        classification.primaryNeed = needType;
        maxMatches = matches;
      } else if (matches >= 1) {
        classification.secondaryNeeds.push(needType);
      }
    }
  });

  return classification;
}

// ========== 重複チェック ==========
function isDuplicateLead(crmSheet, email, companyName) {
  const data = crmSheet.getDataRange().getValues();

  // メールアドレス完全一致チェック
  for (let i = 1; i < data.length; i++) {
    if (data[i][2] === email) {
      return true; // 重複あり
    }
  }

  // 企業名 + ドメイン一致チェック
  if (companyName) {
    const domain = email.split('@')[1];
    for (let i = 1; i < data.length; i++) {
      const existingEmail = data[i][2];
      const existingCompany = data[i][1];
      if (existingEmail.split('@')[1] === domain && existingCompany === companyName) {
        return true; // 重複あり
      }
    }
  }

  return false; // 重複なし
}

// ========== リード登録 ==========
function registerLead(crmSheet, leadInfo, classification) {
  const nextId = crmSheet.getLastRow();

  crmSheet.appendRow([
    nextId,
    leadInfo.company,
    leadInfo.email,
    leadInfo.employees,
    leadInfo.phone,
    leadInfo.department,
    "新規",
    "中", // デフォルト関心度
    new Date(),
    new Date(),
    classification.primaryNeed,
    classification.secondaryNeeds.join(", "),
    leadInfo.extractionScore
  ]);
}

// ========== 抽出ログ記録 ==========
function logExtraction(sheet, leadInfo, classification, status) {
  if (sheet.getLastRow() === 0) {
    createExtractionSheetHeader(sheet);
  }

  sheet.appendRow([
    new Date(),
    leadInfo.email,
    leadInfo.company,
    leadInfo.employees,
    leadInfo.phone,
    leadInfo.department,
    leadInfo.businessType,
    classification.primaryNeed,
    classification.secondaryNeeds.join(", "),
    leadInfo.extractionScore,
    status
  ]);
}

// ========== ヘッダー行作成 ==========
function createExtractionSheetHeader(sheet) {
  sheet.appendRow([
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
  ]);
}

// ========== エラーログ ==========
function logError(message) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const errorSheet = ss.getSheetByName("Error-Log") || ss.insertSheet("Error-Log");

  if (errorSheet.getLastRow() === 0) {
    errorSheet.appendRow(["タイムスタンプ", "エラーメッセージ"]);
  }

  errorSheet.appendRow([new Date(), message]);
  console.error(message);
}
