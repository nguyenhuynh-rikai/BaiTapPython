import pandas as pd

df = pd.DataFrame({
    "name": ["An", "Binh", "An"],
    "age": [20, 21, 20]
})
print(df["age"].dtype)
print(df.memory_usage(deep=True))

df["age"] = df["age"].astype("category")


print(df["age"].dtype)
print(df.memory_usage(deep=True))