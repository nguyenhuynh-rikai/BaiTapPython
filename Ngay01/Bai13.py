data=[{'val': 10}, {'val': 50}]
key='val'

def Max_dicts(data, key):
    if not data:
        return None
    max_val = None
    for i in data:
        if key in i:
            v = i[key]
            if max_val is None or v > max_val:
                max_val = v
    return max_val

print(Max_dicts(data, key))
