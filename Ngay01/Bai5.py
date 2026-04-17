arr = [1, [2, [3, 4]], 5]

def recursion(arr):
    arr2 = []
    for i in arr:
        if type(i) == list:
            arr2.extend(recursion(i))
        else:
            arr2.append(i)
    return arr2

arr = recursion(arr)
print(arr)
