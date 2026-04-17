n = [[1, 2], [3, 4], [5]]

def solve(n):
    n2 = []
    for i in n:
        for j in i:
            n2.append(j)
    return n2

n = solve(n)
print(n)