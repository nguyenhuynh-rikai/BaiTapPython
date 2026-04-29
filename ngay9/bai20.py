import pandas as pd
import polars as pl
import time

N = 1_000_000

pdf = pd.DataFrame({
    "a": range(N),
    "b": range(N)
})

start = time.time()
pdf["sum"] = pdf["a"] + pdf["b"]
pandas_time = time.time() - start

df = pl.DataFrame({
    "a": range(N),
    "b": range(N)
})

start = time.time()
df = df.with_columns(
    (pl.col("a") + pl.col("b")).alias("sum")
)
polars_time = time.time() - start

print(f"Pandas time: {pandas_time:.4f} seconds")
print(f"Polars time: {polars_time:.4f} seconds")