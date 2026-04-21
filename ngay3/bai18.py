class Phone:
    def __call__(self, *args, **kwargs):
        return args[0] * 10


my_obj = Phone()
print(my_obj(5))