import pandas as pd

df = pd.read_csv('datangay7.csv')

df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

monthly = df.resample("ME")["revenue"].sum()

print(monthly)