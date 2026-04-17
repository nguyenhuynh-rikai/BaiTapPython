arr = [1, 2, 3, 4, 5]
n = 2

def solve(arr, n):
    res = []
    sub = []
    cnt = 0
    for x in arr:
        if cnt == n:
            res.append(sub)
            sub = []
            cnt = 0
        sub.append(x)
        cnt += 1
    res.append(sub)
    return res

print(solve(arr, n))

        