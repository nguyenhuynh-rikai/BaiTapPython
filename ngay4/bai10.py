import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers = [
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logging.info("The try...except block is finished")