import json
import logging
logger = logging.getLogger(__name__)

def load_config(path):
    try:
        with open(path) as f:
            config = json.load(f)
    except Exception:
        logger.exception("Failed to load config file")
        return {}

    required_keys = ["host", "port", "username"]

    for key in required_keys:
        if key not in config:
            logger.error(f"Missing required key {key}")
    return config

logging.basicConfig(level=logging.INFO)
config = load_config("ngay4/config.json")