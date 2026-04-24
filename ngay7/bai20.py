import pandas as pd

data = [
    {"id": 1, "info": {"name": "An", "age": 25}},
    {"id": 2, "info": {"name": "Binh", "age": 30}}
]

df = pd.DataFrame(data)
print(df)

df_flat = pd.json_normalize(df["info"])
print(df_flat)