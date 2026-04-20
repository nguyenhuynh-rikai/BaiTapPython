def admin_required(func):
    def wrapper(*args, **kwargs):
        user = args[0]
        if user['role'] != 'admin':
            print("permission denined")
        else:
            return func(*args, **kwargs)
    return wrapper

@admin_required
def log(user):
    return log

log({'role': 'guest'})