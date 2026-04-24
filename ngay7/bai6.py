import pandas as pd

df = pd.DataFrame({
    "region": ["North", "North", "South", "South"],
    "product": ["A", "B", "A", "B"],
    "revenue": [100, 200, 150, 250]
})

pivot = pd.pivot_table(
    df,
    values="revenue",
    index="region",
    columns="product",
    aggfunc="sum"
)

print(pivot)