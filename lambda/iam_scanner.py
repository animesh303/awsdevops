"""
IAM user scanning module for IAM User Monitor.

This module handles retrieving all IAM users from AWS IAM service
with proper pagination and error handling.
"""

import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any, Optional
from logger_config import setup_logging

# Initialize logger
logger = setup_logging()


def scan_iam_users() -> List[Dict[str, Any]]:
    """
    Scan all IAM users in the AWS account with pagination support.
    
    Retrieves all IAM users using boto3 paginator to handle accounts
    with large numbers of users. Extracts required fields including
    user_name, user_id, arn, create_date, and password_last_used.
    
    Returns:
        List of user dictionaries with extracted fields
        
    Raises:
        ClientError: If IAM API call fails
        Exception: For other unexpected errors
    """
    users = []
    
    try:
        # Create IAM client
        iam_client = boto3.client('iam')
        
        # Use paginator to handle large numbers of users
        paginator = iam_client.get_paginator('list_users')
        page_iterator = paginator.paginate()
        
        logger.info("Starting IAM user scan")
        
        # Iterate through all pages
        for page in page_iterator:
            page_users = page.get('Users', [])
            
            for user in page_users:
                # Extract required fields
                user_data = {
                    'user_name': user['UserName'],
                    'user_id': user['UserId'],
                    'arn': user['Arn'],
                    'create_date': user['CreateDate'].isoformat(),
                }
                
                # Handle optional password_last_used field
                if 'PasswordLastUsed' in user:
                    user_data['password_last_used'] = user['PasswordLastUsed'].isoformat()
                else:
                    user_data['password_last_used'] = None
                
                users.append(user_data)
        
        logger.info(
            f"Successfully scanned {len(users)} IAM users",
            extra={"total_users": len(users)}
        )
        
        return users
        
    except ClientError as e:
        # Log AWS-specific error details
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
        request_id = e.response.get('ResponseMetadata', {}).get('RequestId', 'Unknown')
        
        logger.error(
            f"IAM API error during user scan: {error_message}",
            extra={
                "error_code": error_code,
                "error_type": "ClientError",
                "request_id": request_id
            }
        )
        raise
        
    except Exception as e:
        # Log unexpected errors
        logger.error(
            f"Unexpected error during IAM user scan: {str(e)}",
            extra={
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        raise
