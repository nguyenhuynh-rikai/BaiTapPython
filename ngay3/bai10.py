class Shelf:
    def __init__(self):
        self.items = []

    def add(self, items):
        self.items.append(items)

    def __len__(self):
        return len(self.items)

my_shelf = Shelf()
my_shelf.add("book")
my_shelf.add("pen")
print(len(my_shelf))