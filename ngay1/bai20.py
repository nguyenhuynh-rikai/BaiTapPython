inp = {'a': 1, 'b': 2}

def solve(inp):
    res = {}
    for k, v in inp.items():
        res[v] = k
    return res

print(solve(inp))