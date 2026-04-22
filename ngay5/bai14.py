def my_gen():
    x = yield "Start"
    y = yield "Start65"
    print("Received:", x)
    print("Received:", y)
    yield "End"

g = my_gen()

print(next(g))
print(g.send("this is a test1"))
print(g.send("this is a test2"))