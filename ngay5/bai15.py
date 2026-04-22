def gen():
    yield from [1, 2, 3]
    yield from [4, 5]

print(list(gen()))