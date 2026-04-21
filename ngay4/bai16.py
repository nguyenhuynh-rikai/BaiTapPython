import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("app.log", maxBytes=5000000, backupCount=3)
logger.addHandler(handler)
logger.info("This is a log message")