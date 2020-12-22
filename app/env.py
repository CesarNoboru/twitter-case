import os
import sys
import dotenv
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
dotenv.load_dotenv(dotenv.find_dotenv())

def read_tags(name, default=None):
    logger.info(f"msg='Getting ENV' env_var='{name}'")
    try:
        key = os.environ.get(name, default)
        if key is None:
            logger.warning(f"msg='No ENV found, using default' env_var='{name}'")
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
        else:
            tags = []
            for tag in key.split(','):
                tags.append(tag)
            logger.info(f"msg='ENV variable loaded into tags' env_var='{name}' tags={tags}")
    except Exception as e:
        logger.error(f"msg='Error Reading ENV' env_var='{name}' error={e}")
        sys.exit()
    return tags