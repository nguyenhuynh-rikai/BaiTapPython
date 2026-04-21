class User:
    count = 0

    def __init__(self):
        User.count += 1
u1 = User()
u2 = User()
u3 = User()

print(User.count)