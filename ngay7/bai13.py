import pandas as pd

data = {
    "region": ["North", "North", "South", "South"],
    "product": ["A", "B", "A", "B"],
    "revenue": [100, 150, 200, 250]
}

df = pd.DataFrame(data)

df = df.set_index(["region", "product"])

print(df)