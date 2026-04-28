import pandas as pd

df = pd.read_csv('datangay7.csv')

df['date'] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day

print(df)