# 使い方・起動方法

## セットアップ
1. リポジトリをクローン
2. 必要なライブラリをインストール

## 起動方法
```sh
python main.py
```

または

```sh
streamlit run app.py
```
（Webアプリの場合）

## 出力例
- 分析レポート（Markdownファイル）
- グラフ・図表（PNG等画像ファイル）
- Markdown内で画像を参照する形でレポートを自動生成

## GitHubでの閲覧について
- 画像ファイルはリポジトリ内（例: `images/` ディレクトリ）に保存してください。
- Markdownファイル内で画像を相対パスで参照することで、GitHub上でも画像付きレポートを閲覧できます。

例：
```markdown
![グラフの例](images/sample-graph.png)
```

## EDINET財務諸表CSVのインポート手順
1. EDINET（金融庁の電子開示システム）より、会社A・会社Bの財務諸表（PL/BS/CF等）をCSV形式でダウンロードしてください。
2. ダウンロードしたCSVファイルを本アプリにインポートします。
3. インポート後、会社A・会社Bそれぞれの財務データとして利用できます。

### CSVファイル例
- `edinet_companyA.csv`
- `edinet_companyB.csv`

※CSVの具体的なフォーマットはEDINETの仕様に準じます。 