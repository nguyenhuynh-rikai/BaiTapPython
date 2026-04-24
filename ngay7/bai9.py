import pandas as pd

df = pd.DataFrame({
    "email": ["a@gmail.com", "b@yahoo.com", "c@gmail.com"]
})

df["is_gmail"] = df["email"].str.contains("gmail")
print(df)
df["new_gmail"] = df["email"].str.replace("gmail", "new")
print(df)