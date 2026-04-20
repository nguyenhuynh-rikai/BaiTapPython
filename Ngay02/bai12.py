def double_return(func):
    def wrapper(*args,**kwargs):
        res = func(*args,**kwargs)
        if isinstance(res, (int,float)):
            return res*2
        return res
    return wrapper

@double_return
def add(x,y):
    return x+y
print(add(3,4))