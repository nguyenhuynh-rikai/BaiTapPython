import pandas as pd

df = pd.read_csv("save.csv")
df2 = pd.read_csv("save2.csv")

df3 = pd.concat([df, df2], ignore_index=True)

print(df3)