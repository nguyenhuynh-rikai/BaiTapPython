words = ['apple', 'bat', 'ant']

def group_prefix(words):
    result = {}
    for i in words:
        prefix = i[0]
        result[prefix] = result.get(prefix, []) + [i]
    return result

print(group_prefix(words))