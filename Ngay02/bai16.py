def add_doc(func):
    extra_info = "hahaha"

    if func.__doc__:
        func.__doc__ = func.__doc__ + extra_info
    else:
        func.__doc__ = extra_info
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

@add_doc
def calculate_sum(a,b):
    return a+b

help(calculate_sum)
