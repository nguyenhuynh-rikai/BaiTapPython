def type_validator(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, int):
                print("TypeError")
                return None
        return func(*args, **kwargs)
    return wrapper

@type_validator
def add(s):
    return s

add("Hello world")