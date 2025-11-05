# Changelog:
# AWS-5 - Initial Lambda function for S3 trigger - 2025-01-27

import json
import logging
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for S3 trigger events.

    Args:
        event: S3 event data containing bucket and object information
        context: Lambda context object

    Returns:
        Dict containing response data
    """
    try:
        logger.info("Hello World! Lambda function triggered by S3 event")

        # Process S3 event records
        for record in event.get("Records", []):
            bucket_name = record["s3"]["bucket"]["name"]
            object_key = record["s3"]["object"]["key"]
            event_name = record["eventName"]

            logger.info(f"Processing S3 event: {event_name}")
            logger.info(f"Bucket: {bucket_name}")
            logger.info(f"Object: {object_key}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Hello World! S3 event processed successfully",
                    "processed_records": len(event.get("Records", [])),
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error processing S3 event: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "message": str(e)}),
        }
