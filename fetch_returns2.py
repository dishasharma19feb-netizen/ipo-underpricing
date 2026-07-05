import pandas as pd
import yfinance as yf
from datetime import timedelta
import time

df = pd.read_csv("dataraw/IPO_data_2023_S1.csv")

# Drop rows with missing ticker or ipo_date or ipo_price
df = df.dropna(subset=["ticker", "ipo_date", "ipo_price"])
df["ipo_date"] = pd.to_datetime(df["ipo_date"], dayfirst=True)
df.reset_index(drop=True, inplace=True)

print(f"Total IPOs to process: {len(df)}")

results = []

for i, row in df.iterrows():
    ticker = str(row["ticker"]).strip()
    ipo_date = row["ipo_date"]
    ipo_price = row["ipo_price"]

    start = ipo_date
    end = ipo_date + timedelta(days=7)

    try:
        data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if not data.empty:
            first_day_close = float(data["Close"].iloc[0])
        else:
            first_day_close = None
    except Exception:
        first_day_close = None

    first_day_return = None
    if first_day_close is not None and ipo_price > 0:
        first_day_return = (first_day_close - ipo_price) / ipo_price

    results.append({
        "company": row["company"],
        "ticker": ticker,
        "state": row["state"],
        "exchange": row["exchange"],
        "industry": row["industry"],
        "ipo_date": ipo_date,
        "ipo_price": ipo_price,
        "ipo_amount": row["ipo_amount"],
        "ipo_fees": row["ipo_fees"],
        "profit": row["profit"],
        "debt": row["debt"],
        "assets": row["assets"],
        "first_day_close": first_day_close,
        "first_day_return": first_day_return
    })

    if (i + 1) % 50 == 0:
        print(f"  Processed {i+1}/{len(df)}")

    time.sleep(0.2)

results_df = pd.DataFrame(results)
results_df.to_csv("dataraw/ipo_final.csv", index=False)
print(f"\nDone! Saved {len(results_df)} rows.")
print(f"Missing first_day_return: {results_df['first_day_return'].isna().sum()}")