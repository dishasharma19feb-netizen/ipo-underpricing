import pandas as pd

df = pd.read_csv("dataraw/ipo_with_returns.csv")
df["offer_date"] = pd.to_datetime(df["offer_date"])
df["year"] = df["offer_date"].dt.year

summary = df.groupby("year")["first_day_close"].apply(lambda x: x.notna().sum()).reset_index()
summary.columns = ["year", "found"]
total = df.groupby("year").size().reset_index(name="total")
summary = summary.merge(total, on="year")
summary["missing_pct"] = ((summary["total"] - summary["found"]) / summary["total"] * 100).round(1)
print(summary)