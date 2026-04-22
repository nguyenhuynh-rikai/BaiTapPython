import logging

logging.basicConfig(level=logging.DEBUG)

from database import connect
from user import get_user

connect()
get_user()