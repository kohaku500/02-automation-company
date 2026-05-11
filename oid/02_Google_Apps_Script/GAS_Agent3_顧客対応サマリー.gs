/**
 * Agent 3: 顧客対応サマリーエージェント
 *
 * 目的: メール・チャット・通話記録から重要な内容を自動抽出・サマリー
 *
 * 機能:
 * 1. Gmail のメール会話を自動集約
 * 2. キーワード抽出（決定キーワード、懸念事項など）
 * 3. 営業担当者向けの「今日のアクション」を自動生成
 * 4. 週次進捗レポート自動作成
 */

const CRM_SHEET_NAME = "CRM-Master";
const SUMMARY_SHEET_NAME = "Conversation-Summary";
const ACTION_SHEET_NAME = "Daily-Actions";

// ========== サマリー生成メイン関数 ==========
function generateConversationSummaries() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const crmSheet = spreadsheet.getSheetByName(CRM_SHEET_NAME);
    const summarySheet = spreadsheet.getSheetByName(SUMMARY_SHEET_NAME) ||
                        spreadsheet.insertSheet(SUMMARY_SHEET_NAME);
    const actionSheet = spreadsheet.getSheetByName(ACTION_SHEET_NAME) ||
                       spreadsheet.insertSheet(ACTION_SHEET_NAME);

    if (!crmSheet) {
      throw new Error("CRM-Master シートが見つかりません");
    }

    // ヘッダー行作成
    if (summarySheet.getLastRow() === 0) {
      createSummarySheetHeader(summarySheet);
    }

    if (actionSheet.getLastRow() === 0) {
      createActionSheetHeader(actionSheet);
    }

    // Gmail メールを検索（Customer-Conversation ラベル）
    const label = GmailApp.getUserLabelByName("Customer-Conversation");
    if (!label) {
      console.log("'Customer-Conversation' ラベルが見つかりません。スキップします。");
      return;
    }

    const threads = label.getThreads(0, 50);

    threads.forEach((thread) => {
      const customerId = extractCustomerId(thread);
      const summary = generateThreadSummary(thread);
      const actions = extractActions(summary);

      // サマリーを登録
      registerSummary(summarySheet, customerId, summary);

      // アクションを登録
      registerActions(actionSheet, customerId, actions);

      // CRM ステータス更新
      updateCRMStatus(crmSheet, customerId, summary);
    });

  } catch (error) {
    logError(`generateConversationSummaries: ${error.toString()}`);
  }
}

// ========== スレッドサマリー生成 ==========
function generateThreadSummary(thread) {
  const messages = thread.getMessages();
  const summary = {
    threadId: thread.getId(),
    subject: thread.getFirstMessageSubject(),
    messageCount: messages.length,
    conversation: [],
    keywordsBag: [],
    decisionKeywords: [],
    concerns: [],
    nextStep: "",
    priority: "低",
    lastUpdate: new Date()
  };

  messages.forEach((msg) => {
    summary.conversation.push({
      date: msg.getDate(),
      from: msg.getFrom(),
      body: msg.getPlainBody().substring(0, 200) // 最初の200文字
    });
  });

  // 最終メール本文から重要キーワード抽出
  const latestBody = messages[messages.length - 1].getPlainBody();
  const keywordResult = extractKeywords(latestBody);

  summary.keywordsBag = keywordResult.keywords;
  summary.decisionKeywords = keywordResult.decisionKeywords;
  summary.concerns = keywordResult.concerns;
  summary.priority = calculatePriority(keywordResult);
  summary.nextStep = generateNextStep(keywordResult);

  return summary;
}

// ========== キーワード抽出ロジック ==========
function extractKeywords(emailBody) {
  const extractionRules = {
    decisionKeywords: [
      { pattern: /導入決定|契約予定|契約確定|契約締結/, priority: "🔴 高" },
      { pattern: /見積書希望|見積を送付|提案書作成/, priority: "🟠 中" },
      { pattern: /デモンストレーション|実装予定/, priority: "🟠 中" }
    ],
    concerns: [
      /懸念|問題|課題|困っている|不安/i,
      /他社比較|検討中|迷っている/i,
      /価格が高い|予算が|費用が/i
    ],
    positiveIndicators: [
      /期待|素晴らしい|良さそう|導入したい/i,
      /ぜひ|お願いします|契約したい/i
    ]
  };

  const result = {
    keywords: [],
    decisionKeywords: [],
    concerns: [],
    positiveCount: 0
  };

  // 決定キーワード抽出
  extractionRules.decisionKeywords.forEach(({ pattern, priority }) => {
    if (pattern.test(emailBody)) {
      result.decisionKeywords.push({
        keyword: pattern.source.substring(0, 20),
        priority: priority
      });
    }
  });

  // 懸念事項抽出
  extractionRules.concerns.forEach((pattern) => {
    const matches = emailBody.match(pattern);
    if (matches) {
      result.concerns.push(matches[0]);
    }
  });

  // 好意的インジケータ
  extractionRules.positiveIndicators.forEach((pattern) => {
    if (pattern.test(emailBody)) {
      result.positiveCount++;
    }
  });

  result.keywords = [
    ...result.decisionKeywords.map(dk => dk.keyword),
    ...result.concerns.slice(0, 3)
  ];

  return result;
}

