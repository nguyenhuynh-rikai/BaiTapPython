import polars as pl

df = pl.scan_csv("data/users.csv")

result = (
    df.filter(pl.col("age") > 25)
      .select(["user_id", "age"])
      .collect()
)

print(result)