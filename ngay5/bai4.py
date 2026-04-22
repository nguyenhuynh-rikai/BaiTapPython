with open("test.txt", "w") as f:
    for i in range(1000):
        f.write(f"day la dong so {i}\n")

def read_large_file(filepath):
    with open(filepath) as f:
        for line in f:
            yield line

gen = read_large_file("test.txt")
for i in range(5):
    print(next(gen))