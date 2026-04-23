import pandas as pd

df = pd.read_csv('data.csv')

newdf = df.rename(columns={'name':"FUlLNAME"})

print(newdf)