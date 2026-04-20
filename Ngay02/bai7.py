import time

def rate_limiter(max_calls, period):
    def decorator(func):
        history = []

        def wrapper(*args, **kwargs):
            now = time.time()

            nonlocal history
            history = [t for t in history if now - t < period]

            if len(history) < max_calls:
                history.append(now)
                return func(*args, **kwargs)
            else:
                return f"Too many requests."

        return wrapper
    return decorator


@rate_limiter(max_calls=2, period=1)
def my_func():
    return "Thành công"

for i in range(10):
    print(my_func())