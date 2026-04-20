def deprecated(func):
    def wrapper(*args, **kwargs):
        print(f"Warning: Function {func.__name__} is deprecated")
        return func(*args, **kwargs)
    return wrapper

@deprecated
def add(x,y):
    return x+y

print(add(3,4))
