import polars as pl

df = pl.DataFrame({
    "a": [1, 2, 3],
    "b": [10, 20, 30]
})

pdf = df.to_pandas()

print(type(pdf))
print(pdf)