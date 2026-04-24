import pandas as pd

df = pd.DataFrame({
    "region": ["N", "S", "N", "S"],
    "product": ["A", "B", "A", "B"]
})

region_map = {
    "N": "North",
    "S": "South"
}

df["region_full"] = df["region"].map(region_map)

df_replace = df.replace({
    "N": "North",
    "S": "South",
    "A": "Apple",
    "B": "Banana"
})

print(df)

print(df_replace)