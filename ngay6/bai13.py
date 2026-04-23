import pandas as pd

df = pd.read_csv('data.csv')

df_clean = df.dropna()
print(df_clean.head())
