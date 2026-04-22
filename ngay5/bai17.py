def batch(data, batch_size):
    sub = []
    for item in data:
        sub.append(item)
        if len(sub) == batch_size:
            yield sub
            sub = []
    if sub:
        yield sub

for b in batch(range(10), 3):
    print(b)
