import pandas as pd
from pandas.core.interchange import column

df = pd.read_csv('data.csv')

newdf = df.drop('age', axis=1)

print(newdf)