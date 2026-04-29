import polars as pl

df = pl.DataFrame({
    "a": [1, 2, 3],
    "b": [4, 5, 6]
})

result = df.select([
    pl.col("a"),
    (pl.col("a") + pl.col("b")).alias("sum")
])

print(result)

df = df.with_columns([
    (pl.col("a") * 2).alias("a_x2"),
    (pl.col("a") + pl.col("b")).alias("sum")
])

print(df)
df = df.filter(pl.col("a") > 1)
print(df)