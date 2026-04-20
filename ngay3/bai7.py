class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, score):
        super().__init__(name)
        self.score = score


s = Student("An", 9)
print(s.name)
print(s.score)