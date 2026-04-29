import polars as pl

df = pl.DataFrame({
    "id": range(1_000_000),
    "value": range(1_000_000)
})
df.write_csv("big_data.csv")

lazy_df = pl.scan_csv("big_data.csv")

result = lazy_df.filter(
    pl.col("value") > 999_990
).select(["id", "value"])

print(result.collect())