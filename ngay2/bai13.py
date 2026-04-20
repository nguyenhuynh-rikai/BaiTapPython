from functools import wraps


def exception_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None

    return wrapper

@exception_wrapper
def run():
    return 5/0

print(run())