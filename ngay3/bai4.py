class Person:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("loi")
        self.__age = value

p = Person(25)
print(p.age)   # đọc như attribute
p.age = -5     # phải ra ValueError