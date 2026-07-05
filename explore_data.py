import pandas as pd

df = pd.read_csv("dataraw/IPO_data_2023_S1.csv")

print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nData types:")
print(df.dtypes)
print(f"\nMissing values:")
print(df.isna().sum())