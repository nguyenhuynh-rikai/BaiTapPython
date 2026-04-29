import pandas as pd

df1 = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["A", "B", "C"]
})

df2 = pd.DataFrame({
    "id": [2, 3, 4],
    "score": [80, 90, 100]
})

result = pd.merge(df1, df2, on="id", how="inner")
print(result)

# df1 = df1.set_index("id")
# df2 = df2.set_index("id")
#
# result = df1.join(df2, how="inner")
# print(result)
#
# df1["id"] = df1["id"].astype("category")
# df2["id"] = df2["id"].astype("category")
#
# df2 = df2[["id", "score"]]
