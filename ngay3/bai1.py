class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_passed(self):
        return self.score >= 5

s = Student("An",9)
print(s.name)
print(s.score)

s1 = Student("An", 9)
print(s1.is_passed())