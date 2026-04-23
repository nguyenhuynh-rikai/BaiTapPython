import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C", "D"],
    "age": [20, 25, 30, 35]
})

df_filtered = df[df["age"] > 25]
print(df_filtered)

df_filtered = df_filtered.reset_index()
print(df_filtered)