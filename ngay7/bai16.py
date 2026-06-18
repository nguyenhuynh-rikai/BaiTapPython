import pandas as pd

df = pd.DataFrame({
    "region": ["North", "South", "North", "North"],
    "product": ["A", "B", "A", "A"],
    "revenue": [100, 200, 100, 100]
})
df_clean = df.drop_duplicates()

print(df.duplicated())
print(df_clean)
