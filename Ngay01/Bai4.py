arr = [[1, 2], [3, 4], [5]]

def chuyen_mang(arr):
    arr2 = []
    for i in arr:
        for j in i:
            arr2.append(j)
    return arr2

arr = chuyen_mang(arr)
print(arr)
