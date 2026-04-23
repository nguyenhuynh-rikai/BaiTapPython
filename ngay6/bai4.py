import pandas as pd

df = pd.read_csv('data.csv')

print(df[df['age']== 25])