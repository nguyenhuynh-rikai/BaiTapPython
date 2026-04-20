def c_to_f(func):
    def wrapper(c):
        f = c * 1.8 +32
        return func(f)
    return wrapper

@c_to_f
def c(x):
    return x

print(c(30))