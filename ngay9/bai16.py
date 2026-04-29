import polars as pl

df = pl.DataFrame({
    "user_id": [1, 2, 3],
    "time_utc": [
        "2024-01-01 10:00:00",
        "2024-01-01 15:30:00",
        "2024-01-02 08:45:00"
    ]
})

df = df.with_columns(
    pl.col("time_utc").str.to_datetime()
)

df = df.with_columns(
    pl.col("time_utc").dt.convert_time_zone("Asia/Ho_Chi_Minh")
)

df = df.with_columns([
    pl.col("time_utc").dt.hour().alias("hour"),
    pl.col("time_utc").dt.weekday().alias("weekday")
])

print(df)