import pandas as pd

data = {
    "region": ["North", "South", "North", "South", "East"],
    "revenue": [100, 200, 150, 300, 250]
}

df = pd.DataFrame(data)
print(df)

result = df.groupby("region")["revenue"].sum()
print(result)