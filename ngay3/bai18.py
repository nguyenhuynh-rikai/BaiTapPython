class Phone:
    def __init__(self, number):
        self.number = number

    def __call__(self, value):
        return f'{self.number} is {value}'

my_obj = Phone("1")
print(my_obj(5))