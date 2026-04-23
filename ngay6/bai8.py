import pandas as pd

df = pd.read_csv("data.csv")

df = df.drop("longitude", axis=1)

print(df)