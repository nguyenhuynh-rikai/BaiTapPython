import polars as pl

df = pl.scan_csv("data/users.csv")

result = (
    df.filter(pl.col("age") > 25)
      .with_columns((pl.col("age") + 10).alias("age_plus"))
      .select(["user_id", "age_plus"])
      .collect()
)

print(result)