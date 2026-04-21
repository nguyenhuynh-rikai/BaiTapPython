class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __gt__(self, other):
        return self.price > other.price

product1 = Product("Apple", 100)
product2 = Product("Banana", 200)

print(product1.__gt__(product2))
