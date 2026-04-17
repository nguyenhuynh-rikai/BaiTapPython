from unittest import result
input = {'a': 1, 'b': 2}

def dict_inver(input):
    result = {}
    for k,v in input.items():
        result[v] = k
    return result
print(dict_inver(input))