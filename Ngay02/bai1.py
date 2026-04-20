import time

def time_decorate(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, ** kwargs)
        end_time = time.time()
        excution_time = end_time - start_time
        print(f"Thời gian: {excution_time:.2f}s")
        return res
    return wrapper

@time_decorate
def time_sleep():
    time.sleep(1)
    return time_sleep

time_sleep()    