try:
    print(int("abc"))
except (ValueError, TypeError):
    print("Invalid input")

