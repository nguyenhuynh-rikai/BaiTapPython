def read_file(filename):
    with open(filename) as f:
        for line in f:
            yield line

for line in read_file("oneGB.txt"):
    print(line.strip())