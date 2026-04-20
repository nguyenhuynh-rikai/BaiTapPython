import time
from functools import wraps

def rate_limiter(max_calls, period):
    def decorator(func):
        call_times = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_times
            now = time.time()
            call_times = [t for t in call_times if now - t < period]
            if len(call_times) >= max_calls:
                print("Too many requests")
                return
            call_times.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limiter(max_calls=2, period=1)
def my_func():
    print("Function called")

for _ in range(10):
    my_func()