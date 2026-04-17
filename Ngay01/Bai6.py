d1= {'a': 10, 'b': 5}
d2= {'a': 5, 'c': 1}

def merge_sum(*dicts):
    reuslt = {}
    for d in dicts:
        for i,j in d.items():
            reuslt[i]=reuslt.get(i,0) + j
    return reuslt

d = merge_sum(d1, d2)
print(d)