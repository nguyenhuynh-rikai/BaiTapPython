arr = [1, 2, 3, 4]
n = 2

def solve(arr, n):
    res = []
    for i in range(len(arr) - 1):
        if arr[i] == arr[i+1] - 1:
            res.append([arr[i], arr[i+1]])
    return res

print(solve(arr, n))
