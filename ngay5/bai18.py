import itertools

arr = [1,2,3,4,5,6,7,8,9,10]

arr2 = itertools.filterfalse(lambda x: x<5, arr)

print(list(arr2))