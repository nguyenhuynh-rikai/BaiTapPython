class myRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        x = self.current
        self.current = self.current + 1
        return x

b = iter(myRange(5,10))

print(next(b))
print(next(b))
print(next(b))
