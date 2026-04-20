def retry_logic(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Lỗi: {e}")
    return wrapper

@retry_logic
def divide(a, b):
    return a / b

divide(1, 0)