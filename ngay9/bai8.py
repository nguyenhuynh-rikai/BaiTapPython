import polars as pl

result = (
    pl.scan_csv("data/users.csv")
    .filter(pl.col("is_active") == True)
    .with_columns(
        (pl.col("income") / 1000).alias("income_k")
    )
    .select(["user_id", "city", "income_k"])
    .group_by("city")
    .agg(pl.col("income_k").mean())
    .collect()
)

print(result)