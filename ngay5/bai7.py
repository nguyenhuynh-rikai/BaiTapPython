my_list = [1, 2, 3]
it = iter(my_list)
try:
    print(next(it))
    print(next(it))
    print(next(it))
    print(next(it))
except StopIteration:
    print("StopIteration")


