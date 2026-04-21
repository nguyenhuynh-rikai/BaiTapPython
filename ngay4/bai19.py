import logging
logging.basicConfig(level=logging.INFO)

def input_number(max_retry = 3):
    for attempt in range(1, max_retry + 1):
        try:
            value = int(input("Enter a number: "))
            return value
        except ValueError:
            logging.error(f"Invalid input. Attempt {attempt}/{max_retry} failed.")

    raise Exception("Invalid input.")

try:
    x = input_number()
    print(f"You entered: ", x)
except Exception as e:
    logging.error(e)