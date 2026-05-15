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

// ========== プラン設定 ==========
// "basic" : 定型文テンプレートで返信（APIキー不要）
// "ai"    : GeminiがメールをAIが読んで自然な返信を生成
const PLAN = "basic";
const GEMINI_API_KEY = ""; // AIプランの場合はここにAPIキーを入力

// ========== メイン関数: 定期実行（毎時間） ==========
function checkAndReplyToEmails() {
  try {
    const gmailLabel = GmailApp.getUserLabelByName(LABEL_NAME);
    if (!gmailLabel) {
      logError("ラベル 'AI受信箱' が見つかりません。先に作成してください。");
      return;
    }

    const threads = GmailApp.search(`label:AI受信箱 -label:応答済み`, 0, 50);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const logSheet = ss.getSheetByName("対応ログ") || ss.insertSheet("対応ログ");
    const crmSheet = ss.getSheetByName("顧客管理") || ss.insertSheet("顧客管理");

    let processedCount = 0;

    threads.forEach((thread) => {
      const messages = thread.getMessages();
      const latestMsg = messages[messages.length - 1];
      const sender = latestMsg.getFrom();
      const subject = thread.getFirstMessageSubject();
      const body = latestMsg.getPlainBody();

      // 関心度判定
      const interestLevel = classifyInterest(body);

      // メール本文から企業情報抽出
      const leadInfo = extractLeadInfo(body, sender);

      // プランに応じて返信文を生成
      const responseTemplate = PLAN === "ai" && GEMINI_API_KEY
        ? generateAIReply(body, subject, sender)
        : getTemplateByLevel(interestLevel);

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

// ========== AIプラン：Geminiで返信文を生成 ==========
function generateAIReply(body, subject, sender) {
  const { greeting, closing, signature } = getMyStyle();

  const prompt = `あなたはビジネスメールの返信を代行するAI秘書です。
以下のメールに対して、自然で丁寧な返信文を日本語で作成してください。

【受信メール】
件名: ${subject}
送信者: ${sender}
本文:
${body}

【返信のルール】
- 書き出しは必ず「${greeting}」で始める
- 締めは「${closing}」で終える
- 署名は「${signature}」を使う
- 相手の質問や要望に具体的に答える
- 200文字以内で簡潔に
- 丁寧だが堅すぎない文体

返信文のみを出力してください。`;

  try {
    const response = UrlFetchApp.fetch(
      `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
      }
    );
    const result = JSON.parse(response.getContentText());
    return result.candidates[0].content.parts[0].text;
  } catch (e) {
    console.log(`Gemini API エラー。テンプレートで代替: ${e}`);
    return getTemplateByLevel(classifyInterest(body));
  }
}

// ========== 文体学習関数（送信済みメールから抽出） ==========
function learnMyStyle() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const styleSheet = ss.getSheetByName("スタイル設定") || ss.insertSheet("スタイル設定");

  const sentThreads = GmailApp.search('in:sent', 0, 50);
  const myEmail = Session.getActiveUser().getEmail();

  const greetings = {};
  const closings = {};
  const signatures = [];

  sentThreads.forEach(thread => {
    thread.getMessages().forEach(msg => {
      if (msg.getFrom().includes(myEmail)) {
        const lines = msg.getPlainBody().split('\n').map(l => l.trim()).filter(l => l !== '');
        if (lines.length < 2) return;

        // 書き出し（最初の行・30文字以内）
        const g = lines[0];
        if (g.length <= 30) greetings[g] = (greetings[g] || 0) + 1;

        // 締め（後ろから2〜4行目・30文字以内）
        for (let i = Math.max(0, lines.length - 4); i < lines.length - 1; i++) {
          const c = lines[i];
          if (c.length > 3 && c.length <= 30) closings[c] = (closings[c] || 0) + 1;
        }

        // 署名（最後の行）
        signatures.push(lines[lines.length - 1]);
      }
    });
  });

  const topGreeting = Object.entries(greetings).sort((a, b) => b[1] - a[1])[0]?.[0] || 'お疲れ様です。';
  const topClosing  = Object.entries(closings).sort((a, b) => b[1] - a[1])[0]?.[0] || 'よろしくお願いいたします。';
  const topSignature = signatures[0] || '';

  styleSheet.clearContents();
  styleSheet.appendRow(['設定項目', '値']);
  styleSheet.appendRow(['書き出し', topGreeting]);
  styleSheet.appendRow(['締めの言葉', topClosing]);
  styleSheet.appendRow(['署名', topSignature]);

  console.log(`✅ スタイル学習完了`);
  console.log(`書き出し: ${topGreeting}`);
  console.log(`締め: ${topClosing}`);
  console.log(`署名: ${topSignature}`);
}

// ========== スタイル設定を読み込む ==========
function getMyStyle() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const styleSheet = ss.getSheetByName("スタイル設定");
  if (!styleSheet || styleSheet.getLastRow() < 2) {
    return { greeting: 'お疲れ様です。', closing: 'よろしくお願いいたします。', signature: '' };
  }
  const style = { greeting: 'お疲れ様です。', closing: 'よろしくお願いいたします。', signature: '' };
  styleSheet.getDataRange().getValues().slice(1).forEach(row => {
    if (row[0] === '書き出し')  style.greeting  = row[1];
    if (row[0] === '締めの言葉') style.closing   = row[1];
    if (row[0] === '署名')      style.signature = row[1];
  });
  return style;
}

// ========== テンプレート取得 ==========
function getTemplateByLevel(level) {
  const { greeting, closing, signature } = getMyStyle();

  const templates = {
    "高": `${greeting}

ご関心ありがとうございます。具体的なご要望をお聞きいただき、心強いです。

より詳細なご提案をさせていただくため、15分ほどお時間をいただけますでしょうか？
ご都合のつく日時をお知らせください。

${closing}

${signature}`,

    "中": `${greeting}

ご問い合わせありがとうございます。

弊社の取り組みについて、より詳しくご説明させていただきたく存じます。
ご都合のよい日時をお知らせいただけますでしょうか。

${closing}

${signature}`,

    "低": `${greeting}

この度はご連絡いただき、ありがとうございます。

詳細な資料をお送りいたします。
ご不明な点がございましたら、お気軽にお問い合わせください。

${closing}

${signature}`
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
  const ss = SpreadsheetApp.openById("1LKpQwkbzzaQXZAyNGLWfDibbeINsReEdR-7kXMyxDMA");
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
