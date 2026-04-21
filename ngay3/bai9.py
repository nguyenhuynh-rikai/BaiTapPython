class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

v1 = Vector(1,2)
v2 = Vector(3,4)
result = v1 + v2
print(result.x)
print(result.y)