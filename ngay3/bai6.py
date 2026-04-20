class Dog:
    def __init__(self, age):
        self.age = age

    def speak(self):
        print("Woof")

class Cat:
    def __init__(self, age):
        self.age = age
    def speak(self):
        print("Meo")

dog = Dog(5)
dog.speak()