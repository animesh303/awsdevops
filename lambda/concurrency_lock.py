"""
Concurrency lock module for IAM User Monitor.

This module implements a distributed lock mechanism using DynamoDB conditional
writes to prevent concurrent Lambda executions from overlapping.
"""

import boto3
import os
import uuid
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
from logger_config import setup_logging

# Initialize logger
logger = setup_logging()

# Lock configuration
LOCK_TTL_MINUTES = 10  # 2x Lambda timeout (5 minutes)
LOCK_KEY = "execution_lock"


class ConcurrencyLock:
    """
    Distributed lock implementation using DynamoDB conditional writes.
    
    Prevents concurrent Lambda executions by acquiring an exclusive lock
    in DynamoDB. The lock automatically expires after TTL to handle
    failures and timeouts.
    """
    
    def __init__(self, table_name: str = None):
        """
        Initialize the concurrency lock.
        
        Args:
            table_name: DynamoDB table name (defaults to env var DYNAMODB_TABLE_NAME)
            
        Raises:
            ValueError: If table_name is not provided and env var is not set
        """
        if table_name is None:
            table_name = os.environ.get('DYNAMODB_TABLE_NAME')
        
        if not table_name:
            raise ValueError("DynamoDB table name must be provided or set in DYNAMODB_TABLE_NAME env var")
        
        self.table_name = table_name
        self.dynamodb = boto3.client('dynamodb')
        self.execution_id = str(uuid.uuid4())
        self.lock_acquired = False
    
    def acquire(self) -> bool:
        """
        Attempt to acquire the execution lock.
        
        Uses DynamoDB conditional write to atomically create a lock item.
        The lock includes an execution_id and timestamp, and has a TTL
        to automatically expire after LOCK_TTL_MINUTES.
        
        Returns:
            True if lock was successfully acquired, False if lock already exists
        """
        try:
            # Calculate lock expiration time
            lock_timestamp = datetime.utcnow()
            lock_expiry = lock_timestamp + timedelta(minutes=LOCK_TTL_MINUTES)
            ttl_epoch = int(lock_expiry.timestamp())
            
            # Create lock item with conditional write
            # user_name = "execution_lock" (partition key)
            # scan_timestamp = current timestamp (sort key)
            self.dynamodb.put_item(
                TableName=self.table_name,
                Item={
                    'user_name': {'S': LOCK_KEY},
                    'scan_timestamp': {'S': lock_timestamp.isoformat() + 'Z'},
                    'execution_id': {'S': self.execution_id},
                    'lock_timestamp': {'S': lock_timestamp.isoformat() + 'Z'},
                    'ttl': {'N': str(ttl_epoch)}
                },
                ConditionExpression='attribute_not_exists(user_name) OR #ttl < :now',
                ExpressionAttributeNames={
                    '#ttl': 'ttl'
                },
                ExpressionAttributeValues={
                    ':now': {'N': str(int(datetime.utcnow().timestamp()))}
                }
            )
            
            self.lock_acquired = True
            
            logger.info(
                "Concurrency lock acquired successfully",
                extra={
                    "execution_id": self.execution_id,
                    "lock_timestamp": lock_timestamp.isoformat() + 'Z',
                    "lock_expiry": lock_expiry.isoformat() + 'Z'
                }
            )
            
            return True
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            
            if error_code == 'ConditionalCheckFailedException':
                # Lock already exists - another execution is in progress
                logger.warning(
                    "Failed to acquire lock - another execution is in progress",
                    extra={
                        "execution_id": self.execution_id,
                        "error_code": error_code
                    }
                )
                return False
            else:
                # Unexpected DynamoDB error
                error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
                request_id = e.response.get('ResponseMetadata', {}).get('RequestId', 'Unknown')
                
                logger.error(
                    f"Failed to acquire lock due to DynamoDB error: {error_message}",
                    extra={
                        "execution_id": self.execution_id,
                        "error_code": error_code,
                        "error_type": "ClientError",
                        "request_id": request_id
                    }
                )
                return False
                
        except Exception as e:
            # Unexpected error
            logger.error(
                f"Failed to acquire lock due to unexpected error: {str(e)}",
                extra={
                    "execution_id": self.execution_id,
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
            return False
    
    def release(self) -> None:
        """
        Release the execution lock.
        
        Deletes the lock item from DynamoDB if this execution acquired it.
        Uses conditional delete to ensure we only delete our own lock.
        """
        if not self.lock_acquired:
            logger.debug("No lock to release - lock was not acquired by this execution")
            return
        
        try:
            # Query for lock items to get the exact sort key
            response = self.dynamodb.query(
                TableName=self.table_name,
                KeyConditionExpression='user_name = :lock_key',
                ExpressionAttributeValues={
                    ':lock_key': {'S': LOCK_KEY}
                },
                Limit=1
            )
            
            items = response.get('Items', [])
            if items:
                lock_item = items[0]
                scan_timestamp = lock_item.get('scan_timestamp', {}).get('S')
                stored_execution_id = lock_item.get('execution_id', {}).get('S')
                
                # Only delete if it's our lock
                if stored_execution_id == self.execution_id:
                    self.dynamodb.delete_item(
                        TableName=self.table_name,
                        Key={
                            'user_name': {'S': LOCK_KEY},
                            'scan_timestamp': {'S': scan_timestamp}
                        }
                    )
                    
                    logger.info(
                        "Concurrency lock released successfully",
                        extra={
                            "execution_id": self.execution_id
                        }
                    )
                else:
                    logger.warning(
                        "Lock was acquired by different execution - not releasing",
                        extra={
                            "our_execution_id": self.execution_id,
                            "stored_execution_id": stored_execution_id
                        }
                    )
            else:
                logger.debug("No lock item found to release")
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_message = e.response.get('Error', {}).get('Message', 'Unknown error')
            request_id = e.response.get('ResponseMetadata', {}).get('RequestId', 'Unknown')
            
            logger.error(
                f"Failed to release lock due to DynamoDB error: {error_message}",
                extra={
                    "execution_id": self.execution_id,
                    "error_code": error_code,
                    "error_type": "ClientError",
                    "request_id": request_id
                }
            )
            
        except Exception as e:
            logger.error(
                f"Failed to release lock due to unexpected error: {str(e)}",
                extra={
                    "execution_id": self.execution_id,
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
    
    def __enter__(self):
        """Context manager entry - acquire lock."""
        if not self.acquire():
            raise LockAcquisitionError("Failed to acquire concurrency lock")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock."""
        self.release()
        return False


class LockAcquisitionError(Exception):
    """Exception raised when lock acquisition fails."""
    pass
