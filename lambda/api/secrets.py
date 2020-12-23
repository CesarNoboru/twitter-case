import json
import boto3
from botocore.exceptions import ClientError
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret():
    
    secret_name = "twitter-case-db-cred"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logger.error(f"msg='Secret Manager error' error='{e}'")
        sys.exit(e)
    else:
        secret = json.loads(get_secret_value_response['SecretString'])

        
    return secret
            