regis = []

def register(func):
    regis.append(func)
    return func

@register
def play_music():
    return "dang phat.."

@register

def stop_music():
    return "da dung..."
@register

def next_track():
    return "da chuyen..."

print("\nSố lượng hàm trong registry:", len(regis))
print("Danh sách các hàm đã đăng ký:", [f.__name__ for f in regis])
