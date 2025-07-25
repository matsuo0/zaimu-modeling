import pandas as pd
import glob
import matplotlib.pyplot as plt
import os
import argparse
import codecs
import matplotlib.ticker as ticker

# 会社ごとの設定
COMPANY_CONFIG = {
    "companyA": {
        "csv_pattern": "companyA/jpcrp*.csv",
        "output_dir": "output/companyA",
        "year_range": range(2018, 2026),
        "elements": {
            "売上高": ("jpcrp_cor:RevenueIFRSSummaryOfBusinessResults", "CurrentYearDuration"),
            "営業利益": ("jpcrp030000-asr_E33834-000:OperatingProfitLossIFRSSummaryOfBusinessResults", "CurrentYearDuration"),
            "経常利益": (None, None),  # 会社Aは該当データなし
            "純利益": ("jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults", "CurrentYearDuration"),
            "総資産": ("jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults", "CurrentYearInstant"),
            "従業員数": ("jpcrp_cor:NumberOfEmployees", "CurrentYearInstant"),
            "自己資本": ("jpcrp_cor:EquityAttributableToOwnersOfParentIFRSSummaryOfBusinessResults", "CurrentYearInstant"),
            "営業CF": ("jpcrp_cor:CashFlowsFromOperatingActivitiesSummaryOfBusinessResults", "CurrentYearDuration"),
            "有利子負債": ("jpcrp_cor:InterestBearingDebt", "CurrentYearInstant"),
            "減価償却費": ("jpcrp_cor:DepreciationAndAmortizationIFRSSummaryOfBusinessResults", "CurrentYearDuration"),
        },
    },
    "companyB": {
        "csv_pattern": "companyB/jpcrp*.csv",
        "output_dir": "output/companyB",
        "year_range": range(2018, 2024),
        "elements": {
            "売上高": ("jpcrp_cor:NetSalesSummaryOfBusinessResults", "CurrentYearDuration_NonConsolidatedMember"),
            "営業利益": ("jpcrp_cor:OperatingIncome", "CurrentYearDuration_NonConsolidatedMember"),
            "経常利益": ("jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults", "CurrentYearDuration_NonConsolidatedMember"),
            "純利益": ("jpcrp_cor:NetIncomeLossSummaryOfBusinessResults", "CurrentYearDuration_NonConsolidatedMember"),
            "総資産": ("jpcrp_cor:TotalAssetsSummaryOfBusinessResults", "CurrentYearInstant_NonConsolidatedMember"),
            "従業員数": ("jpcrp_cor:NumberOfEmployees", "CurrentYearInstant_NonConsolidatedMember"),
            "自己資本": ("jpcrp_cor:NetAssetsSummaryOfBusinessResults", "CurrentYearInstant_NonConsolidatedMember"),
            "営業CF": ("jpcrp_cor:CashFlowsFromOperatingActivitiesSummaryOfBusinessResults", "CurrentYearDuration_NonConsolidatedMember"),
            "有利子負債": ("jpcrp_cor:InterestBearingDebt", "CurrentYearInstant_NonConsolidatedMember"),
            "減価償却費": ("jpcrp_cor:DepreciationAndAmortizationSummaryOfBusinessResults", "CurrentYearDuration_NonConsolidatedMember"),
            "自己資本比率": ("jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults", "CurrentYearInstant_NonConsolidatedMember"),
            "ROE": ("jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults", "CurrentYearDuration_NonConsolidatedMember"),
        },
    },
}

plt.rcParams['font.family'] = 'Hiragino Sans'

def extract_value(df, element_id, context_id):
    if element_id is None or context_id is None:
        return None
    row = df[(df['要素ID'] == element_id) & (df['コンテキストID'] == context_id)]
    if not row.empty:
        try:
            return int(row['値'].values[0])
        except ValueError:
            return None
    return None

def try_read_csv(file):
    encodings = ['utf-8-sig', 'shift_jis', 'cp932', 'utf-16']
    for enc in encodings:
        try:
            return pd.read_csv(file, sep='\t', encoding=enc)
        except Exception:
            continue
    raise ValueError(f"CSVファイルのエンコーディングを判別できませんでした: {file}")

