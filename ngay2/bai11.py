import warnings
from functools import wraps

def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"Function {func.__name__} is deprecated.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)
    return wrapper

@deprecated
def run():
    print("Hello world")

run()