import pandas as pd

df = pd.read_csv("data.csv")

print(df.dtypes)

df["longitude"] = pd.to_datetime(df["longitude"])

print(df.dtypes)