/**
 * Gmail 自動応答ボット v1.0
 *
 * 目的: 営業メール返信に自動で応答し、ファネル最上流の反応確認と初期顧客分類を行う
 *
 * 機能:
 * 1. "AI受信箱" ラベルの未処理メールを自動検出
 * 2. メール本文から顧客の関心度を判定（高/中/低）
 * 3. 判定に応じた自動応答テンプレートで返信
 * 4. 顧客情報を Google Sheets の CRM に自動登録
 * 5. 関心度・対応状況を Slack に通知
 */

// ========== グローバル設定 ==========
const LABEL_NAME = "AI受信箱";
const SPREADSHEET_ID = "1LKpQwkbzzaQXZAyNGLWfDibbeINsReEdR-7kXMyxDMA";
const SLACK_WEBHOOK_URL = "";

// ========== メイン関数: 定期実行（毎時間） ==========
function checkAndReplyToEmails() {
  try {
    const gmailLabel = GmailApp.getUserLabelByName(LABEL_NAME);
    if (!gmailLabel) {
      logError("ラベル 'AI受信箱' が見つかりません。先に作成してください。");
      return;
    }

    const threads = GmailApp.search(`label:AI受信箱 is:unread`, 0, 50);
    const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    const logSheet = ss.getSheetByName("対応ログ") || ss.insertSheet("対応ログ");
    const crmSheet = ss.getSheetByName("顧客管理") || ss.insertSheet("顧客管理");

    let processedCount = 0;

    threads.forEach((thread) => {
      const messages = thread.getMessages();
      const latestMsg = messages[messages.length - 1];
      const sender = latestMsg.getFrom();
      const subject = thread.getFirstMessageSubject();
      const body = latestMsg.getPlainBody();

      // 既に応答済みかチェック
      if (thread.hasLabel(GmailApp.getUserLabelByName("応答済み"))) {
        return;
      }

      // 関心度判定
      const interestLevel = classifyInterest(body);

      // メール本文から企業情報抽出
      const leadInfo = extractLeadInfo(body, sender);

      // テンプレートから応答メール生成
      const responseTemplate = getTemplateByLevel(interestLevel);

      // 自動応答メール送信
      if (responseTemplate) {
        try {
          latestMsg.reply(responseTemplate, {
            from: Session.getActiveUser().getEmail(),
            name: "AI Support Team"
          });

          // ラベル付け（応答済みマーク）
          const respondedLabel = GmailApp.getUserLabelByName("応答済み") ||
                                 GmailApp.createLabel("応答済み");
          thread.addLabel(respondedLabel);
          thread.removeLabel(gmailLabel);

          processedCount++;
        } catch (e) {
          logError(`メール送信失敗: ${sender} - ${e.toString()}`);
        }
      }

      // Spreadsheet に記録
      logToSheet(logSheet, {
        timestamp: new Date(),
        subject: subject,
        from: sender,
        interest: interestLevel,
        status: "応答済み",
        leadInfo: leadInfo
      });

      // CRM に登録
      registerToCRM(crmSheet, leadInfo, interestLevel);

      // Slack に通知
      notifyToSlack(interestLevel, sender, subject);
    });

    // 処理結果をログに記録
    PropertiesService.getUserProperties().setProperty(
      'LAST_RUN_TIME',
      new Date().toString()
    );

  } catch (error) {
    logError(`checkAndReplyToEmails エラー: ${error.toString()}`);
  }
}

// ========== 関心度判定関数 ==========
function classifyInterest(emailBody) {
  const bodyLower = emailBody.toLowerCase();

  // 関心度: 高
  if (/具体的な質問|ユースケース|相談したい|提案を希望|見積もり希望|導入検討/.test(bodyLower)) {
    return "高";
  }

  // 関心度: 中
  if (/ご関心|問い合わせ|詳細を知りたい|情報がほしい|よろしくお願い/.test(bodyLower)) {
    return "中";
  }

  // 関心度: 低
  return "低";
}

// ========== メール本文から企業情報抽出 ==========
function extractLeadInfo(emailBody, senderEmail) {
  const patterns = {
    companyName: /(?:貴社|弊社|当社|当団体)は(.+?)(?:[でに]|の)/,
    employeeCount: /(?:従業員数|スタッフ数)は?約?(\d+)/,
    phone: /(?:電話|TEL|Phone)[\s：:]*(\d{2,4}-\d{2,4}-\d{4})/,
    department: /(?:部門|部|課|チーム)[\s：:]*(.*?)(?:です|ございます|です。)/
  };

  const leadInfo = {
    email: senderEmail,
    company: "",
    employees: "",
    phone: "",
    department: "",
    extractedAt: new Date()
  };

  // パターンマッチング
  const companyMatch = emailBody.match(patterns.companyName);
  if (companyMatch) {
    leadInfo.company = companyMatch[1].trim();
  }

  const employeeMatch = emailBody.match(patterns.employeeCount);
  if (employeeMatch) {
    leadInfo.employees = employeeMatch[1];
  }

  const phoneMatch = emailBody.match(patterns.phone);
  if (phoneMatch) {
    leadInfo.phone = phoneMatch[1];
  }

  const deptMatch = emailBody.match(patterns.department);
  if (deptMatch) {
    leadInfo.department = deptMatch[1].trim();
  }

  return leadInfo;
}

