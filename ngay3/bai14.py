class Camera:
    def __init__(self):
        pass

    def take_photo(self):
        return "take photo"

class Phone:
    def __init__(self):
        pass

    def call(self):
        return "call"

class SmartPhone(Camera, Phone):
    def __init__(self):
        super().__init__()
        pass

sp = SmartPhone()

print(sp.take_photo())
print(sp.call())


