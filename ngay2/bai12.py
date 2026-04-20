from functools import wraps

def double(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, (int, float)):
            return result * 2
        else: print(f"Kết quả ra về của hàm {func.__name__} phải là số.")
        return result
    return wrapper

@double
def run():
    return 5

print(run())