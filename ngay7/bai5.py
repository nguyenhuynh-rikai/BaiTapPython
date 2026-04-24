import pandas as pd

df1 = pd.DataFrame({
    "user_id": [1, 2, 3],
    "name": ["An", "Binh", "Chi"]
})

df2 = pd.DataFrame({
    "user_id": [1, 2],
    "order": ["A", "B"]
})

df = pd.merge(df1, df2, on="user_id", how="left")
print(df)