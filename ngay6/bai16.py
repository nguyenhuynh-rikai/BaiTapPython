import pandas as pd

df = pd.read_csv('data.csv')

df['age'] = pd.to_numeric(df['age'])

print(df.dtypes)
