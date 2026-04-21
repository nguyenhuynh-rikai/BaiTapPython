class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return f"User: {self.name} (ID:  {self.id})"

u = User("Admin", 1)
print(u)