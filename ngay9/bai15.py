import polars as pl

df = pl.DataFrame({
    "user_id": [1, 2, 3],
    "items": [
        [5, 2, 9],
        [10, 1],
        [7, 3, 8]
    ]
})

df = df.with_columns(
    pl.col("items").list.sort().alias("items_sorted")
)

print(df)

