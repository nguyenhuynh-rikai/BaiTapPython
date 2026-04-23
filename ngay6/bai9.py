import pandas as pd

df = pd.read_csv("data.csv")

df = df.rename(columns={"total_rooms": "sum_rooms"})

print(df)