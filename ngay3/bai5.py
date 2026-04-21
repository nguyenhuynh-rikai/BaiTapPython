class Vehicle:
    def drive(self):
        print("Vehicle is moving")

class Car(Vehicle):
    pass

car = Car()
car.drive()