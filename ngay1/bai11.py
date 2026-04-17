inp = ['eat', 'tea', 'tan', 'nat']


def solve(inp): 
    res = []
    for i in range(len(inp) - 1):
        sub = []
        for j in range(i + 1, len(inp)):
            if sorted(inp[i]) == sorted(inp[j]):
                sub.append(inp[i])
                sub.append(inp[j])
        if(sub != []):
            res.append(sub)
    return res

print(solve(inp))
