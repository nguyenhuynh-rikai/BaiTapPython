class User:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name" : self.name}

user = User('A')
print(user.to_dict())