import pandas as pd

df = pd.DataFrame({
    "price": [10, 20, 30, 40, 50]
})

df["MA_3"] = df["price"].rolling(3).mean()
print(df)