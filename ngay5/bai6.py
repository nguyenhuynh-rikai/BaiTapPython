arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def filter_generator(arr):
    for x in arr:
        if x % 2 == 0:
            yield x

def map_generator(arr):
    for x in arr:
        yield x * x


pipeline = filter_generator(arr)
pipeline = map_generator(pipeline)
res = sum(pipeline)

print(res)