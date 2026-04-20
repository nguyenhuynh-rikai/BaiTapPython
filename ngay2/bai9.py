def single_instance(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@single_instance
class User:
    pass

a = User()
b = User()

print("Dia chi vung nho cua a la: " + str(id(a)))
print("Dia chi vung nho cua b la: " + str(id(a)))
