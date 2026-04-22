def fibonacci():
    a,b = 0,1
    while True:
        yield a
        a,b = b,a+b

gen = fibonacci()
for i in range(100):
    print(next(gen))