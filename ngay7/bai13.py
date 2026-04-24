import pandas as pd

df = pd.DataFrame({
    "region": ["North", "North", "South"],
    "product": ["A", "B", "A"],
    "revenue": [100, 200, 150]
})

df = df.set_index(["region", "product"])
print(df)