import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

try:
    x = int("abc")
except ValueError as e:
    raise RuntimeError("Data processing error") from e