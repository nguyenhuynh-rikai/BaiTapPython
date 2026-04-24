import pandas as pd

df = pd.DataFrame({
    "gender": ["Male", "Female", "Male", "Female", "Male"],
    "product": ["A", "A", "B", "B", "A"]
})

ct = pd.crosstab(df["gender"], df["product"])

print(ct)