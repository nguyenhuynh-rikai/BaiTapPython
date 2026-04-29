import polars as pl

df = pl.DataFrame({
    "name": ["A", "B", "C"],
    "score": [90, 75, 85]
})

print(df.sort("score"))


df = pl.DataFrame({
    "id": [1, 2],
    "values": [[3, 1, 2], [6, 5]]
})
print(df.explode("values"))