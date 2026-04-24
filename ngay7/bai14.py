import pandas as pd

df = pd.read_csv('datangay7.csv')

res = pd.crosstab(
    df["region"],
    df["product"]
)
print(res)
