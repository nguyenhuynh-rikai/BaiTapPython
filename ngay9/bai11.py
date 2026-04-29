import polars as pl

df = pl.DataFrame({
    "trans_id": [1, 2, 3, 4, 5],
    "user_id": [101, 102, 103, 104, 105],
    "items": [
        [7, 13, 22],
        [76, 20],
        [71, 91, 12, 5],
        [7, 22],
        [62, 79, 88]
    ],
    "amount": [120, 450, 300, 150, 600]
})

df = df.with_columns(
    pl.col("items").list.len().alias("num_items")
)

print(df)