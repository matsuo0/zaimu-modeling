# 財務モデリングアプリケーション

このリポジトリは、会社Aが会社BをM&A（合併・買収）する際に必要な財務モデリングを支援するPythonアプリケーションのプロジェクトです。
特に、DCF法による企業価値評価、PMI（統合後）シナリオ分析、買収価格算定に重点を置いています。

## ドキュメント
詳細は`docs/`ディレクトリを参照してください。

## 補足
エルライン: 
従業員数206名から218名 、グループ連結売上高120億円から160億円 、単体売上高126億円

似た売上高の会社でEBINETに登録されている下記を買収側の基準とする
信和(株)【3447.T】

---

## 必要なPythonライブラリ

CompanyAの財務データ可視化スクリプト（src/plot_financials.py）を実行するには、以下のPythonライブラリが必要です。

- pandas
- matplotlib

インストール例：

```
pip install pandas matplotlib
```

## 主なPythonスクリプト

- `src/plot_financials.py`
  CompanyAの財務データ（2018〜2025年）を年度ごとに集計・グラフ化するスクリプトです。

## 会社ごとの出力例

- 会社A・会社BそれぞれのEDINET財務データ（CSV）を取得・格納後、
- Pythonスクリプトで各社ごとに
  - 財務データのグラフ画像（PNG等）
  - 分析レポート（Markdown）
  を自動生成します。

### 出力例
- output/companyA_report.md
- output/companyA_graph_売上高推移.png
- output/companyA_graph_営業利益推移.png
- output/companyA_graph_純利益推移.png
- output/companyA_graph_総資産推移.png
- output/companyA_graph_自己資本比率.png
- output/companyA_graph_ROE.png
- output/companyA_graph_ROA.png
- ...（できるだけ多くの財務指標グラフを出力）

- output/companyB_report.md
- output/companyB_graph_売上高推移.png
- output/companyB_graph_営業利益推移.png
- output/companyB_graph_純利益推移.png
- output/companyB_graph_総資産推移.png
- output/companyB_graph_自己資本比率.png
- output/companyB_graph_ROE.png
- output/companyB_graph_ROA.png
- ...（同様に多様なグラフを出力）

## 機能・特徴（2024年7月時点）

- CompanyA・CompanyBそれぞれのEDINET財務データ（CSV）から主要指標を自動抽出・自動計算
- 自己資本比率は「自己資本÷総資産×100」で自動計算（EDINET値がなくても算出）
- 売上高、営業利益、経常利益、純利益、総資産、自己資本、自己資本比率、ROE、ROA、EBITDA、従業員数などM&Aで重要な指標を網羅
- 2社の全共通指標を自動で比較グラフ化（output/compare/配下にPNG出力）
- 指標や要素IDはEDINET CSVの内容に応じて柔軟に拡張可能
- 欠損値や型変換も自動で処理

### 出力例
- output/companyA/summary.csv, output/companyB/summary.csv … 各社の年度別主要指標一覧
- output/companyA/（PNG, Markdown） … 各社ごとのグラフ・レポート
- output/compare/（PNG） … 2社の全共通指標の比較グラフ

---

## 実行手順

1. 仮想環境の作成・有効化

```sh
python3 -m venv venv
source venv/bin/activate
```

2. 必要なライブラリのインストール

```sh
pip install pandas matplotlib
```

3. スクリプトの実行（会社Aの例）

```sh
python src/plot_financials.py --company companyA
```

会社Bの場合は

```sh
python src/plot_financials.py --company companyB
```

4. 出力結果の確認

- `output/companyA/` または `output/companyB/` フォルダ内に、グラフ画像（PNG）とMarkdownレポート（.md）が生成されます。

