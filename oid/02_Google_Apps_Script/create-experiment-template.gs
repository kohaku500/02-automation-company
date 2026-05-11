/**
 * 実験記録テンプレート自動生成スクリプト
 *
 * 使い方:
 * 1. Google Apps Script エディタを開く
 * 2. このコードを貼り付け
 * 3. createExperimentTemplate() 関数を実行
 * 4. Google Drive に新しいスプレッドシート「実験記録テンプレート」が作成される
 */

function createExperimentTemplate() {
  try {
    // 新規スプレッドシート作成
    const ss = SpreadsheetApp.create('実験記録テンプレート');
    const sheet = ss.getActiveSheet();
    sheet.setName('実験記録');

    // セルサイズ設定
    sheet.setColumnWidth(1, 180);  // A列
    sheet.setColumnWidth(2, 300);  // B列
    sheet.setColumnWidth(3, 200);  // C列
    for (let i = 4; i <= 10; i++) {
      sheet.setColumnWidth(i, 120);
    }

    // フォント設定
    const range = sheet.getRange('A:Z');
    range.setFontFamily('Noto Sans JP');
    range.setFontSize(11);

    // ========== セクション1: 試験の基本情報 ==========
    const section1Row = 1;
    addSectionHeader(sheet, section1Row, '【セクション1】試験の基本情報', '#1565C0');

    // 記録ID
    sheet.getRange(`A${section1Row + 1}`).setValue('記録ID');
    const idFormula = `=TEXT(NOW(),"YYYYMMDD")&"-"&RANDBETWEEN(1,999)`;
    sheet.getRange(`B${section1Row + 1}`).setFormula(idFormula);
    sheet.getRange(`C${section1Row + 1}`).setValue('自動生成（日時ベース）');
    sheet.getRange(`C${section1Row + 1}`).setFontStyle('italic').setFontColor('#999999');

    // 作成日時
    sheet.getRange(`A${section1Row + 2}`).setValue('作成日時');
    sheet.getRange(`B${section1Row + 2}`).setFormula('=TODAY()');
    sheet.getRange(`C${section1Row + 2}`).setValue('自動記入（今日の日付）');
    sheet.getRange(`C${section1Row + 2}`).setFontStyle('italic').setFontColor('#999999');

    // 試験概要
    const overviewRow = section1Row + 4;
    sheet.getRange(`A${overviewRow}:A${overviewRow + 4}`).mergeVertically();
    sheet.getRange(`A${overviewRow}`).setValue('試験概要');
    sheet.getRange(`B${overviewRow}:B${overviewRow + 4}`).mergeVertically();
    sheet.getRange(`B${overviewRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${overviewRow}`).setValue('この試験の背景・概要を簡潔に説明（100-200字程度）');
    sheet.getRange(`C${overviewRow}`).setValue('ヒント：なぜこの試験をするのか');
    sheet.getRange(`C${overviewRow}`).setFontStyle('italic').setFontColor('#999999');
    sheet.setRowHeight(overviewRow, 80);

    // 試験目的
    const purposeRow = overviewRow + 5;
    sheet.getRange(`A${purposeRow}:A${purposeRow + 4}`).mergeVertically();
    sheet.getRange(`A${purposeRow}`).setValue('試験目的');
    sheet.getRange(`B${purposeRow}:B${purposeRow + 4}`).mergeVertically();
    sheet.getRange(`B${purposeRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${purposeRow}`).setValue('なぜこの試験をするのか、達成目標は何か（100-200字程度）');
    sheet.getRange(`C${purposeRow}`).setValue('ヒント：試験結果で何を確認したいか');
    sheet.getRange(`C${purposeRow}`).setFontStyle('italic').setFontColor('#999999');
    sheet.setRowHeight(purposeRow, 80);

    // ========== セクション2: 試験の実施体制 ==========
    const section2Row = purposeRow + 6;
    addSectionHeader(sheet, section2Row, '【セクション2】試験の実施体制・環境', '#2E7D32');

    // 試験対象品
    const targetRow = section2Row + 1;
    sheet.getRange(`A${targetRow}:A${targetRow + 1}`).mergeVertically();
    sheet.getRange(`A${targetRow}`).setValue('試験対象品');
    sheet.getRange(`B${targetRow}:C${targetRow + 1}`).mergeVertically();
    sheet.getRange(`B${targetRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${targetRow}`).setValue('製品名、型番、シリアル番号などを記載');
    sheet.setRowHeight(targetRow, 50);
    addHintColumn(sheet, targetRow, 'ヒント：何を試験するのか');

    // 試験者
    const operatorRow = targetRow + 2;
    sheet.getRange(`A${operatorRow}`).setValue('試験者');
    sheet.getRange(`B${operatorRow}`).setValue('試験を実施した担当者名（複数可、カンマ区切り）');
    addHintColumn(sheet, operatorRow, 'ヒント：誰が実施したか');

    // 試験場所
    const locationRow = operatorRow + 1;
    sheet.getRange(`A${locationRow}`).setValue('試験場所');
    sheet.getRange(`B${locationRow}`).setValue('試験室名、建屋、エリア');
    addHintColumn(sheet, locationRow, 'ヒント：どこで実施したか');

    // 試験設備・機器
    const equipmentRow = locationRow + 2;
    sheet.getRange(`A${equipmentRow}:A${equipmentRow + 3}`).mergeVertically();
    sheet.getRange(`A${equipmentRow}`).setValue('試験設備・機器');
    sheet.getRange(`B${equipmentRow}:C${equipmentRow + 3}`).mergeVertically();
    sheet.getRange(`B${equipmentRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${equipmentRow}`).setValue('使用した計測機器・装置の詳細。メーカー、型番、精度を記載');
    sheet.setRowHeight(equipmentRow, 80);
    addHintColumn(sheet, equipmentRow, 'ヒント：何で測定したか');

    // ========== セクション3: 試験条件 ==========
    const section3Row = equipmentRow + 4;
    addSectionHeader(sheet, section3Row, '【セクション3】試験条件', '#F57F17');

    const conditionRow = section3Row + 1;
    sheet.getRange(`A${conditionRow}:A${conditionRow + 4}`).mergeVertically();
    sheet.getRange(`A${conditionRow}`).setValue('試験条件');
    sheet.getRange(`B${conditionRow}:C${conditionRow + 4}`).mergeVertically();
    sheet.getRange(`B${conditionRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${conditionRow}`).setValue('環境条件（温度、湿度など）、試験パラメータ、実施時間などを記載。1行1項目推奨');
    sheet.setRowHeight(conditionRow, 100);
    addHintColumn(sheet, conditionRow, 'ヒント：どのような条件で');

    // ========== セクション4: 試験写真 ==========
    const section4Row = conditionRow + 5;
    addSectionHeader(sheet, section4Row, '【セクション4】試験実施の様子（写真）', '#F57C00');

    const photoRow = section4Row + 1;
    sheet.getRange(`A${photoRow}:A${photoRow + 4}`).mergeVertically();
    sheet.getRange(`A${photoRow}`).setValue('試験写真');
    sheet.getRange(`B${photoRow}:C${photoRow + 4}`).mergeVertically();
    sheet.getRange(`B${photoRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${photoRow}`).setValue('セットアップ、実施中、完了後の写真と説明。複数枚推奨');
    sheet.setRowHeight(photoRow, 100);
    addHintColumn(sheet, photoRow, 'ヒント：証拠となる画像');

    // ========== セクション5: 試験結果 ==========
    const section5Row = photoRow + 5;
    addSectionHeader(sheet, section5Row, '【セクション5】試験結果', '#E65100');

    // テーブルヘッダー
    const tableHeaderRow = section5Row + 1;
    const headers = ['測定項目', '初期値', '最終値', '変化量', '単位', '備考'];
    for (let i = 0; i < headers.length; i++) {
      const cell = sheet.getRange(tableHeaderRow, i + 1);
      cell.setValue(headers[i]);
      cell.setBackground('#E65100');
      cell.setFontColor('#FFFFFF');
      cell.setFontWeight('bold');
      cell.setHorizontalAlignment('center');
    }

    // テーブル行（10行分用意）
    for (let i = 0; i < 10; i++) {
      const rowNum = tableHeaderRow + 1 + i;
      sheet.getRange(`A${rowNum}:F${rowNum}`).setBorder(true, true, true, true, true, true);
    }

    // ========== セクション6: 試験考察 ==========
    const section6Row = tableHeaderRow + 12;
    addSectionHeader(sheet, section6Row, '【セクション6】試験考察・結論', '#6A1B9A');

    const analysisRow = section6Row + 1;
    sheet.getRange(`A${analysisRow}:A${analysisRow + 5}`).mergeVertically();
    sheet.getRange(`A${analysisRow}`).setValue('試験考察');
    sheet.getRange(`B${analysisRow}:C${analysisRow + 5}`).mergeVertically();
    sheet.getRange(`B${analysisRow}`).setWrap(true).setVerticalAlignment('top');
    sheet.getRange(`B${analysisRow}`).setValue('試験目的に対して、試験結果はどうであるか。目的達成度を分析し、判定と改善提案を記載（300-400字程度）');
    sheet.setRowHeight(analysisRow, 120);
    addHintColumn(sheet, analysisRow, 'ヒント：目的を達成したか');

    // ステータス
    const statusRow = analysisRow + 6;
    sheet.getRange(`A${statusRow}`).setValue('ステータス');
    sheet.getRange(`B${statusRow}`).setDataValidation(
      SpreadsheetApp.newDataValidation()
        .allowList(['確認済み', '要確認', '承認待ち'])
        .build()
    );
    sheet.getRange(`B${statusRow}`).setValue('確認済み');
    addHintColumn(sheet, statusRow, 'ドロップダウン選択');

    // ========== フッター ==========
    const footerRow = statusRow + 3;
    sheet.getRange(`A${footerRow}`).setValue('このテンプレートについて');
    sheet.getRange(`B${footerRow}`).setValue('実験記録テンプレート v1.0 | 作成日: 2026-05-05');
    sheet.getRange(`B${footerRow}`).setFontSize(9).setFontColor('#999999');

    // スプレッドシートを開く
    const url = ss.getUrl();
    Logger.log('テンプレート作成完了: ' + url);

    // ダイアログで完了を通知
    SpreadsheetApp.getUi().alert(
      'テンプレート作成完了！\n\n' +
      'URL: ' + url + '\n\n' +
      'Google Driveで「実験記録テンプレート」という名前で作成されました。\n' +
      'このファイルをコピーして、各試験の記録を作成してください。'
    );

  } catch (error) {
    Logger.log('エラー: ' + error);
    SpreadsheetApp.getUi().alert('エラーが発生しました: ' + error);
  }
}

/**
 * セクションヘッダーを追加
 */
function addSectionHeader(sheet, row, title, bgColor) {
  const cell = sheet.getRange(`A${row}:C${row}`);
  cell.mergeAcross();
  cell.setValue(title);
  cell.setBackground(bgColor);
  cell.setFontColor('#FFFFFF');
  cell.setFontWeight('bold');
  cell.setFontSize(12);
  cell.setHorizontalAlignment('left');
  cell.setVerticalAlignment('middle');
  sheet.setRowHeight(row, 30);
}

/**
 * C列にヒントを追加
 */
function addHintColumn(sheet, row, hint) {
  const cell = sheet.getRange(`C${row}`);
  cell.setValue(hint);
  cell.setFontStyle('italic');
  cell.setFontColor('#999999');
  cell.setFontSize(9);
  cell.setHorizontalAlignment('left');
  cell.setVerticalAlignment('top');
  cell.setWrap(true);
}
