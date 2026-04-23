import pandas as pd

df = pd.read_csv("data.csv")

print(df["housing_median_age"].unique())