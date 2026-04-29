import polars as pl

df = pl.scan_csv("data/users.csv")
print(type(df))