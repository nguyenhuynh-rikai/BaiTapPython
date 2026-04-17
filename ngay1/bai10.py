nums=[2, 7, 11]
target=9

def solve(nums, target):
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None

print(solve(nums, target))