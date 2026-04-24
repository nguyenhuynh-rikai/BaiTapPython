import pandas as pd

df1 = pd.read_csv('datawide.csv')

df_melt = df1.melt(
    id_vars='region',
    var_name='month',
    value_name='revenue'
)


print(df_melt)