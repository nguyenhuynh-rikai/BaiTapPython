def batch_generator(data, batch_size):
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch


data = list(range(1, 251))
for batch in batch_generator(data, 100):
    print(batch)