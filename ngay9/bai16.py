import polars as pl

df = pl.DataFrame({
    "time": ["2024-01-01 10:00:00", "2024-06-01 15:00:00"]
}).with_columns(
    pl.col("time").str.strptime(pl.Datetime)
)

df = df.with_columns(
    pl.col("time").dt.replace_time_zone("UTC")
)

df = df.with_columns(
    pl.col("time").dt.convert_time_zone("Asia/Ho_Chi_Minh").alias("vn_time")
)

print(df)