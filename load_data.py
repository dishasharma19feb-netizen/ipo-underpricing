import pandas as pd

# Load the raw data
df = pd.read_excel("dataraw/IPO-age.xlsx", sheet_name="1975-2025", header=0)

# Rename columns
df.columns = [
    "offer_date", "company_name", "ticker", "cusip",
    "adr", "vc_backed", "dual_class", "post_issue_shares",
    "internet", "crsp_perm", "founding_year", "rollup",
    "empty1", "empty2", "empty3"
]

# Drop empty columns
df.drop(columns=["empty1", "empty2", "empty3"], inplace=True)

# Convert offer_date to datetime
df["offer_date"] = pd.to_datetime(df["offer_date"], format="%Y%m%d", errors="coerce")

# Filter 2010-2023
df = df[(df["offer_date"].dt.year >= 2010) & (df["offer_date"].dt.year <= 2023)]

# Replace missing value codes with NaN
df.replace(-99, pd.NA, inplace=True)
df.replace(".", pd.NA, inplace=True)

# Drop ADRs (foreign companies)
df = df[df["adr"] == 1]

# Reset index
df.reset_index(drop=True, inplace=True)

print(f"Total IPOs (2010-2023): {len(df)}")
print(df.head())
print(df.dtypes)