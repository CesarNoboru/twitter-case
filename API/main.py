import logging
import rds
import time
logger = logging.getLogger()
logger.setLevel(logging.INFO)
types = ['followers', 'hour', 'posts']

bad_req = {
    "Response" : 400,
    "Error" : "Missing Parameters"
}

def handler(event, context):
    try:
        logger.info("msg='Starting API.'")
        start_time = time.time()
        tag = None
        if 'query' not in event:
            logger.error("msg='Missing 'query' parameter.'")
            return bad_req
        if event['query'] not in types:
            return bad_req
        if event['query'] == 'posts':
            if 'tag' not in event:
                logger.error("msg='Query 'posts' without 'tag''")
                return bad_req
            tag = event['tag']
            logger.info(f"msg='Query validated' query='{event['query']} tag='{tag}'")
        query = rds.run(event['query'], tag)
        seconds = time.time() - start_time
        logger.info(f"msg='API done' exec_time={seconds:.2f}")
    except Exception as e:
        raise e
    return {
        "Response": 200,
        "Query": query,
        "ExecutionTime" : f"{seconds:.2f}"
    }