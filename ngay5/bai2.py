import sys

large_list = range(1000000)

upper_list = [x*x for x in range(1000000)]

upper_gen = (x*x for x in range(1000000))

print(sys.getsizeof(upper_list))
print(sys.getsizeof(upper_gen))

