import pandas as pd

df = pd.read_csv('data.csv')



print(df.loc[0])
print(df.iloc[0:4])