def main(company):
    config = COMPANY_CONFIG[company]
    os.makedirs(config["output_dir"], exist_ok=True)
    results = []
    for year in config["year_range"]:
        pattern = f"{company}/jpcrp*{year}-03-31_*.csv"
        files = glob.glob(pattern)
        if not files:
            continue
        file = files[0]
        df = try_read_csv(file)
        data = {"年度": year}
        for key, (element_id, context_id) in config["elements"].items():
            data[key] = extract_value(df, element_id, context_id)
        results.append(data)
    summary_df = pd.DataFrame(results)
    summary_df.to_csv(os.path.join(config["output_dir"], "summary.csv"), index=False)

    # 指標の自動計算
    if '自己資本' in summary_df.columns and '総資産' in summary_df.columns:
        print('自己資本:', summary_df['自己資本'])
        print('総資産:', summary_df['総資産'])
        summary_df['自己資本'] = pd.to_numeric(summary_df['自己資本'], errors='coerce')
        summary_df['総資産'] = pd.to_numeric(summary_df['総資産'], errors='coerce')
        summary_df['自己資本比率'] = summary_df['自己資本'] / summary_df['総資産'] * 100
        print('自己資本比率:', summary_df['自己資本比率'])
    if '純利益' in summary_df.columns and '自己資本' in summary_df.columns:
        summary_df['ROE'] = summary_df['純利益'] / summary_df['自己資本'] * 100
    if '純利益' in summary_df.columns and '総資産' in summary_df.columns:
        summary_df['ROA'] = summary_df['純利益'] / summary_df['総資産'] * 100
    if '営業利益' in summary_df.columns and '減価償却費' in summary_df.columns:
        summary_df['EBITDA'] = summary_df['営業利益'].fillna(0) + summary_df['減価償却費'].fillna(0)
    if '有利子負債' in summary_df.columns and '自己資本' in summary_df.columns:
        summary_df['有利子負債比率'] = summary_df['有利子負債'] / summary_df['自己資本'] * 100

    # 比率系指標の%換算（EDINET値は使わない）
    for col in ["ROE"]:
        if col in summary_df.columns:
            summary_df[col] = summary_df[col] * 100

    # グラフ生成
    graph_info = {
        "売上高": {"ylabel": "百万円", "divide": 1_000_000},
        "営業利益": {"ylabel": "百万円", "divide": 1_000_000},
        "経常利益": {"ylabel": "百万円", "divide": 1_000_000},
        "純利益": {"ylabel": "百万円", "divide": 1_000_000},
        "総資産": {"ylabel": "百万円", "divide": 1_000_000},
        "従業員数": {"ylabel": "人", "divide": 1},
        "自己資本": {"ylabel": "百万円", "divide": 1_000_000},
        "自己資本比率": {"ylabel": "%", "divide": 1},
        "ROE": {"ylabel": "%", "divide": 1},
        "ROA": {"ylabel": "%", "divide": 1},
        "営業CF": {"ylabel": "百万円", "divide": 1_000_000},
        "有利子負債": {"ylabel": "百万円", "divide": 1_000_000},
        "有利子負債比率": {"ylabel": "%", "divide": 1},
        "EBITDA": {"ylabel": "百万円", "divide": 1_000_000},
        "減価償却費": {"ylabel": "百万円", "divide": 1_000_000},
    }
    md_lines = [f"# {company} 財務指標グラフ\n"]
    for col, info in graph_info.items():
        if col in summary_df.columns and summary_df[col].notnull().any():
            plt.figure()
            y = summary_df[col] / info["divide"]
            plt.plot(summary_df["年度"], y, marker='o')
            plt.title(col)
            plt.xlabel("年度")
            plt.ylabel(info["ylabel"])
            ax = plt.gca()
            if info["ylabel"] == "百万円":
                ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
                ax.ticklabel_format(style='plain', axis='y')
            fname = f"{col}.png"
            fpath = os.path.join(config["output_dir"], fname)
            plt.savefig(fpath)
            plt.close()
            md_lines.append(f"![{col}]({fname})\n")
    # Markdown出力
    md_path = os.path.join(config["output_dir"], f"{company}_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(md_lines))
    print(f"Markdownレポートを出力: {md_path}")

def compare_companies():
    os.makedirs('output/compare', exist_ok=True)
    a_df = pd.read_csv('output/companyA/summary.csv')
    b_df = pd.read_csv('output/companyB/summary.csv')
    merged = pd.merge(a_df, b_df, on='年度', suffixes=('_A', '_B'))
    # 共通指標を自動抽出
    common_cols = set(a_df.columns) & set(b_df.columns) - {'年度'}
    for col in common_cols:
        # 単位判定
        if col in ['従業員数']:
            ylabel = '人'
            divide = 1
        elif col in ['自己資本比率', 'ROE', 'ROA', '有利子負債比率']:
            ylabel = '%'
            divide = 1
        else:
            ylabel = '百万円'
            divide = 1_000_000
        if col+'_A' in merged.columns and col+'_B' in merged.columns:
            plt.figure()
            plt.plot(merged['年度'], merged[col+'_A']/divide, marker='o', label='信和')
            plt.plot(merged['年度'], merged[col+'_B']/divide, marker='s', label='中央ビルト工業')
            plt.title(f'{col} 比較')
            plt.xlabel('年度')
            plt.ylabel(ylabel)
            plt.legend()
            ax = plt.gca()
            if ylabel == '百万円':
                ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
                ax.ticklabel_format(style='plain', axis='y')
            fname = f'{col}_compare.png'
            fpath = os.path.join('output/compare', fname)
            plt.savefig(fpath)
            plt.close()
    print('CompanyA（信和）とCompanyB（中央ビルト工業）の全共通指標の比較グラフをoutput/compare/に出力しました')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", choices=["companyA", "companyB"], required=False, help="対象会社")
    parser.add_argument("--compare", action="store_true", help="2社比較グラフを出力")
    args = parser.parse_args()
    if args.compare:
        compare_companies()
    elif args.company:
        main(args.company) 