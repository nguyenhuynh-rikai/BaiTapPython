import pandas as pd

df = pd.read_csv('datangay7.csv')

print(df.memory_usage(deep=True))

df["region"] = df["region"].astype("category")
df["product"] = df["product"].astype("category")

print(df.memory_usage(deep=True))
