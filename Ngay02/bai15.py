import time

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"đang chạy hàm: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"time chạy: {end - start: f}s ")
        return result
    return wrapper

@logger
@timer
def add_slow(a,b):
    time.sleep(10)
    return a + b

print(add_slow(10,20))