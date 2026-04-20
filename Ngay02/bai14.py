def make_adder(x):
    def add(y):
        return x+y
    return add

add_five = make_adder(5)

result = add_five(10)
print(result)