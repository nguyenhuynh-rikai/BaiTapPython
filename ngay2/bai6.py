def authorization_check(func):
    def wrapper(user, *args, **kwargs):
        if user['role'] != 'admin': print("Permission Denied"); return
        return func(*args, **kwargs)
    return wrapper

@authorization_check
def input(user):
    return user

input({'role': 'guest'})