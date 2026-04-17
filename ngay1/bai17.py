inp = ['a', 'b', 'a']

def solve(inp):
    res = {}
    for x in inp:
        if x not in res:
            res[x] = 1
        else:
            res[x] += 1
    return res

print(solve(inp))