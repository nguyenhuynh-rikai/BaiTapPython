class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    @staticmethod
    def is_adult(age):
        if age >= 18:
            return True
        else:
            return False

print(Person.is_adult(20))

