import pandas as pd

df = pd.DataFrame({
    "gender": ["Male", "Female", "Male", "Female", "Male"],
    "product": ["A", "A", "B", "B", "A"]
})

df["product"] = df["product"].map(lambda x: "Apple" if x == "A" else "Orange", na_action="ignore")

print(df)

# df["product"] = df["product"].replace({"A": "Apple", "O": "Orange"})

# print(df)