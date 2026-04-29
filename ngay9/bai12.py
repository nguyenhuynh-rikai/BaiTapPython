import polars as pl

df = pl.DataFrame({
    "user_id": [1, 2, 3],
    "name": ["An", "Binh", "Chi"],
    "info": [
        {"age": 20, "city": "Da Nang"},
        {"age": 25, "city": "Hanoi"},
        {"age": 30, "city": "HCM"}
    ]
})

df = df.unnest("info")

df = df.with_columns(
    (pl.col("age") < 25).alias("is_young")
)

df_filtered = df.filter(pl.col("age") > 25)

print(df)
print(df_filtered)