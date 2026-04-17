n = ['apple', 'bat', 'ant']

def solve(n):
    res = {}
    for x in n:
        if x[0] not in res:
            res[x[0]] = []
        res[x[0]].append(x)
    return res

print(solve(n))