import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C", "D", "E"],
    "spending": [2500, 9900, 5000, 8500, 3300]
})

df["customer_type"] = df["spending"].apply(
    lambda x: "VIP" if x > 4500 else "normal"
)

print(df)