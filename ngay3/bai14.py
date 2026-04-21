class Camera:
    def __init__(self):
        pass

    def take_photo(self):
        return "take_photo"

class Phone:
    def __init__(self):
        pass

    def call(self):
        return "call"

class Smartphone(Phone, Camera):
    def __init__(self):
        super().__init__()
        pass

sp = Smartphone()
print(sp.take_photo())
print(sp.call())