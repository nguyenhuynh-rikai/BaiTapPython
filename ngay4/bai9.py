import logging
logging.basicConfig(
    handlers = [
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logging.info("The try...except block is finished")