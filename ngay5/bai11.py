import timeit

time_list = timeit.timeit("[x*x for x in range(10)]", number=10000000)
print(f"Time list: {time_list}")

time_generator = timeit.timeit("(x*x for x in range(10))", number=10000000)
print(f"Time generator: {time_generator}")