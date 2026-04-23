import pandas as pd

df = pd.read_csv("data.csv")

df = df.fillna(0)

print(df)