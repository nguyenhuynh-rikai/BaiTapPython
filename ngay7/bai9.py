import pandas as pd

df = pd.read_csv('datangay7.csv')

res = df[df["product"].str.contains("Mo")]

df_replace = df["product"].str.replace("Mouse", "Chuot")

print(res)

print(df_replace)
