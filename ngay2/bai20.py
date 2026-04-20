registry_list = []

def register(func):
    registry_list.append(func)

@register
def func_a():
    return "Function A"

@register
def func_b():
    return "Function B"

@register
def func_c():
    return "Function C"

print(registry_list)