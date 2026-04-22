import logging
from functools import wraps

logging.basicConfig(
    level=logging.DEBUG,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error in function: {func.__name__}")
    return wrapper

@log_exception
def run(a, b):
    return a / b

run(10, 0)