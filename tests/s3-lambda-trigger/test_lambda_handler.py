# Changelog:
# AWS-5 - Initial unit tests for Lambda function - 2025-01-27

import json
import pytest
from unittest.mock import Mock
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/lambda-s3-lambda-trigger'))

from lambda_handler import lambda_handler

class TestLambdaHandler:
    """Unit tests for S3 Lambda trigger function."""

    def test_lambda_handler_success(self):
        """Test successful processing of S3 event."""
        # Mock S3 event
        event = {
            'Records': [
                {
                    'eventName': 's3:ObjectCreated:Put',
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'test-file.txt'}
                    }
                }
            ]
        }
        
        # Mock context
        context = Mock()
        
        # Call function
        response = lambda_handler(event, context)
        
        # Assertions
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'Hello World! S3 event processed successfully'
        assert body['processed_records'] == 1

    def test_lambda_handler_multiple_records(self):
        """Test processing multiple S3 event records."""
        # Mock S3 event with multiple records
        event = {
            'Records': [
                {
                    'eventName': 's3:ObjectCreated:Put',
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'file1.txt'}
                    }
                },
                {
                    'eventName': 's3:ObjectCreated:Post',
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'file2.txt'}
                    }
                }
            ]
        }
        
        context = Mock()
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['processed_records'] == 2

    def test_lambda_handler_empty_records(self):
        """Test handling of empty records."""
        event = {'Records': []}
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['processed_records'] == 0

    def test_lambda_handler_no_records_key(self):
        """Test handling when Records key is missing."""
        event = {}
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['processed_records'] == 0

    def test_lambda_handler_malformed_event(self):
        """Test handling of malformed event data."""
        # Event missing required S3 structure
        event = {
            'Records': [
                {
                    'eventName': 's3:ObjectCreated:Put'
                    # Missing 's3' key
                }
            ]
        }
        
        context = Mock()
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert 'error' in body