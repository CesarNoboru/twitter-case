import json
import boto3
from botocore.exceptions import ClientError
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret():
    
    secret_name = "twitter-case-db-cred"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
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
            