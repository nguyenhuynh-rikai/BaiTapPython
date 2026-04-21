class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, string):
        name, age = string.split("-")
        return cls(name, int(age))

    def __str__(self):
        return f"{self.name} ({self.age})"

p = Person.from_string("Binh-25")

print(str(p))