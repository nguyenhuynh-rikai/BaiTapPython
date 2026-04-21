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
    x = 10/0
except Exception as e:
    logging.exception("Co loi xay ra")