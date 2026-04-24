import pandas as pd

df = pd.DataFrame({
    "a": [1, 5, 3],
    "b": [2, 2, 4]
})

result = df.query("a > b")
print(result)