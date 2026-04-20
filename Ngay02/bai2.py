def retry_logic(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, ** kwargs)
            except Exception as e:
                if i == 2:
                    print(f"test lần {i+1} vẫn lỗi. Dừng")
                else:
                    print(f"test lần {i+1} lỗi. Thử lại")
    return wrapper

@retry_logic
def test_errol(a,b):
    return a / b

test_errol(1,0)