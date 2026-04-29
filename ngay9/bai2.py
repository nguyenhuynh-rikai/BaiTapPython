"""""
import polars as pl

df = pl.read_csv("data/users.csv")

df = df.filter(pl.col("age") > 25)
print(df)
"""""
# lazy

import polars as pl

df = pl.scan_csv("data/users.csv")
result = (
    df.filter(pl.col("age") > 25)
      .select(["user_id", "age"])
)

result = result.collect()
print(result)