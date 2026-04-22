import logging
from unittest import result

logging.basicConfig(level=logging.INFO)

class HTTPError(Exception):
    pass

def fake_request(status_code):
    if status_code == 404:
        raise HTTPError("404 not found")
    elif status_code == 500:
        raise HTTPError("500 server error")
    else:
        return {"status_code": status_code}

def handle_request(status_code):
    try:
        result = fake_request(status_code)
        logging.info(result)
    except HTTPError as e:
        logging.error(e)

handle_request(200)
handle_request(404)
handle_request(500)
