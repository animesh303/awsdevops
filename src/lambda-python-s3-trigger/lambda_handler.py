# Changelog:
# AWS-17 - Initial Lambda function for S3 trigger demo - 2025-01-28

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    S3 trigger Lambda handler - logs Hello World and event details.
    
    Args:
        event: S3 event notification payload
        context: Lambda context object
    
    Returns:
        Dict with status code and message
    """
    logger.info("Hello World - S3 Lambda Trigger Demo")
    logger.info(f"Event: {json.dumps(event)}")
    
    for record in event.get('Records', []):
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        logger.info(f"File uploaded: s3://{bucket}/{key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World from Lambda')
    }
