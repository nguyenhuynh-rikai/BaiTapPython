import json
def output_formatter(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(json.dumps(result))
        return result
    return wrapper

@output_formatter
def run(x):
    return x

run({
  "name": "John",
  "age": 30,
  "city": "New York"
})