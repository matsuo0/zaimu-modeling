import pandas as pd
import glob
import matplotlib.pyplot as plt

# ファイルパターン
csv_files = sorted(glob.glob("companyB/jpcrp*.csv"))

def extract_value(df, element_id, context_id):
    row = df[(df['要素ID'] == element_id) & (df['コンテキストID'] == context_id)]
    if not row.empty:
        try:
            return int(row['値'].values[0])
        except ValueError:
            return None
    return None

# 2018〜2023年のデータのみ抽出
years = list(range(2018, 2024))
results = []

for year in years:
    pattern = f"companyB/jpcrp030000-asr-001_E00091-000_{year}-03-31_*.csv"
    files = glob.glob(pattern)
    if not files:
        continue
    file = files[0]
    df = pd.read_csv(file, sep='\t', encoding='utf-8-sig')
    data = {
        '年度': year,
        '売上高': extract_value(df, 'jpcrp_cor:NetSalesSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember'),
        '経常利益': extract_value(df, 'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember'),
        '当期純利益': extract_value(df, 'jpcrp_cor:NetIncomeLossSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember'),
        '総資産': extract_value(df, 'jpcrp_cor:TotalAssetsSummaryOfBusinessResults', 'CurrentYearInstant_NonConsolidatedMember'),
    }
    results.append(data)

summary_df = pd.DataFrame(results)
print(summary_df)

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(summary_df['年度'], summary_df['売上高'], marker='o')
plt.title('売上高')
plt.xlabel('年度')
plt.ylabel('円')

plt.subplot(2, 2, 2)
plt.plot(summary_df['年度'], summary_df['経常利益'], marker='o')
plt.title('経常利益')
plt.xlabel('年度')
plt.ylabel('円')

plt.subplot(2, 2, 3)
plt.plot(summary_df['年度'], summary_df['当期純利益'], marker='o')
plt.title('当期純利益')
plt.xlabel('年度')
plt.ylabel('円')

plt.subplot(2, 2, 4)
plt.plot(summary_df['年度'], summary_df['総資産'], marker='o', label='総資産')
plt.ylabel('円')
plt.xlabel('年度')
plt.title('総資産')

plt.tight_layout()
plt.show() 