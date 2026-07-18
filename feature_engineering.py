import pandas as pd
import numpy as np

df = pd.read_csv("dataraw/ipo_clean.csv")
df["ipo_date"] = pd.to_datetime(df["ipo_date"])

print(f"Before winsorizing:")
print(df["return"].describe())

# Winsorize returns at 1st and 99th percentile
lower = df["return"].quantile(0.01)
upper = df["return"].quantile(0.99)

print(f"\n1st percentile: {lower:.2f}%")
print(f"99th percentile: {upper:.2f}%")

df["return_winsorized"] = df["return"].clip(lower=lower, upper=upper)

print(f"\nAfter winsorizing:")
print(df["return_winsorized"].describe())

# Extract date-based features
df["month"] = df["ipo_date"].dt.month
df["quarter"] = df["ipo_date"].dt.quarter
df["day_of_week"] = df["ipo_date"].dt.dayofweek  # 0=Monday

# Underpricing flag (binary target for classification if needed later)
df["is_underpriced"] = (df["return_winsorized"] > 0).astype(int)

print(f"\nUnderpriced (positive return): {df['is_underpriced'].sum()} / {len(df)} ({df['is_underpriced'].mean()*100:.1f}%)")

df.to_csv("dataraw/ipo_features_v1.csv", index=False)
print("\nSaved to dataraw/ipo_features_v1.csv")