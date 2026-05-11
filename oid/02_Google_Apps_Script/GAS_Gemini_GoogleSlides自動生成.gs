/**
 * Gemini API + Google Slides 自動生成スクリプト
 * プレゼン資料を自動作成するメインコード
 */

// ==================== 設定 ====================
const GEMINI_API_KEY = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
const GEMINI_MODEL = 'gemini-2.5-pro';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/' + GEMINI_MODEL + ':generateContent';

// ==================== メイン実行関数 ====================

/**
 * プレゼン資料を Gemini で生成して Google Slides に作成
 * @param {string} title - プレゼンテーションのタイトル
 * @param {string} description - プレゼン内容の説明
 */
function createPresentationWithGemini(title = 'AI Agent自動運営プロジェクト', description = '月間MRR ¥1M+ の自動化収益システム構築') {
  Logger.log('🚀 Gemini プレゼン資料生成開始...');

  try {
    // Step 1: Gemini に JSON を生成させる
    Logger.log('【Step 1】Gemini API に プレゼン構成リクエスト...');
    const slideJson = generateSlideJsonFromGemini(title, description);

    if (!slideJson) {
      Logger.log('❌ Gemini からのレスポンスが取得できません');
      return;
    }

    Logger.log('✅ Gemini からプレゼン構成取得完了');
    Logger.log('JSON: ' + JSON.stringify(slideJson).substring(0, 200) + '...');

    // Step 2: Google Slides を作成
    Logger.log('【Step 2】Google Slides を作成中...');
    const presentationId = createGoogleSlides(title);

    if (!presentationId) {
      Logger.log('❌ Google Slides の作成に失敗しました');
      return;
    }

    Logger.log('✅ Google Slides 作成完了 (ID: ' + presentationId + ')');

    // Step 3: スライドを追加
    Logger.log('【Step 3】スライドコンテンツを配置中...');
    addSlidesToPresentation(presentationId, slideJson);

    Logger.log('✅ 全スライド配置完了');

    // Step 4: リンク表示
    const url = 'https://docs.google.com/presentation/d/' + presentationId + '/edit';
    Logger.log('');
    Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    Logger.log('✅ プレゼン資料が完成しました！');
    Logger.log('リンク: ' + url);
    Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  } catch (error) {
    Logger.log('❌ エラー: ' + error.toString());
  }
}

// ==================== Gemini API 連携 ====================

/**
 * Gemini API を呼び出してプレゼン構成を JSON で取得
 */
function generateSlideJsonFromGemini(title, description) {
  const prompt = `あなたは優秀なビジネスコンサルタントです。以下のプレゼンテーション資料を、JSON形式で15スライド分生成してください。

【プレゼンテーション情報】
タイトル: ${title}
説明: ${description}

【必須要件】
- 15スライド分の構成を作成
- 各スライドは以下の形式で JSON 配列として返す:
  {
    "slide_number": 1,
    "title": "スライドタイトル",
    "subtitle": "サブタイトル（オプション）",
    "content": ["要点1", "要点2", "要点3"]
  }

【スライド構成】
1. タイトルスライド
2. プロジェクト概要
3. 問題点と解決策
4. ビジネスモデル
5. Day 1 収益シミュレーション
6. 成長推移
7. 6ヶ月売上推移
8. 投資対効果
9. Day 1 プロセスフロー
10. AI Agent 3つの役割
11. リスク評価と対策
12. KPI ダッシュボード
13. 実行ロードマップ
14. 成功指標
15. 結論とアクション

【重要】
- JSON 配列のみを返す。説明文は付けない。
- 各スライドの content は配列形式で、要点を3～5個記載。
- 日本語で作成。
- JSON が有効な形式であることを確認。`;

  const payload = {
    contents: [{
      parts: [{
        text: prompt
      }]
    }]
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(GEMINI_API_URL + '?key=' + GEMINI_API_KEY, options);
    const result = JSON.parse(response.getContentText());

    if (result.candidates && result.candidates[0]) {
      const text = result.candidates[0].content.parts[0].text;

      // JSON を抽出（markdown コード記号を削除）
      const jsonMatch = text.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
    }

    Logger.log('⚠️ Gemini からの予期しない応答: ' + response.getContentText().substring(0, 200));
    return null;

  } catch (error) {
    Logger.log('❌ Gemini API エラー: ' + error.toString());
    return null;
  }
}

// ==================== Google Slides 操作 ====================

/**
 * Google Slides プレゼンテーションを作成
 */
function createGoogleSlides(title) {
  try {
    const presentation = SlidesApp.create(title);
    const presentationId = presentation.getId();

    // デフォルトスライドを削除
    const slides = presentation.getSlides();
    if (slides.length > 0) {
      slides[0].remove();
    }

    return presentationId;
  } catch (error) {
    Logger.log('❌ Google Slides 作成エラー: ' + error.toString());
    return null;
  }
}

/**
 * JSON データに基づいてスライドを追加
 */
function addSlidesToPresentation(presentationId, slideJsonArray) {
  try {
    const presentation = SlidesApp.openById(presentationId);

    slideJsonArray.forEach((slideData, index) => {
      Logger.log('スライド ' + (index + 1) + ' を作成中...');

      // スライドレイアウトを選択
      const layout = index === 0
        ? SlidesApp.PredefinedLayout.TITLE_SLIDE
        : SlidesApp.PredefinedLayout.TITLE_AND_BODY;

      const slide = presentation.appendSlide(layout);

      // タイトルを設定
      const titleShape = slide.getPlaceholder(SlidesApp.PlaceholderType.TITLE);
      if (titleShape) {
        titleShape.asShape().getText().clear().appendText(slideData.title);
      }

      // 本文を設定
      const bodyShape = slide.getPlaceholder(SlidesApp.PlaceholderType.BODY);
      if (bodyShape) {
        const textRange = bodyShape.asShape().getText();
        textRange.clear();

        // サブタイトルがあれば追加
        if (slideData.subtitle) {
          textRange.appendText(slideData.subtitle);
          textRange.appendText('\n\n');
        }

        // コンテンツ（要点）を箇条書きで追加
        if (slideData.content && slideData.content.length > 0) {
          slideData.content.forEach((point, i) => {
            textRange.appendText(point);
            if (i < slideData.content.length - 1) {
              textRange.appendText('\n');
            }
          });
        }
      }
    });

    Logger.log('✅ 全 ' + slideJsonArray.length + ' スライドを作成完了');

  } catch (error) {
    Logger.log('❌ スライド追加エラー: ' + error.toString());
  }
}

// ==================== ヘルパー関数 ====================

/**
 * Gemini API キーを設定
 * 実行前に必ず呼び出す
 */
function setGeminiApiKey(apiKey) {
  PropertiesService.getScriptProperties().setProperty('GEMINI_API_KEY', apiKey);
  Logger.log('✅ Gemini API キーを設定しました');
}

/**
 * API キーを確認
 */
function checkApiKey() {
  const key = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  if (key) {
    Logger.log('✅ Gemini API キーが設定されています');
    Logger.log('キー（最後の10文字）: ' + key.substring(key.length - 10));
  } else {
    Logger.log('❌ Gemini API キーが設定されていません');
    Logger.log('以下を実行してください: setGeminiApiKey("あなたのAPIキー")');
  }
}

/**
 * テスト実行
 */
function testPresentationGeneration() {
  Logger.log('🧪 テスト実行を開始します...');

  // API キーをチェック
  checkApiKey();

  // プレゼン生成
  createPresentationWithGemini(
    'AI Agent自動運営プロジェクト',
    '月間MRR ¥1M+ の自動化収益システム構築'
  );
}
