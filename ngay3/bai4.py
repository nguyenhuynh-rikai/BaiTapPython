class Person:
    def __init__(self, age):
        self.age = age

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError('Age must be positive')
        self._age = value

p = Person(20)
print(p.age)
p.age = -5