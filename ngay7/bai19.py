import pandas as pd

df = pd.DataFrame({
    "name": ["A", "B", "C", "D"],
    "age": [20, 30, 25, 35],
    "salary": [1000, 2000, 1500, 3000]
})

res = df.query("age > 25 and salary > 1500")

print(res)

