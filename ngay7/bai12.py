import pandas as pd

df = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=6),
    "price": [100, 105, 102, 110, 108, 115]
})

df["MA_3"] = df["price"].rolling(window=3).mean()

print(df)