from importlib.metadata import distributions

for dist in distributions():
    print(f"{dist.metadata['Name']} == {dist.version}")