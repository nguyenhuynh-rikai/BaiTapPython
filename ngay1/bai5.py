n = [1, [2, [3, 4]], 5]

def solve(n):
    n2 = []
    for x in n:
        if type(x) == list:
            n2.extend(solve(x))
        else:
            n2.append(x)
    return n2

n = solve(n)
print(n)
