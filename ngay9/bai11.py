import polars as pl

df = pl.DataFrame({
    "group": ["A", "A", "B", "B", "B"],
    "values": [1, 2, 3, 4, 5]
})

df_list = df.group_by("group").agg(pl.col("values"))

print(df_list.with_columns(
    sorted = pl.col("values").list.sort(descending=True),
    reversed = pl.col("values").list.reverse()
))

print(df_list.with_columns(
    unique_vals = pl.col("values").list.unique()
))

print(df_list.with_columns(
    processed = pl.col("values").list.eval(pl.element() * 2).list.eval(pl.element().filter(pl.element() > 5))
))