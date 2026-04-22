import logging

logging.basicConfig(level=logging.DEBUG)

from database import connect

connect()
