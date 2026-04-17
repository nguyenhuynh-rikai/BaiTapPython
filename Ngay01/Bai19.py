from unittest import result
arr = [1, 2, 3], [2, 3, 4]

def list_in(arr):
    result = []
    for i in arr[0]:
        for j in arr[1]:
            if i == j:
                result.append(i)
    return result

print(list_in(arr))