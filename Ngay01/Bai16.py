a =  [1, 2]
b =  ['a', 'b']

def zip_re(a,b):
    result = []
    n = min(len(a), len(b))
    for i in range(n):
        result.append((a[i], b[i]))
    return result

print(zip_re(a,b))