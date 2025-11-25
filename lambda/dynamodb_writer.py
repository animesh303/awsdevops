"""
DynamoDB writer module for IAM User Monitor.

This module handles writing IAM user records to DynamoDB with proper
batch operations, error handling, and TTL calculation.
"""

import boto3
import os
from botocore.exceptions import ClientError
from typing import List, Dict, Any
from datetime import datetime, timedelta
from logger_config import setup_logging

# Initialize logger
logger = setup_logging()


def write_user_records(
    users: List[Dict[str, Any]], 
    scan_timestamp: str,
    table_name: str = None,
    retention_days: int = 90
) -> Dict[str, int]:
    """
    Write IAM user records to DynamoDB with batch operations.
    
    Formats user records with all required attributes including scan_timestamp
    and TTL. Implements batch write operations (up to 25 items per batch) for
    efficiency. Continues processing remaining users even if some writes fail.
    
    Args:
        users: List of user dictionaries from IAM scanner
        scan_timestamp: ISO 8601 timestamp of the scan operation
        table_name: DynamoDB table name (defaults to env var DYNAMODB_TABLE_NAME)
        retention_days: Number of days to retain records (default: 90)
        
    Returns:
        Dictionary with statistics: {
            'records_written': int,
            'errors': int,
            'failed_users': List[str]
        }
        
    Raises:
        ValueError: If table_name is not provided and env var is not set
    """
    # Get table name from parameter or environment variable
    if table_name is None:
        table_name = os.environ.get('DYNAMODB_TABLE_NAME')
    
    if not table_name:
        raise ValueError("DynamoDB table name must be provided or set in DYNAMODB_TABLE_NAME env var")
    
    # Initialize statistics
    stats = {
        'records_written': 0,
        'errors': 0,
        'failed_users': []
    }
    
    if not users:
        logger.info("No users to write to DynamoDB")
        return stats
    
    # Create DynamoDB client
    dynamodb = boto3.client('dynamodb')
    
    # Calculate TTL (epoch timestamp)
    ttl_date = datetime.utcnow() + timedelta(days=retention_days)
    ttl_epoch = int(ttl_date.timestamp())
    
    logger.info(
        f"Starting DynamoDB write operation for {len(users)} users",
        extra={
            "total_users": len(users),
            "scan_timestamp": scan_timestamp,
            "table_name": table_name,
            "retention_days": retention_days
        }
    )
    
    # Process users in batches of 25 (DynamoDB BatchWriteItem limit)
    batch_size = 25
    for i in range(0, len(users), batch_size):
        batch = users[i:i + batch_size]
        
        # Format batch write request
        request_items = []
        for user in batch:
            item = _format_user_record(user, scan_timestamp, ttl_epoch)
            request_items.append({
                'PutRequest': {
                    'Item': item
                }
            })
        
        # Attempt to write batch
        try:
            response = dynamodb.batch_write_item(
                RequestItems={
                    table_name: request_items
                }
            )
            
            # Check for unprocessed items
            unprocessed = response.get('UnprocessedItems', {})
            if unprocessed:
                # Log warning about unprocessed items
                unprocessed_count = len(unprocessed.get(table_name, []))
                logger.warning(
                    f"Batch write had {unprocessed_count} unprocessed items",
                    extra={
                        "unprocessed_count": unprocessed_count,
                        "batch_start_index": i
                    }
                )
                stats['errors'] += unprocessed_count
                
                # Track failed users from unprocessed items
                for item in unprocessed.get(table_name, []):
                    user_name = item.get('PutRequest', {}).get('Item', {}).get('user_name', {}).get('S', 'Unknown')
                    stats['failed_users'].append(user_name)
            
            # Count successfully written records
            successful_writes = len(batch) - len(unprocessed.get(table_name, []))
            stats['records_written'] += successful_writes
            
        except ClientError as e:
            # Log AWS-specific error details
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
            request_id = e.response.get('ResponseMetadata', {}).get('RequestId', 'Unknown')
            
            # Log error with affected user names
            user_names = [user['user_name'] for user in batch]
            logger.error(
                f"DynamoDB batch write failed: {error_message}",
                extra={
                    "error_code": error_code,
                    "error_type": "ClientError",
                    "request_id": request_id,
                    "affected_users": user_names,
                    "batch_size": len(batch)
                }
            )
            
            # Track errors and failed users
            stats['errors'] += len(batch)
            stats['failed_users'].extend(user_names)
            
            # Continue processing remaining batches
            continue
            
        except Exception as e:
            # Log unexpected errors
            user_names = [user['user_name'] for user in batch]
            logger.error(
                f"Unexpected error during DynamoDB write: {str(e)}",
                extra={
                    "error_type": type(e).__name__,
                    "affected_users": user_names,
                    "batch_size": len(batch)
                },
                exc_info=True
            )
            
            # Track errors and failed users
            stats['errors'] += len(batch)
            stats['failed_users'].extend(user_names)
            
            # Continue processing remaining batches
            continue
    
    # Log final statistics
    logger.info(
        f"DynamoDB write operation completed: {stats['records_written']} written, {stats['errors']} errors",
        extra={
            "records_written": stats['records_written'],
            "errors": stats['errors'],
            "scan_timestamp": scan_timestamp
        }
    )
    
    return stats


def _format_user_record(
    user: Dict[str, Any],
    scan_timestamp: str,
    ttl_epoch: int
) -> Dict[str, Any]:
    """
    Format a user record for DynamoDB with proper attribute types.
    
    Converts user data to DynamoDB item format with all required attributes
    including scan_timestamp and TTL.
    
    Args:
        user: User dictionary from IAM scanner
        scan_timestamp: ISO 8601 timestamp of the scan
        ttl_epoch: TTL expiration as epoch timestamp
        
    Returns:
        DynamoDB item dictionary with typed attributes
    """
    item = {
        'user_name': {'S': user['user_name']},
        'scan_timestamp': {'S': scan_timestamp},
        'user_id': {'S': user['user_id']},
        'arn': {'S': user['arn']},
        'create_date': {'S': user['create_date']},
        'ttl': {'N': str(ttl_epoch)}
    }
    
    # Add optional password_last_used field if present
    if user.get('password_last_used'):
        item['password_last_used'] = {'S': user['password_last_used']}
    
    return item
