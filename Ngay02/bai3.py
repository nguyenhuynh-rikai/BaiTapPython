def type_check(func):
    def wrapper(*args, **kwargs):
        for i in args:
            if not isinstance(i, int):
                raise TypeError("errol")
        return func(*args, **kwargs)
    return wrapper

@type_check
def add(a,b):
    return a + b

print(add(1,"3"))