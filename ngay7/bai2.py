import pandas as pd

df = pd.read_csv('datangay7.csv')

print(df.groupby('region')['revenue'].agg(['mean','max','min']))