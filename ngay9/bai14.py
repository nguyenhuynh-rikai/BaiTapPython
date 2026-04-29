import polars as pl
import numpy as np
import pandas as pd

df = pl.DataFrame({
    "a": [1, 2, 3],
    "b": [4, 5, 6]
})

pdf = df.to_pandas()
print(type(pdf))
pdf = pd.DataFrame({
    "a": [1, 2, 3],
    "b": [4, 5, 6]
})

df = pl.from_pandas(pdf)
print(type(df))

arr = df.to_numpy()
print(arr)
arr = np.array([[1, 4], [2, 5], [3, 6]])

df = pl.DataFrame(arr, schema=["a", "b"])