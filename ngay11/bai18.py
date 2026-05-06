def multiply(a, b):
    return a * b

def test_multiply():
    assert multiply(2, 4) == 8
    assert multiply(-1, 5) == -5

# Run command: pytest 18_test_math.py