import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("dataraw/ipo_features_v1.csv")

# Simple features we have so far
features = ["ipo_price", "month", "quarter", "day_of_week"]
target = "return_winsorized"

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Train size: {len(X_train)}")
print(f"Test size: {len(X_test)}")

model = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nMAE: {mae:.2f}")
print(f"R²: {r2:.4f}")

# Feature importance
importance = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print(f"\nFeature importance:")
print(importance)