class User:
    def __init__(self, role, id):
        self.role = role
        self.id = id

    def __str__(self):
        return f"User: {self.role} (ID: {self.id})"

user = User("Admin", 1)
print(user)