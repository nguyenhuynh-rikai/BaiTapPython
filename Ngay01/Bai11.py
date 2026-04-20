arr = ['eat', 'tea', 'tan', 'nat']

def anagram_grouping(arr):

    res = []
    for i in range(len(arr) - 1):
        sub = []
        for j in range(i + 1, len(arr)):
            if(sorted(arr[i]) == sorted(arr[j])):
                sub.append(arr[i])
                sub.append(arr[j])
        
        res.append(sub)
    return res
print(anagram_grouping(arr))