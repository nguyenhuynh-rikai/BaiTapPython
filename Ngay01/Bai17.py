arr =  ['a', 'b', 'a']

def count_num(arr):
    count = {}
    for i in arr:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return count
print(count_num(arr))
            