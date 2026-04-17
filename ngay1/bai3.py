import sys

n = [3, 1, 2, 3, 4, 1]
def solve(n):
    n2 = []
    for i in n:
        if i not in n2:
            n2.append(i)
    return n2
n = solve(n)
print(n)