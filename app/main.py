from env import read_tags
from log import logger
import rds
import time
from twitter import search
import os

try:
    logger.info("msg='Starting search for tags.'")
    start_time = time.time()
    tags = read_tags('TAGS')      
    data = search(tags)
    rds.run(data)
    seconds = time.time() - start_time
    logger.info(f"msg='Job done' exec_time={seconds:.2f}")
except Exception as e:
    raise e