import logging
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
try:
    10 / 0
except ZeroDivisionError:
    logging.error("Errol", exc_info=True)