// ========== テンプレート取得 ==========
function getTemplateByLevel(level) {
  const templates = {
    "高": `お疲れ様です。

ご関心ありがとうございます。具体的なご要望をお聞きいただき、心強いです。

より詳細な提案をさせていただくため、15分の無料相談をご提案させていただきたいのですが、
ご都合のつく日時はありますでしょうか？

以下のリンクからご予約いただけます：
https://calendly.com/takada-makoto/consultation

よろしくお願いいたします。

誠一
Takada Makoto`,

    "中": `お疲れ様です。

ご問い合わせありがとうございます。

弊社の取り組みについて、より詳しくご説明させていただきたく、
初回相談をお勧めいたします。

以下のリンクからご予約ください（無料・30分程度）：
https://calendly.com/takada-makoto/consultation

ご不明な点があればお気軽にお問い合わせください。

誠一
Takada Makoto`,

    "低": `お疲れ様です。

この度は情報請求いただき、ありがとうございます。

詳細な資料をお送りいたします。
ご不明な点やご質問があれば、いつでもお気軽にお問い合わせください。

今後ともよろしくお願いいたします。

誠一
Takada Makoto`
  };

  return templates[level] || templates["中"];
}

// ========== Spreadsheet にログ記録 ==========
function logToSheet(sheet, logData) {
  // ヘッダー行がない場合は作成
  if (sheet.getLastRow() === 0) {
    sheet.appendRow([
      "タイムスタンプ",
      "件名",
      "送信者",
      "関心度",
      "対応状況",
      "企業名",
      "従業員数",
      "電話番号",
      "部門"
    ]);
  }

  sheet.appendRow([
    logData.timestamp,
    logData.subject,
    logData.from,
    logData.interest,
    logData.status,
    logData.leadInfo.company || "",
    logData.leadInfo.employees || "",
    logData.leadInfo.phone || "",
    logData.leadInfo.department || ""
  ]);
}

// ========== CRM に顧客情報登録 ==========
function registerToCRM(crmSheet, leadInfo, interestLevel) {
  // ヘッダー行がない場合は作成
  if (crmSheet.getLastRow() === 0) {
    crmSheet.appendRow([
      "顧客ID",
      "企業名",
      "代表メール",
      "従業員数",
      "電話番号",
      "部門",
      "ステータス",
      "関心度",
      "初回接触日",
      "最終更新日"
    ]);
  }

  // 重複チェック（同一メールアドレスが存在するか）
  const data = crmSheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][2] === leadInfo.email) {
      // 既存顧客：ステータスのみ更新
      crmSheet.getRange(i + 1, 8).setValue(interestLevel); // 関心度更新
      crmSheet.getRange(i + 1, 10).setValue(new Date()); // 最終更新日
      return;
    }
  }

  // 新規顧客：登録
  const nextId = (crmSheet.getLastRow()) + 1;
  crmSheet.appendRow([
    nextId,
    leadInfo.company || "（未抽出）",
    leadInfo.email,
    leadInfo.employees || "",
    leadInfo.phone || "",
    leadInfo.department || "",
    "新規",
    interestLevel,
    new Date(),
    new Date()
  ]);
}

// ========== Slack 通知 ==========
function notifyToSlack(interestLevel, sender, subject) {
  if (!SLACK_WEBHOOK_URL) {
    return; // Slack URL が未設定の場合はスキップ
  }

  const colors = {
    "高": "#FF6B6B",  // 赤
    "中": "#FFA500",  // オレンジ
    "低": "#808080"   // グレー
  };

  const payload = {
    attachments: [
      {
        color: colors[interestLevel] || "#808080",
        title: `新規メール受信 [関心度: ${interestLevel}]`,
        text: `*件名:* ${subject}\n*送信者:* ${sender}`,
        ts: Math.floor(Date.now() / 1000)
      }
    ]
  };

  try {
    UrlFetchApp.fetch(SLACK_WEBHOOK_URL, {
      method: "post",
      payload: JSON.stringify(payload),
      headers: { "Content-Type": "application/json" }
    });
  } catch (e) {
    logError(`Slack 通知失敗: ${e.toString()}`);
  }
}

// ========== エラーログ関数 ==========
function logError(message) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const errorSheet = ss.getSheetByName("エラーログ") || ss.insertSheet("エラーログ");

  if (errorSheet.getLastRow() === 0) {
    errorSheet.appendRow(["タイムスタンプ", "エラーメッセージ"]);
  }

  errorSheet.appendRow([new Date(), message]);

  // コンソールにも出力
  console.error(message);
}

// ========== トリガー設定（実行後、手動で設定） ==========
// Google Apps Script エディタ → トリガー → 新規トリガー
// 関数: checkAndReplyToEmails
// デプロイ: 新しいデプロイ
// イベントソース: 時間主導型
// イベント種類: 時間ベース → 1時間ごと
// エラー通知: メールで通知
