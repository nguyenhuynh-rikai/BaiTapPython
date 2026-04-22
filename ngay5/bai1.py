class MyRange:
    def __init__(self, start, stop):
        self.current = start
        self.end = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

for i in MyRange(0,5):
    print(i)