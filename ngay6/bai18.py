import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C"],
    "age": [20, 25, 30]
}, index=["x", "y", "z"])

print(df.loc["x"])

print(df.loc["x":"y"])

print(df.loc["x", "age"])

print(df.iloc[0])

print(df.iloc[0:2])

print(df.iloc[0, 1])