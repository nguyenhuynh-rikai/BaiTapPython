def infinite_cycle(lst, count):
    res = 0
    while True:
        for i in lst:
            yield i
            res += 1
            if res >= count:
                return res

gen = infinite_cycle([1, 2], 5)
for x in gen:
    print(x)