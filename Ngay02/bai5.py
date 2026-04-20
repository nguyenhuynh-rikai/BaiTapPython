def argument_log(func):
    def wrapper(*args, ** kwargs):
        print(f"Log Args:{args}, Kwargs:{kwargs}")
        return func(*args, ** kwargs)

    return wrapper

@argument_log
def greet(c,b, a=100 ):
    return c+b+a

greet(1,2, a = 3 )