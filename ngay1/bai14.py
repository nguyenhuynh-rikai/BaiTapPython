s = 'hello world'

def string_reversal(s):
    res = []
    arr = s.split(' ')
    arr = sorted(arr, reverse=True)
    for x in arr:
        res.append(x[::-1])
    return ' '.join(res)

print(string_reversal(s))