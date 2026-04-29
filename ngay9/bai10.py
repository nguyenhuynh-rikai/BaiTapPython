import polars as pl

df = pl.DataFrame({
    "a": [1.0, None, float("nan")]
})

print(df)

df.select(pl.col("a").is_null())
df.select(pl.col("a").is_nan())

df.with_columns(
    pl.col("a").fill_null(0)
)

print(df.with_columns(
    pl.col("a").fill_nan(0)
))
print(df.with_columns(
    pl.col("a").fill_nan(0)
))