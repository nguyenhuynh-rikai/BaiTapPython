import logging

logging.basicConfig(level=logging.INFO)

class HTTPError(Exception):
    pass

def fake_request(status_code):
    if status_code == 404:
        raise HTTPError("404 Not Found")
    elif status_code == 500:
        raise HTTPError("500 Internal Server Error")
    else:
        return "200 OK"

def handle_request(status_code):
    try:
        result = fake_request(status_code)
        logging.info(f"Success: {result}")
    except HTTPError as e:
        logging.error(f"HTTP Error occurred: {e}")

handle_request(200)
handle_request(404)
handle_request(500)