import json

def json_format(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        json_string = json.dumps(res)
        return json_string
    return wrapper

@json_format
def get_info():
    return {"name": "Nguyen", "job": "IT Student", "year": 4}

data = get_info()
print(data)
