def my_gen():
    print("Generator started")
    x = yield "Start"
    print("x received:", x)

    y = yield "Start65"
    print("y received:", y)

    yield "End"

g = my_gen()
print(next(g))
print(g.send("this is a test1"))
print(g.send("this is a test2"))