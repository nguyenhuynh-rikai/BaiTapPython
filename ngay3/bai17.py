class Car:
    def __init__(self):
        pass

    class Engine:
        def __init__(self):
            pass

        def start(self):
            return "Engine start"

car = Car()
print(car.Engine().start())