import time

def simple_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Thời gian: {end - start:.2f}s")
        return result
    return wrapper

@simple_timer
def sleep_1s():
    time.sleep(1)

sleep_1s()