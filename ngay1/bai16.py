a = [1, 2], ['a', 'b']

def solve(a):
    res = []
    for x in a:
        res.append(tuple(x))
    return res

print(solve(a))