import pandas as pd

df = pd.DataFrame({
    "date": ["2024-01-15", "2024-02-20"]
})

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["weekday"] = df["date"].dt.day_name()

print(df)