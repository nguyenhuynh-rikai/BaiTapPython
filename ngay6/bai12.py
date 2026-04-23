
import pandas as pd

df = pd.read_csv('data.csv')



print(df.isna().sum())

df_fill = df.fillna({
    "name": "Unnamed",
    "age": 0,
    "city": "Unknown"
})
print(df_fill.isna().sum())