import pandas as pd

df = pd.read_csv("dataraw/ipo_scraped.csv")

print(f"Before cleaning: {len(df)} rows")

# Fix ipo_price — remove $ and convert to float
df["ipo_price"] = df["ipo_price"].str.replace("$", "", regex=False).str.strip()
df["ipo_price"] = pd.to_numeric(df["ipo_price"], errors="coerce")

# Fix return — remove % and convert to float
df["return"] = df["return"].str.replace("%", "", regex=False).str.replace(",", "", regex=False).str.strip()
df["return"] = pd.to_numeric(df["return"], errors="coerce")

# Fix ipo_date
df["ipo_date"] = pd.to_datetime(df["ipo_date"], errors="coerce")

# Drop rows with missing critical values
df = df.dropna(subset=["ipo_price", "return", "ipo_date", "ticker"])

# Drop rows where ipo_price is 0 or negative
df = df[df["ipo_price"] > 0]

# Add year column
df["year"] = df["ipo_date"].dt.year

df.reset_index(drop=True, inplace=True)

print(f"After cleaning: {len(df)} rows")
print(df.dtypes)
print(df.head())

df.to_csv("dataraw/ipo_clean.csv", index=False)
print("\nSaved to dataraw/ipo_clean.csv")