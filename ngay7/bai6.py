import pandas as pd

df1 = pd.read_csv('datangay7.csv')
df2 = pd.read_csv('dataconnect.csv')

res = pd.pivot_table(df1, index='date', columns='region', values='revenue', aggfunc='sum')
print(res)