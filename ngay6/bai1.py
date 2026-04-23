import pandas as pd

data = [
    {"name": "Thanh", "age": 22, "city": "Da Nang"},
    {"name": "An", "age": 25, "city": "Ha Noi"},
    {"name": "Binh", "age": 20, "city": "Sai Gon"}
]

df = pd.DataFrame(data)

print(df)