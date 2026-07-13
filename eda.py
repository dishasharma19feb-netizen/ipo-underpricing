import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataraw/ipo_clean.csv")
df["ipo_date"] = pd.to_datetime(df["ipo_date"])

print("=== Basic Stats ===")
print(f"Total IPOs: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
print(f"\nReturn stats:")
print(df["return"].describe())

# Plot 1 - Return distribution
plt.figure(figsize=(10, 5))
plt.hist(df["return"], bins=100, edgecolor="black", color="steelblue")
plt.title("IPO First-Day Return Distribution")
plt.xlabel("First Day Return (%)")
plt.ylabel("Count")
plt.axvline(0, color="red", linestyle="--", label="0%")
plt.axvline(df["return"].median(), color="green", linestyle="--", label=f"Median: {df['return'].median():.1f}%")
plt.legend()
plt.tight_layout()
plt.savefig("eda_return_distribution.png")
plt.close()
print("\nSaved: eda_return_distribution.png")

# Plot 2 - Average return by year
plt.figure(figsize=(10, 5))
yearly = df.groupby("year")["return"].mean()
plt.bar(yearly.index, yearly.values, color="steelblue", edgecolor="black")
plt.title("Average First-Day Return by Year")
plt.xlabel("Year")
plt.ylabel("Avg Return (%)")
plt.tight_layout()
plt.savefig("eda_return_by_year.png")
plt.close()
print("Saved: eda_return_by_year.png")

# Plot 3 - IPO count by year
plt.figure(figsize=(10, 5))
yearly_count = df.groupby("year").size()
plt.bar(yearly_count.index, yearly_count.values, color="coral", edgecolor="black")
plt.title("Number of IPOs by Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("eda_count_by_year.png")
plt.close()
print("Saved: eda_count_by_year.png")

print("\n=== Return by Year ===")
print(df.groupby("year")["return"].agg(["mean", "median", "count"]).round(2)) 