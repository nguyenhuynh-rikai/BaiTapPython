import pandas as pd
import openpyxl

df = pd.read_csv('data.csv')

filter_df = df[df['age'] > 25]
filter_df = filter_df.reset_index(drop=True)

print(filter_df)

df.to_csv('bai20.csv', index=False)
df.to_excel('bai20.xlsx', index=False)
df.to_json('bai20.json',orient='records',indent=4)

