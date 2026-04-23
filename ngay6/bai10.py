import pandas as pd

df = pd.read_csv('data.csv')

df_sort = df.sort_values(by=['city','age'])
print(df_sort)