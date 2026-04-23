import pandas as pd

df = pd.read_csv("data.csv")

df = df.sort_values(by=["latitude", "longitude"], ascending=[True, False])

print(df)