def except_wrap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)

    return wrapper
@except_wrap
def divide(x,y):
    return x/y

print(divide(10,0))