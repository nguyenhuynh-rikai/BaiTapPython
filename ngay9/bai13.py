import polars as pl

df = pl.DataFrame({
    "user_id": [1, 1, 1, 2, 2, 3],
    "day": [1, 2, 3, 1, 2, 1],
    "score": [10, 20, 15, 5, 30, 25]
})


df = df.with_columns(
    pl.col("score")
    .cum_sum()
    .over("user_id")
    .alias("cumsum")
)

print(df)
