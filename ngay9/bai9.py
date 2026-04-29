import polars as pl

df = pl.DataFrame({
    "text": ["Hello World              ", "Polars Fast", "DATA"]
})

print(df.select(pl.col("text").str.to_lowercase()))
print(df.select(pl.col("text").str.to_uppercase()))

print(df.select(pl.col("text").str.len_chars()))

print(df.select(pl.col("text").str.strip_chars()))

print(df.filter(pl.col("text").str.contains("Polars")))