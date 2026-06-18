import pandas as pd

df = pd.DataFrame({
    "region": ["North", "South", "North"],
    "product": ["A", "B", "C"],
    "revenue": [100, 200, 300]
})

df["type"] = df["revenue"].apply(
    lambda x: "VIP" if x > 150 else "Normal"
)

print(df)
