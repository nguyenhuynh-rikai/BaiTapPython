def result_catch(func):
    cache = {}
    def wrapper (*args):
        if args in args:
            return func(*args)

        res = func(*args)

        cache[args] = res
        return res
    return wrapper

@result_catch
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
