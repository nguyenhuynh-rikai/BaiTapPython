import polars as pl

df = pl.read_csv("data.csv")

result = (
    df.filter(pl.col("housing_median_age") > 25)
      .select(["longitude", "latitude"])
)

df = pl.read_csv("data.csv").lazy()

result = (
    df.filter(pl.col("housing_median_age") > 25)
      .select(["longitude", "latitude"])
      .collect()
)