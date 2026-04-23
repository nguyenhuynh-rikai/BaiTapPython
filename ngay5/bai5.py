def infinite_cycle(arr):
    while True:
        for x in arr:
            yield x

arr = [1, 2]; count = 5
gen = infinite_cycle(arr)
for _ in range(count):
    print(next(gen), end=" ")