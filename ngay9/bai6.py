import pandas as pd
import polars as pl
import numpy as np
import time

n = 10_000_000

data = {
    "category": np.random.choice(["A", "B", "C", "D"], n),
    "value": np.random.rand(n) * 100
}

start = time.time()

df_pd = pd.DataFrame(data)

result_pd = (
    df_pd.groupby("category")["value"]
         .agg(["sum", "mean"])
)

print("Pandas time:", time.time() - start)

start = time.time()

df_pl = pl.DataFrame(data)

result = (
    df_pl.group_by("category")
         .agg([
             pl.col("value").sum().alias("total_value"),
             pl.col("value").mean().alias("avg_value")
         ])
)

print("Polars time:", time.time() - start)

# start = time.time()
#
# df_pl = pl.DataFrame(data).lazy()
#
# result_lazy = (
#     df_pl.group_by("category")
#          .agg([
#              pl.col("value").sum().alias("total_value"),
#              pl.col("value").mean().alias("avg_value")
#          ])
#          .collect()
# )
#
# print("Polars Lazy time:", time.time() - start)