"""
Basic tests for Lambda handler functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
from datetime import datetime
from lambda_function import lambda_handler, _check_timeout, _finalize_execution, _build_response


class TestLambdaHandler(unittest.TestCase):
    """Test cases for Lambda handler."""
    
    def setUp(self):
        """Set up test environment."""
        os.environ['DYNAMODB_TABLE_NAME'] = 'test-table'
        os.environ['LOG_LEVEL'] = 'INFO'
        os.environ['RETENTION_DAYS'] = '90'
    
    @patch('lambda_function.ConcurrencyLock')
    @patch('lambda_function.emit_metrics')
    @patch('lambda_function.write_user_records')
    @patch('lambda_function.scan_iam_users')
    def test_lambda_handler_success(self, mock_scan, mock_write, mock_emit, mock_lock_class):
        """Test successful Lambda execution."""
        # Mock concurrency lock
        mock_lock = Mock()
        mock_lock.acquire.return_value = True
        mock_lock_class.return_value = mock_lock
        
        # Mock scan_iam_users to return test users
        mock_scan.return_value = [
            {
                'user_name': 'test-user',
                'user_id': 'AIDAI123',
                'arn': 'arn:aws:iam::123456789012:user/test-user',
                'create_date': '2024-01-01T00:00:00Z',
                'password_last_used': '2024-11-01T00:00:00Z'
            }
        ]
        
        # Mock write_user_records to return success stats
        mock_write.return_value = {
            'records_written': 1,
            'errors': 0,
            'failed_users': []
        }
        
        # Create mock context
        context = Mock()
        context.function_name = 'test-function'
        context.request_id = 'test-request-id'
        context.get_remaining_time_in_millis = Mock(return_value=300000)  # 5 minutes
        
        # Execute handler
        result = lambda_handler({}, context)
        
        # Verify result
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['status'], 'success')
        self.assertTrue(result['statistics']['success'])
        self.assertEqual(result['statistics']['total_users'], 1)
        self.assertEqual(result['statistics']['records_written'], 1)
        self.assertEqual(result['statistics']['errors'], 0)
        
        # Verify all functions were called
        mock_lock.acquire.assert_called_once()
        mock_lock.release.assert_called_once()
        mock_scan.assert_called_once()
        mock_write.assert_called_once()
        mock_emit.assert_called_once()
    
    @patch('lambda_function.ConcurrencyLock')
    @patch('lambda_function.emit_metrics')
    @patch('lambda_function.write_user_records')
    @patch('lambda_function.scan_iam_users')
    def test_lambda_handler_with_errors(self, mock_scan, mock_write, mock_emit, mock_lock_class):
        """Test Lambda execution with some DynamoDB write errors."""
        # Mock concurrency lock
        mock_lock = Mock()
        mock_lock.acquire.return_value = True
        mock_lock_class.return_value = mock_lock
        
        # Mock scan_iam_users to return test users
        mock_scan.return_value = [
            {'user_name': 'user1', 'user_id': 'ID1', 'arn': 'arn1', 'create_date': '2024-01-01T00:00:00Z'},
            {'user_name': 'user2', 'user_id': 'ID2', 'arn': 'arn2', 'create_date': '2024-01-01T00:00:00Z'}
        ]
        
        # Mock write_user_records with partial success
        mock_write.return_value = {
            'records_written': 1,
            'errors': 1,
            'failed_users': ['user2']
        }
        
        # Create mock context
        context = Mock()
        context.function_name = 'test-function'
        context.request_id = 'test-request-id'
        context.get_remaining_time_in_millis = Mock(return_value=300000)
        
        # Execute handler
        result = lambda_handler({}, context)
        
        # Verify result - should still be success since some records were written
        self.assertEqual(result['statusCode'], 200)
        self.assertTrue(result['statistics']['success'])
        self.assertEqual(result['statistics']['total_users'], 2)
        self.assertEqual(result['statistics']['records_written'], 1)
        self.assertEqual(result['statistics']['errors'], 1)
    
    @patch('lambda_function.ConcurrencyLock')
    def test_lambda_handler_lock_acquisition_fails(self, mock_lock_class):
        """Test Lambda execution when lock acquisition fails."""
        # Mock concurrency lock to fail acquisition
        mock_lock = Mock()
        mock_lock.acquire.return_value = False
        mock_lock_class.return_value = mock_lock
        
        # Create mock context
        context = Mock()
        context.function_name = 'test-function'
        context.request_id = 'test-request-id'
        
        # Execute handler
        result = lambda_handler({}, context)
        
        # Verify result - should skip execution
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['status'], 'skipped_concurrent_execution')
        self.assertIn('message', result)
        
        # Verify lock was attempted but not released (since it wasn't acquired)
        mock_lock.acquire.assert_called_once()
        mock_lock.release.assert_not_called()
    
    def test_check_timeout_approaching(self):
        """Test timeout detection when approaching limit."""
        context = Mock()
        context.get_remaining_time_in_millis = Mock(return_value=20000)  # 20 seconds
        
        result = _check_timeout(context)
        self.assertTrue(result)
    
    def test_check_timeout_sufficient_time(self):
        """Test timeout detection with sufficient time."""
        context = Mock()
        context.get_remaining_time_in_millis = Mock(return_value=120000)  # 2 minutes
        
        result = _check_timeout(context)
        self.assertFalse(result)
    
    def test_finalize_execution(self):
        """Test execution statistics finalization."""
        stats = {}
        start_time = datetime.utcnow()
        
        _finalize_execution(stats, start_time)
        
        self.assertIn('duration_seconds', stats)
        self.assertIsInstance(stats['duration_seconds'], float)
        self.assertGreaterEqual(stats['duration_seconds'], 0)
    
    def test_build_response_success(self):
        """Test building success response."""
        stats = {
            'scan_timestamp': '2024-11-24T10:00:00Z',
            'total_users': 5,
            'records_written': 5,
            'errors': 0,
            'duration_seconds': 2.5,
            'success': True
        }
        
        response = _build_response(stats, 'success')
        
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['statistics']['total_users'], 5)
        self.assertNotIn('error', response)
    
    def test_build_response_error(self):
        """Test building error response."""
        stats = {
            'scan_timestamp': '2024-11-24T10:00:00Z',
            'total_users': 0,
            'records_written': 0,
            'errors': 1,
            'duration_seconds': 1.0,
            'success': False
        }
        
        response = _build_response(stats, 'error', 'Test error message')
        
        self.assertEqual(response['statusCode'], 500)
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['error'], 'Test error message')
        self.assertFalse(response['statistics']['success'])


if __name__ == '__main__':
    unittest.main()
