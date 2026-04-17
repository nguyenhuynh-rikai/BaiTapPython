import sys

n = [1, 2, 3, 4, 5]

def solve(n):
    n2 = []
    for i in n:
        if i % 2 == 0:
            n2.append(i)
    return n2

n = solve(n)
print(n)