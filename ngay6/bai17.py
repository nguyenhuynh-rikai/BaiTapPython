import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

df.plot(x="median_income", y="median_house_value", kind="scatter")
plt.show()