import polars as pl

df = pl.read_csv("data/users.csv")

print(df.select(pl.col("income").null_count()))

df = df.with_columns(
    pl.col("income").fill_nan(None)
)

df = df.with_columns(
    pl.col("income").fill_null(
        pl.col("income").mean().over("city")
    )
)

df = df.filter(pl.col("income").is_not_null())

print(df.head())