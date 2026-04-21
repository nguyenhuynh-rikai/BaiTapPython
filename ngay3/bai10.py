class Shelf:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

my_shelf = [1, 2, 3, 4, 5]

print(len(my_shelf))