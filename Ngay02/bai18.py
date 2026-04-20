def decor_func(func):
    def wrapper():
        return func()
    return wrapper

@decor_func
def show_text(infor):
    return infor

print(show_text("Nguyen Huynh"))