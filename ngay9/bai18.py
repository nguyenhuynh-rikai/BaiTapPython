import polars as pl
import os

print("Default threads:", pl.thread_pool_size())

os.environ["POLARS_MAX_THREADS"] = "4"

df = pl.DataFrame({
    "a": range(1_000_000),
    "b": range(1_000_000)
})

result = df.select(
    (pl.col("a") + pl.col("b")).alias("sum")
)

print(result.head())