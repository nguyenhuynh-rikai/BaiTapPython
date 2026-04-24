import pandas as pd

df = pd.DataFrame({
    "name": ["An", "Binh", "An"],
    "age": [20, 21, 20]
})

df = df.drop_duplicates(subset="name", keep="first")    

print(df)