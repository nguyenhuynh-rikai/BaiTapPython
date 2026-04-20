class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_passed(self):
        return self.score >= 5

s = Student("An", 9)

print(s.name)

s2 = Student("Binh", 4.5)

print(s2.is_passed())