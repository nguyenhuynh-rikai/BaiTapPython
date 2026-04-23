import pandas as pd
import datetime

df = pd.read_csv('data.csv')

current_time = datetime.datetime.now().year

df['year of birth'] = current_time - df['age']

print(df)