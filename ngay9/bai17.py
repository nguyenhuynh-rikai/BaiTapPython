import polars as pl

df = pl.DataFrame({
    "id": [1, 2, 3],
    "value": [10, 20, 30]
})

df.write_parquet("data.parquet")

df2 = pl.read_parquet("data.parquet")

print(df2)