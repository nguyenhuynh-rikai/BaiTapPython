import itertools

arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
arr3 = [7, 8, 9]

arr4 = itertools.chain(arr1, arr2, arr3)

print(list(arr4))