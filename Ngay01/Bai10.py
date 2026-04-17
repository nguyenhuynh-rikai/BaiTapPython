nums=[2, 7, 11]
target = 9

def two_sum(nums):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i,j]

print(two_sum(nums))