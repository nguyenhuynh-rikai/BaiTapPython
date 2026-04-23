import pandas as pd

df = pd.read_csv("data.csv")

df["rooms_per_household"] = df["total_rooms"] / df["households"]

print(df)