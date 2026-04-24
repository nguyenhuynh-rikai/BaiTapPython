import pandas as pd

df = pd.DataFrame({
    "date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
    "revenue": [100, 200, 150, 300, 250]
})

df = df.set_index("date")

monthly = df.resample("ME").sum()
print(monthly)