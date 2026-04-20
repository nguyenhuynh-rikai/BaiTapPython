import os
from functools import wraps

def debug_mode(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        debug = os.getenv("DEBUG", "False") == "True"

        if debug:
            print(f"[DEBUG] Call function {func.__name__}")
            print(f"[DEBUG] args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)
        if debug:
            print(f"[DEBUG] result={result}")
        return result
    return wrapper

@debug_mode
def run(a, b):
    return a * b

print(run(3, 6))