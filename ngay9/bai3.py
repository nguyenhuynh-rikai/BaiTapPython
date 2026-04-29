import polars as pl
import time

start = time.time()

df = pl.read_csv("california_housing_train.csv")
df = df.filter(pl.col("housing_median_age") > 30)

print("Primary case: ", time.time() - start)

df = pl.scan_csv("california_housing_train.csv")

start = time.time()

result = (
    df.filter(pl.col("housing_median_age") > 30)
      .select(["longitude", "latitude"])
      .collect()
)

print("Used scan csv: ", time.time() - start)