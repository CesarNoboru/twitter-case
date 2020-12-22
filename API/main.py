import logging
import rds
import time
logger = logging.getLogger()
logger.setLevel(logging.INFO)
types = ['followers', 'hour', 'posts']
msg = "Missing Parameters."
response = {
    "isBase64Encoded": 'false',
    "statusCode": 400,
    "headers": {},
    "body": ''
}


def handler(event, context):
    try:
        logger.info("msg='Starting API.'")
        start_time = time.time()
        tag = None
        if 'query' not in event['queryStringParameters']:
            logger.error("msg='Missing 'query' parameter.'")
            response['body'] = "msg='Missing 'query' parameter.'"
            return response
        query = event['queryStringParameters']['query']
        if query not in types:
            response['body'] = "msg='Missing 'query' parameter.'"
            return response
        if query == 'posts':
            if 'tag' not in event['queryStringParameters']:
                logger.error("msg='Query 'posts' without 'tag''")
                response['body'] = "Query 'posts' without 'tag'"
                return response
            tag = event['queryStringParameters']['tag']
            logger.info(f"msg='Query validated' query='{query} tag='{tag}'")
        query = rds.run(query, tag)
        seconds = time.time() - start_time
        logger.info(f"msg='API done' exec_time={seconds:.2f}")
    except Exception as e:
        raise e
    logger.info(type(query))
    response['statusCode'] = 200
    response['body'] = query
    logger.info(response)
    return response