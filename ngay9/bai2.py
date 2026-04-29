import polars as pl
import time

start = time.time()

df = pl.read_csv("california_housing_train.csv")
result = (
    df.filter(pl.col("housing_median_age") > 25)
      .select(["longitude", "latitude"])
)

print("Eager mode: ", time.time() - start)


start = time.time()

df = pl.read_csv("california_housing_train.csv").lazy()
result = (
    df.filter(pl.col("housing_median_age") > 25)
      .select(["longitude", "latitude"])
      .collect()
)

print("Lazy mode: ", time.time() - start)
