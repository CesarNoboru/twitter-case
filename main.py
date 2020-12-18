from env import read_env
from log import logger
import rds
import sys
import time
from twitter import search



def scan():

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

    if rds.run(data) == 0:
        print("deu bom")


    
if __name__ == "__main__":
    logger.info('Starting Search.')
    scan()
    logger.info('Done')