try:
    a = int("abc")
except ValueError or TypeError:
    print("Invalid input type")