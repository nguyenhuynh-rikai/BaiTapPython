import time

def delay(seconds):
    def deco(func):
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return deco
@delay(seconds=2)
def add(x,y):
    return x+y

print(add(3,4))
