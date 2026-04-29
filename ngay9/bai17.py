import polars as pl

df = pl.DataFrame({
    "user_id": [1, 2, 3],
    "score": [10, 20, 30]
})

df.write_parquet("data.parquet")

df = pl.read_parquet("data.parquet")

df_lazy = pl.scan_parquet("data.parquet")

df_filtered = df_lazy.filter(pl.col("score") > 15).collect()

print(df_filtered)