// ========== 優先度計算 ==========
function calculatePriority(keywordResult) {
  if (keywordResult.decisionKeywords.length > 0) {
    return "🔴 高"; // 決定キーワード発見
  }
  if (keywordResult.concerns.length > 0) {
    return "🟠 中"; // 懸念事項あり
  }
  if (keywordResult.positiveCount >= 2) {
    return "🟡 低"; // 好意的だが決定なし
  }
  return "⚪ 低";
}

// ========== 次のステップ自動生成 ==========
function generateNextStep(keywordResult) {
  if (keywordResult.decisionKeywords.length > 0) {
    return "【即対応】契約フロー開始 / 提案資料最終版作成";
  }
  if (keywordResult.concerns.length > 0) {
    return "【24時間内】懸念事項に対する回答メール送付";
  }
  if (keywordResult.positiveCount >= 1) {
    return "【48時間内】デモンストレーションまたは提案書送付";
  }
  return "【標準】3日以内にフォローアップメール送付";
}

// ========== アクション抽出 ==========
function extractActions(summary) {
  const actions = [];

  summary.decisionKeywords.forEach((keyword) => {
    actions.push({
      type: "CONTRACT",
      description: "契約手続き開始",
      deadline: addDays(new Date(), 1),
      priority: "高"
    });
  });

  summary.concerns.forEach((concern) => {
    actions.push({
      type: "RESPOND",
      description: `懸念事項への回答: "${concern}"`,
      deadline: addDays(new Date(), 1),
      priority: "高"
    });
  });

  if (summary.messageCount < 3) {
    actions.push({
      type: "FOLLOWUP",
      description: "初回フォローアップメール",
      deadline: addDays(new Date(), 2),
      priority: "中"
    });
  }

  return actions;
}

// ========== サマリー登録 ==========
function registerSummary(sheet, customerId, summary) {
  // 重複チェック（同一 threadId で最新のサマリーのみ保持）
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][1] === summary.threadId) {
      // 既存行を更新
      sheet.getRange(i + 1, 3).setValue(summary.messageCount);
      sheet.getRange(i + 1, 5).setValue(summary.keywordsBag.join(", "));
      sheet.getRange(i + 1, 6).setValue(summary.priority);
      sheet.getRange(i + 1, 7).setValue(summary.nextStep);
      sheet.getRange(i + 1, 8).setValue(summary.lastUpdate);
      return;
    }
  }

  // 新規登録
  sheet.appendRow([
    new Date(),
    summary.threadId,
    summary.messageCount,
    summary.subject,
    summary.keywordsBag.join(", "),
    summary.priority,
    summary.nextStep,
    summary.lastUpdate
  ]);
}

// ========== アクション登録 ==========
function registerActions(sheet, customerId, actions) {
  actions.forEach((action) => {
    sheet.appendRow([
      new Date(),
      customerId || "不明",
      action.type,
      action.description,
      action.deadline,
      action.priority,
      "未実施"
    ]);
  });
}

// ========== CRM ステータス更新 ==========
function updateCRMStatus(crmSheet, customerId, summary) {
  if (!customerId) return;

  const data = crmSheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] == customerId) {
      // ステータス更新
      if (summary.decisionKeywords.length > 0) {
        crmSheet.getRange(i + 1, 7).setValue("提案待ち");
      } else if (summary.priority === "🟠 中") {
        crmSheet.getRange(i + 1, 7).setValue("検討中");
      }
      crmSheet.getRange(i + 1, 10).setValue(new Date());
      return;
    }
  }
}

// ========== ヘッダー作成 ==========
function createSummarySheetHeader(sheet) {
  sheet.appendRow([
    "生成タイムスタンプ",
    "スレッドID",
    "メール数",
    "件名",
    "抽出キーワード",
    "優先度",
    "次のステップ",
    "最終更新"
  ]);
}

function createActionSheetHeader(sheet) {
  sheet.appendRow([
    "作成日",
    "顧客ID",
    "アクション種類",
    "説明",
    "期限",
    "優先度",
    "実施状況"
  ]);
}

// ========== カスタマーID抽出 ==========
function extractCustomerId(thread) {
  // スレッドのメール送信者から顧客ID を推測
  const messages = thread.getMessages();
  const firstFrom = messages[0].getFrom();
  return firstFrom.split('@')[0]; // 仮の実装
}

// ========== ユーティリティ ==========
function addDays(date, days) {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function logError(message) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const errorSheet = ss.getSheetByName("Error-Log") || ss.insertSheet("Error-Log");

  if (errorSheet.getLastRow() === 0) {
    errorSheet.appendRow(["タイムスタンプ", "エラーメッセージ"]);
  }

  errorSheet.appendRow([new Date(), message]);
  console.error(message);
}
