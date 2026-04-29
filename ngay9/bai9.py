import polars as pl

df = pl.read_csv("data/transactions.csv")

df = df.with_columns(
    pl.col("category")
    .str.strip_chars()
    .str.to_lowercase()
    .alias("category_clean")
)

print(df)