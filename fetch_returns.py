import pandas as pd
import yfinance as yf
from datetime import timedelta

# Load the cleaned data
df = pd.read_excel("dataraw/IPO-age.xlsx", sheet_name="1975-2025", header=0)

df.columns = [
    "offer_date", "company_name", "ticker", "cusip",
    "adr", "vc_backed", "dual_class", "post_issue_shares",
    "internet", "crsp_perm", "founding_year", "rollup",
    "empty1", "empty2", "empty3"
]

df.drop(columns=["empty1", "empty2", "empty3"], inplace=True)
df["offer_date"] = pd.to_datetime(df["offer_date"], format="%Y%m%d", errors="coerce")
df = df[(df["offer_date"].dt.year >= 2010) & (df["offer_date"].dt.year <= 2023)]
df.replace(-99, pd.NA, inplace=True)
df.replace(".", pd.NA, inplace=True)
df = df[df["adr"] == 1]
df = df[df["ticker"].notna()]
df.reset_index(drop=True, inplace=True)

print(f"Total IPOs to process: {len(df)}")

# Get unique tickers
tickers = df["ticker"].astype(str).str.strip().unique().tolist()
print(f"Unique tickers: {len(tickers)}")

# Fetch all price data at once in one batch call
print("Downloading all price data in batch (this takes 1-2 mins)...")
all_data = yf.download(
    tickers,
    start="2010-01-01",
    end="2024-01-01",
    progress=True,
    auto_adjust=True
)

# Extract closing prices
close_prices = all_data["Close"]

print("Fetching done! Now computing first-day returns...")

results = []

for i, row in df.iterrows():
    ticker = str(row["ticker"]).strip()
    offer_date = row["offer_date"]

    first_day_close = None
    try:
        if ticker in close_prices.columns:
            # Get prices from offer date onwards
            ticker_prices = close_prices[ticker].loc[offer_date:]
            ticker_prices = ticker_prices.dropna()
            if len(ticker_prices) > 0:
                first_day_close = float(ticker_prices.iloc[0])
    except Exception:
        first_day_close = None

    results.append({
        "ticker": ticker,
        "company_name": row["company_name"],
        "offer_date": offer_date,
        "vc_backed": row["vc_backed"],
        "dual_class": row["dual_class"],
        "internet": row["internet"],
        "founding_year": row["founding_year"],
        "rollup": row["rollup"],
        "first_day_close": first_day_close
    })

results_df = pd.DataFrame(results)
results_df.to_csv("dataraw/ipo_with_returns.csv", index=False)
print(f"\nDone! Saved {len(results_df)} rows.")
print(f"Missing first_day_close: {results_df['first_day_close'].isna().sum()}")