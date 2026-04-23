import pandas as pd

data = [
    {'product': 'Laptop', 'price': 1200, 'stock': 5},
    {'product': 'mouse', 'price': 10, 'stock': 7},
    {'product': 'kb', 'price': 30, 'stock': 1},
]

df = pd.DataFrame(data)

print(df)