class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, data):
        name, age = data.split('-')
        return cls(name, int(age))

person = Person.from_string("Binh-25")

print(type(person))