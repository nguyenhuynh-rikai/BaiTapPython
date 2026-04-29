import polars as pl
import pandas as pd
import numpy as np
import time

data = {
    "name": ["An", "Binh", "Cuong"],
    "age": [25, 30, 35],
    "salary": [1000, 1500, 2000]
}

df_pl = pl.DataFrame(data)
print(df_pl)

n = 1_000_000

data = {
    "a": np.random.rand(n),
    "b": np.random.rand(n)
}
start = time.time()

df_pd = pd.DataFrame(data)
df_pd["c"] = df_pd["a"] + df_pd["b"]

print("Pandas time:", time.time() - start)

start = time.time()

df_pl = pl.DataFrame(data)
df_pl = df_pl.with_columns((pl.col("a") + pl.col("b")).alias("c"))

print("Polars time:", time.time() - start)