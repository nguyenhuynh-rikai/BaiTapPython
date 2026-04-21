class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __gt__(self, other):
        return self.price > other.price

prod1 = Product("P1", 100)
prod2 = Product("P2", 50)

print(prod1.__gt__(prod2))