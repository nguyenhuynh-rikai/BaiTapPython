import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C", "D"],
    "age": [20, 25, 30, 35]
})

df.to_csv("save.csv", index=False)