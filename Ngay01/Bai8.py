arr = [1, 2, 3, 4, 5]
n = 2

def chunking_list(arr, n):
    result = []
    sub = []
    count = 0
    for i in arr:
        if count == n:
            result.append(sub)
            sub = []
            count = 0
        sub.append(i)
        count += 1
    result.append(sub)
    return result

print(chunking_list(arr, n))
