from functools import wraps


def add_doc(extra_text):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        original_doc = func.__doc__ or ""
        wrapper.__doc__ = original_doc + "\n" + extra_text
        return wrapper
    return decorator

@add_doc("This function has been modified by the decorator")
def run():
    """This is original function"""
    pass

help(run)