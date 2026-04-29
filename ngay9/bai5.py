import polars as pl

df = pl.DataFrame({
    "name": ["An", "Binh", "Cuong"],
    "age": [22, 30, 35],
    "salary": [1000, 2000, 3000]
})

print(df.filter(pl.col("age") > 25))

print(df.select(["name", "salary"]))