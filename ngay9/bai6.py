import polars as pl
import time

start = time.time()

df = pl.scan_csv("data/users.csv")

result = (
    df.select(["city", "income"])
      .group_by("city")
      .agg(pl.col("income").mean())
      .collect()
)
print(result)
print("Time:", time.time() - start)