import pandas as pd

df = pd.read_csv("dataraw/ipo_clean.csv")

# Show the most extreme returns
print("=== Top 10 highest returns ===")
print(df.nlargest(10, "return")[["ticker", "company", "ipo_date", "ipo_price", "return"]])

print("\n=== Top 10 lowest returns ===")
print(df.nsmallest(10, "return")[["ticker", "company", "ipo_date", "ipo_price", "return"]])

# Check how many are extreme outliers
print(f"\nReturns > 200%: {(df['return'] > 200).sum()}")
print(f"Returns < -90%: {(df['return'] < -90).sum()}")
print(f"IPO price < $2: {(df['ipo_price'] < 2).sum()}")