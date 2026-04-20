import json
def output_formatter(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result)
    return wrapper

@output_formatter
def run(x):
    return x

print(run({
  "name": "John",
  "age": 30,
  "city": "New York"
}))