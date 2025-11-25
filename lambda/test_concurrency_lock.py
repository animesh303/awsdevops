"""
Tests for concurrency lock module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
from botocore.exceptions import ClientError
from concurrency_lock import ConcurrencyLock, LockAcquisitionError


class TestConcurrencyLock(unittest.TestCase):
    """Test cases for ConcurrencyLock."""
    
    def setUp(self):
        """Set up test environment."""
        os.environ['DYNAMODB_TABLE_NAME'] = 'test-table'
    
    @patch('concurrency_lock.boto3.client')
    def test_lock_acquisition_success(self, mock_boto_client):
        """Test successful lock acquisition."""
        # Mock DynamoDB client
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = {}
        
        # Create lock and acquire
        lock = ConcurrencyLock(table_name='test-table')
        result = lock.acquire()
        
        # Verify acquisition succeeded
        self.assertTrue(result)
        self.assertTrue(lock.lock_acquired)
        
        # Verify put_item was called with correct parameters
        mock_dynamodb.put_item.assert_called_once()
        call_args = mock_dynamodb.put_item.call_args
        self.assertEqual(call_args[1]['TableName'], 'test-table')
        self.assertIn('Item', call_args[1])
        self.assertIn('ConditionExpression', call_args[1])
    
    @patch('concurrency_lock.boto3.client')
    def test_lock_acquisition_fails_concurrent_execution(self, mock_boto_client):
        """Test lock acquisition failure when another execution is in progress."""
        # Mock DynamoDB client to raise ConditionalCheckFailedException
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        
        error_response = {
            'Error': {
                'Code': 'ConditionalCheckFailedException',
                'Message': 'The conditional request failed'
            },
            'ResponseMetadata': {
                'RequestId': 'test-request-id'
            }
        }
        mock_dynamodb.put_item.side_effect = ClientError(error_response, 'PutItem')
        
        # Create lock and attempt acquisition
        lock = ConcurrencyLock(table_name='test-table')
        result = lock.acquire()
        
        # Verify acquisition failed
        self.assertFalse(result)
        self.assertFalse(lock.lock_acquired)
    
    @patch('concurrency_lock.boto3.client')
    def test_lock_acquisition_fails_dynamodb_error(self, mock_boto_client):
        """Test lock acquisition failure due to DynamoDB error."""
        # Mock DynamoDB client to raise a different error
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        
        error_response = {
            'Error': {
                'Code': 'ProvisionedThroughputExceededException',
                'Message': 'Throughput exceeded'
            },
            'ResponseMetadata': {
                'RequestId': 'test-request-id'
            }
        }
        mock_dynamodb.put_item.side_effect = ClientError(error_response, 'PutItem')
        
        # Create lock and attempt acquisition
        lock = ConcurrencyLock(table_name='test-table')
        result = lock.acquire()
        
        # Verify acquisition failed
        self.assertFalse(result)
        self.assertFalse(lock.lock_acquired)
    
    @patch('concurrency_lock.boto3.client')
    def test_lock_release_success(self, mock_boto_client):
        """Test successful lock release."""
        # Mock DynamoDB client
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = {}
        mock_dynamodb.query.return_value = {
            'Items': [{
                'user_name': {'S': 'execution_lock'},
                'scan_timestamp': {'S': '2024-11-24T10:00:00Z'},
                'execution_id': {'S': 'test-execution-id'}
            }]
        }
        mock_dynamodb.delete_item.return_value = {}
        
        # Create lock, acquire, and release
        lock = ConcurrencyLock(table_name='test-table')
        lock.execution_id = 'test-execution-id'  # Set to match query result
        lock.lock_acquired = True
        lock.release()
        
        # Verify query and delete were called
        mock_dynamodb.query.assert_called_once()
        mock_dynamodb.delete_item.assert_called_once()
    
    @patch('concurrency_lock.boto3.client')
    def test_lock_release_no_lock_acquired(self, mock_boto_client):
        """Test lock release when no lock was acquired."""
        # Mock DynamoDB client
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        
        # Create lock without acquiring
        lock = ConcurrencyLock(table_name='test-table')
        lock.release()
        
        # Verify no DynamoDB operations were called
        mock_dynamodb.query.assert_not_called()
        mock_dynamodb.delete_item.assert_not_called()
    
    @patch('concurrency_lock.boto3.client')
    def test_lock_release_different_execution(self, mock_boto_client):
        """Test lock release when lock belongs to different execution."""
        # Mock DynamoDB client
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        mock_dynamodb.query.return_value = {
            'Items': [{
                'user_name': {'S': 'execution_lock'},
                'scan_timestamp': {'S': '2024-11-24T10:00:00Z'},
                'execution_id': {'S': 'different-execution-id'}
            }]
        }
        
        # Create lock with different execution_id
        lock = ConcurrencyLock(table_name='test-table')
        lock.execution_id = 'our-execution-id'
        lock.lock_acquired = True
        lock.release()
        
        # Verify query was called but delete was not
        mock_dynamodb.query.assert_called_once()
        mock_dynamodb.delete_item.assert_not_called()
    
    @patch('concurrency_lock.boto3.client')
    def test_context_manager_success(self, mock_boto_client):
        """Test using lock as context manager with successful acquisition."""
        # Mock DynamoDB client
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        mock_dynamodb.put_item.return_value = {}
        mock_dynamodb.query.return_value = {
            'Items': [{
                'user_name': {'S': 'execution_lock'},
                'scan_timestamp': {'S': '2024-11-24T10:00:00Z'},
                'execution_id': {'S': 'test-id'}
            }]
        }
        
        # Use lock as context manager
        lock = ConcurrencyLock(table_name='test-table')
        lock.execution_id = 'test-id'
        
        with lock:
            self.assertTrue(lock.lock_acquired)
        
        # Verify release was called
        mock_dynamodb.query.assert_called_once()
    
    @patch('concurrency_lock.boto3.client')
    def test_context_manager_acquisition_fails(self, mock_boto_client):
        """Test using lock as context manager when acquisition fails."""
        # Mock DynamoDB client to fail acquisition
        mock_dynamodb = Mock()
        mock_boto_client.return_value = mock_dynamodb
        
        error_response = {
            'Error': {
                'Code': 'ConditionalCheckFailedException',
                'Message': 'The conditional request failed'
            },
            'ResponseMetadata': {
                'RequestId': 'test-request-id'
            }
        }
        mock_dynamodb.put_item.side_effect = ClientError(error_response, 'PutItem')
        
        # Attempt to use lock as context manager
        lock = ConcurrencyLock(table_name='test-table')
        
        with self.assertRaises(LockAcquisitionError):
            with lock:
                pass


if __name__ == '__main__':
    unittest.main()
