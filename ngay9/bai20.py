import pandas as pd
import polars as pl
import time

file_path = "data/users.csv"

start = time.time()
df_pd = pd.read_csv(file_path)
res_pd = df_pd.groupby("city").agg({"income": "mean", "age": "max"})
pd_time = time.time() - start
print(f"Pandas: {pd_time:.4f}s")

start = time.time()
df_pl = pl.read_csv(file_path)
res_pl = df_pl.group_by("city").agg([
    pl.col("income").mean(),
    pl.col("age").max()
])
pl_time = time.time() - start
print(f"Polars: {pl_time:.4f}s")

print(f"==> Polars nhanh hơn khoảng {pd_time/pl_time:.1f} lần")