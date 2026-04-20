import logging
import time
from functools import wraps

logging.basicConfig(level=logging.INFO)

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Call {func.__name__} with args = {args}, kwargs = {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@timer
@logger
def run(x):
    time.sleep(1)
    return x * 3

print(run(5))