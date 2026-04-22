import logging
logging.basicConfig(
    level=logging.DEBUG,
    handlers = [
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logging.info("The try...except block is finished")