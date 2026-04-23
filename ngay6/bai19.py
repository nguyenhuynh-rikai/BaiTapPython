import pandas as pd

df = pd.read_csv('data.csv')

filter_df = df[df['age'] > 25]
filter_df = filter_df.reset_index(drop=True)

print(filter_df)

