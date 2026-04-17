d1= {'a': 10, 'b': 5}
d2 = {'a': 5, 'c': 1}

def solve(d1, d2):
    d3 = d1.copy()
    for k, v in d2.items():
        if k in d3:
            d3[k] += v
        else:
            d3[k] = v
    return d3

print(solve(d1 ,d2))