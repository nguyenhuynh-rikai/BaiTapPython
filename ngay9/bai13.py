import polars as pl

df = pl.DataFrame({
    "region": ["A", "A", "B", "B", "B"],
    "sales": [100, 200, 150, 300, 250]
})

print(df.with_columns(
    pl.col("sales").cum_sum().over("region").alias("cum_sales")
))