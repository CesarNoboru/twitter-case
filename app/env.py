import os
import sys
import dotenv
from log import logger

dotenv.load_dotenv(dotenv.find_dotenv())

def read_env(name, default=None):
    key = os.environ.get(name, default)
    if key is None:
        logger.error(f"Couldn't find ENV {name}.")
        sys.exit()
    return key