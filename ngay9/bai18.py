import polars as pl

df = pl.DataFrame({
    "x": list(range(1_000_000)),
    "y": list(range(1_000_000))
})

df = df.with_columns(
    (pl.col("x") * pl.col("y")).alias("z")
)

print(df.head())