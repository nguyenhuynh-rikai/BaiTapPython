import pandas as pd
import polars as pl
import time

N = 1_000_000

data = {
    "id": list(range(N)),
    "age": [i % 50 + 20 for i in range(N)],
    "salary": [i * 100 for i in range(N)]
}

# Pandas
start = time.time()
df_pd = pd.DataFrame(data)
df_pd["age_plus"] = df_pd["age"] + 10
print("Pandas time:", time.time() - start)

# Polars
start = time.time()
df_pl = pl.DataFrame(data)
df_pl = df_pl.with_columns(
    (pl.col("age") + 10).alias("age_plus")
)
print("Polars time:", time.time() - start)