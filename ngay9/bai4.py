import polars as pl
import time
# start = time.time()
# df = pl.DataFrame({
#     "name": ["An", "Binh", "Cuong"],
#     "age": [22, 30, 35],
#     "salary": [1000, 2000, 3000]
# })
#
# result = (
#     df.filter(pl.col("age") > 25)
#       .with_columns((pl.col("salary") * 1.1).alias("new_salary"))
#       .select(["name", "new_salary"])
# )
# print("Chaining: ", time.time() - start)

start = time.time()
df = pl.DataFrame({
    "name": ["An", "Binh", "Cuong"],
    "age": [22, 30, 35],
    "salary": [1000, 2000, 3000]
})

df = df.with_columns(
    (pl.col("salary") * 1.1).alias("new_salary")
)
print("Expression API: ", time.time() - start)

