data = {"name": "Binh", "age": 25}

try:
    print(data["address"])
except KeyError:
    print("Key not found!")