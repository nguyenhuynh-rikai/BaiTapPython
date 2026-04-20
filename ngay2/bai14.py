def make_adder(x):
    def adder(y):
        return x + y
    return adder

add_five = make_adder(5)
print(add_five(10))
