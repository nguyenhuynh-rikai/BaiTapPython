arr = [1, 2, 4, 5]

def find_miss(arr):
    find = []
    for i in range(arr[0], arr[len(arr)-1],1):
        if i not in arr:
            find.append(i)
    return find

print(find_miss(arr))