import time
from functools import wraps

def delay(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Cho {seconds} giay truoc khi thuc thi...")
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@delay(5)
def run(x):
    print("Hello world")

run(6)