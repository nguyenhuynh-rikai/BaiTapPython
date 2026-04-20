import os

def debug_mode(func):
    def wrapper(*args, **kwargs):
        is_debug = os.getenv('DEBUG') == 'True'

        if is_debug:
            print(func.__name__, args, kwargs)

        return func(*args, **kwargs)
    return wrapper

@debug_mode
def add(x, y):
    return x + y

os.environ["DEBUG"] = "True"
print(add(1, 2))

print("-" *20)