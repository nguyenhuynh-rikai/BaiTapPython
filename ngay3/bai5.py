class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def drive(self):
        print("Vehicle is moving")

class Car(Vehicle):
    def drive(self):
        super().drive()

car = Car("BMW", "A")
car.drive()