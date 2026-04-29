import polars as pl

df = pl.scan_parquet("data.parquet")

result = (
    df
    .filter(pl.col("score") > 50)
    .select(["user_id", "score"])
    .collect()
)

print(result)