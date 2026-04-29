import polars as pl

df = pl.DataFrame({
    "id": [1, 2],
    "info": [
        {"name": "Thanh", "age": 22},
        {"name": "An", "age": 25}
    ]
})

print(df)

print(df.select(
    pl.col("info").struct.field("name")
))

df = pl.DataFrame({
    "name": ["Thanh", "An"],
    "age": [22, 25]
})

df = df.with_columns(
    pl.struct(["name", "age"]).alias("info")
)

print(df)