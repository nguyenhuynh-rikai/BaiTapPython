arr = [1, 2, 3, 4]
n = 2

def slide_win(arr, n):
    result = []
    for i in range(len(arr) - 1):
        if arr[i] == arr[i+1] - 1:
            result.append([arr[i], arr[i+1]])
    return result

print(slide_win(arr, n))