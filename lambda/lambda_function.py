import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function
    
    Args:
        event: Lambda event data
        context: Lambda context object
        
    Returns:
        HTTP response with status code and body
    """
    logger.info(f"Event received: {json.dumps(event)}")
    
    # Extract request ID from context or event
    request_id = getattr(context, 'aws_request_id', 'N/A')
    if 'requestContext' in event and 'requestId' in event['requestContext']:
        request_id = event['requestContext']['requestId']
    
    response_body = {
        'message': 'Hello from AWS Lambda!',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'requestId': request_id,
        'event': event
    }
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(response_body)
    }
    
    return response