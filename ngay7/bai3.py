import pandas as pd

df1 = pd.read_csv('datangay7.csv')
df2 = pd.read_csv('dataconnect.csv')
df = pd.concat([df1, df2], ignore_index=True)

print(df)