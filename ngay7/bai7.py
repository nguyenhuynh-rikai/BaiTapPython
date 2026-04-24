import pandas as pd

df = pd.DataFrame({
    "name": ["An", "Binh"],
    "math": [8, 7],
    "english": [9, 6]
})

df_melt = pd.melt(
    df,
    id_vars=["name"],
    value_vars=["math", "english"],
    var_name="subject",
    value_name="score"
)

print(df_melt)