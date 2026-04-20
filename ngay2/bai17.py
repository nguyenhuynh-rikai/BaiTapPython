from functools import wraps


def convert(func):
    @wraps(func)
    def wrapper(x, *args, **kwargs):
        x_f = x * 9/5 + 32
        return func(x_f, *args, **kwargs)
    return wrapper

@convert
def run(x):
    return x

print(run(30))