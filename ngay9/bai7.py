import polars as pl

users = pl.scan_csv("data/users.csv")
orders = pl.scan_csv("data/events.csv")

result = (
    users.join(orders, on="user_id", how="inner")
         .select(["user_id", "city", "device"])
         .collect()
)

print(result)