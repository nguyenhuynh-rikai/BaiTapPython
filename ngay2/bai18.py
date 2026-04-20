from functools import wraps

def indentity_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@indentity_decorator
def run():
    return 42
print(run())
