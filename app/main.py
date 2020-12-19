from env import read_env
from log import logger
import rds
import time
from twitter import search
import sys


def scan():
    tags = read_env('tags')
    print(tags)
    tags = [
        "#openbanking", 
        "#remediation", 
        "#devops", 
        "#sre", 
        "#microservices", 
        "#observability", 
        "#oauth", 
        "#metrics", 
        "#logmonitoring", 
        "#opentracing"
    ]
    data = search(tags)


    rds.run(data)


    
if __name__ == "__main__":
    logger.info("msg='Starting search for tags.'")
    start_time = time.time()
    scan()
    seconds = time.time() - start_time
    logger.info(f"msg='Job done' exec_time={seconds:.2f}")
    sys.exit()