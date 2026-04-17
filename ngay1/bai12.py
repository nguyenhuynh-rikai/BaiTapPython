inp = {'apple': 10, 'orange': 5, 'banana': 12}

def solve(inp):
    return dict(sorted(inp.items(), key= lambda x: x[1]))

print(solve(inp))