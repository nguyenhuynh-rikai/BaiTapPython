import sysconfig

n = [1, 2, 3]
def solve(n):
    ans = []
    for i in n:
        ans.append(i * i)
    return ans

n = solve(n)
print(n)