import pandas as pd

data = [
    {
        "name": "A",
        "info": {"age": 20, "city": "Hanoi"}
    },
    {
        "name": "B",
        "info": {"age": 30, "city": "HCMC"}
    }
]

df = pd.DataFrame(data)

df_flat = pd.json_normalize(df["info"])

df_final = pd.concat([df["name"], df_flat], axis=1)

print(df_final)