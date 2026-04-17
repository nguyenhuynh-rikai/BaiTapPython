arr = [1, 2, 3], [2, 3, 4]

def solve(arr):
    res = []
    for x in arr[0]:
        for y in arr[1]:
            if x == y:
                res.append(x)
    return res

print(solve(arr))