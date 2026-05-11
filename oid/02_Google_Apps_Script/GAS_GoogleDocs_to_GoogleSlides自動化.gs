/**
 * Google Docs → Google Slides 自動変換
 * Google Docs のプレゼン資料を自動的に Google Slides に変換
 */

// 設定
const DOC_ID = "1eh-IIAigdvkyUCIB_Ml3szjTY_YtQqbT2lBnak32kgs"; // 既存の Google Docs
const SLIDES_ID = "1hBbEK73gr2WUpvXZNczILcufyaYlsBCaSNZN9sdA4D4"; // 新規 Google Slides

/**
 * メイン実行関数
 */
function convertDocsToSlides() {
  Logger.log('🚀 Google Docs → Google Slides 変換開始...');

  try {
    // Step 1: Google Docs の内容を取得
    Logger.log('【Step 1】Google Docs を読み込み中...');
    const slides = extractSlidesFromDocs();

    if (!slides || slides.length === 0) {
      Logger.log('❌ スライド情報が抽出できません');
      return;
    }

    Logger.log('✅ ' + slides.length + ' スライド分のコンテンツを抽出');

    // Step 2: Google Slides にコンテンツを追加
    Logger.log('【Step 2】Google Slides を作成中...');
    addSlidesToPresentation(slides);

    Logger.log('✅ Google Slides への追加完了');

    // Step 3: 完成
    const url = 'https://docs.google.com/presentation/d/' + SLIDES_ID + '/edit';
    Logger.log('');
    Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    Logger.log('✅ 変換完了！');
    Logger.log('Google Slides: ' + url);
    Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  } catch (error) {
    Logger.log('❌ エラー: ' + error.toString());
  }
}

/**
 * Google Docs から【スライド X】の形式でスライドを抽出
 */
function extractSlidesFromDocs() {
  try {
    const doc = DocumentApp.openById(DOC_ID);
    const body = doc.getBody();
    const text = body.getText();

    // 【スライド 1】【スライド 2】...で分割
    const slidePattern = /【スライド \d+】([^【]*?)(?=【スライド \d+】|$)/gs;
    const matches = text.matchAll(slidePattern);

    const slides = [];

    for (const match of matches) {
      const slideContent = match[1].trim();

      if (slideContent) {
        // タイトルと本文に分割
        const lines = slideContent.split('\n').filter(line => line.trim());

        if (lines.length > 0) {
          const title = lines[0].trim();
          const content = lines.slice(1)
            .map(line => line.trim())
            .filter(line => line && line !== '━'.repeat(50))
            .join('\n');

          slides.push({
            title: title,
            content: content
          });
        }
      }
    }

    return slides;

  } catch (error) {
    Logger.log('❌ Docs 読み込みエラー: ' + error.toString());
    return null;
  }
}

/**
 * Google Slides にスライドを追加
 */
function addSlidesToPresentation(slides) {
  try {
    const presentation = SlidesApp.openById(SLIDES_ID);

    // デフォルトスライドを削除
    const defaultSlides = presentation.getSlides();
    if (defaultSlides.length > 0) {
      defaultSlides.forEach(slide => slide.remove());
    }

    // 各スライドを追加
    slides.forEach((slideData, index) => {
      Logger.log('スライド ' + (index + 1) + ' を作成中...');

      try {
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

          if (slideData.content) {
            textRange.appendText(slideData.content);
          }
        }

        Logger.log('✅ スライド ' + (index + 1) + ' 作成完了');

      } catch (slideError) {
        Logger.log('⚠️ スライド ' + (index + 1) + ' で警告: ' + slideError.toString());
      }
    });

  } catch (error) {
    Logger.log('❌ Slides 追加エラー: ' + error.toString());
    throw error;
  }
}

/**
 * テスト実行用関数
 */
function testConversion() {
  Logger.log('🧪 テスト実行開始...');
  convertDocsToSlides();
}

/**
 * デバッグ：抽出されたスライドを確認
 */
function debugExtractSlides() {
  const slides = extractSlidesFromDocs();

  Logger.log('抽出されたスライド数: ' + (slides ? slides.length : 0));

  if (slides) {
    slides.forEach((slide, index) => {
      Logger.log('');
      Logger.log('【スライド ' + (index + 1) + '】');
      Logger.log('タイトル: ' + slide.title);
      Logger.log('本文（最初の100文字）: ' + slide.content.substring(0, 100) + '...');
    });
  }
}
