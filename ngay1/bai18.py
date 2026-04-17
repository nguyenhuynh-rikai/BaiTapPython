inp = [1, 2, 4, 5]

def solve(inp):
    res = []
    for i in range(inp[0], inp[len(inp) - 1],1):
        if i not in inp:
            res.append(i)
    return res

print(solve(inp))