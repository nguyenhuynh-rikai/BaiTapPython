def argument_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Args: ({args}), Kwargs: ({kwargs})")
        return func(*args, **kwargs)
    return wrapper

@argument_logger
def add(x, y, a = 0):
    return x + y + a

add(1, 2, a = 3)