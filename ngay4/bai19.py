import logging


def input_type(max_try = 3):
    for attempt in range(1, max_try+1):
        try:
            value = int(input("enter number:"))
            return value
        except ValueError:
            logging.error("invalid input")

    raise ValueError("invalid input")

try:
    x = input_type()
    print("you entered", x)
except ValueError:
    logging.error("invalid input")