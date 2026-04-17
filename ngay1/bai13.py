data=[{'val': 10}, {'val': 50}]
key='val'


def solve(data, key):
    mx = list(data[0].values())[0]
    for x in data:
        if list(x.keys())[0] == key and list(x.values())[0] > mx:
            mx = list(x.values())[0]
    return mx

print(solve(data, key))