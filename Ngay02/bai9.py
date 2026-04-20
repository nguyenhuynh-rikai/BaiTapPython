def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class MyClass:
    def __init__(self, name):
        self.name = name
        print(f"Khởi tạo thực thể cho: {self.name}")

obj1 = MyClass("Nguyên")

obj2 = MyClass("Hùng")

print(f"Tên của obj2 là: {obj2.name}")
print(f"Hai đối tượng là một: {obj1 is obj2}")

