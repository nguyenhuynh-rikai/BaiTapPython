import timeit

time_list = timeit.timeit("[x*x for x in range(10)]",number=10000)
print(time_list)

time_generator = timeit.timeit("(x*x for x in range(10)) ",number=10000)
print(time_generator)