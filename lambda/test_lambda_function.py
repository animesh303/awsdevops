import json
import pytest
from unittest.mock import Mock
from lambda_function import lambda_handler

class TestLambdaHandler:
    """Test cases for Lambda handler function"""
    
    def test_lambda_handler_with_request_context(self):
        """Test Lambda handler with request context"""
        event = {
            'requestContext': {
                'requestId': 'test-request-id'
            }
        }
        context = Mock()
        context.aws_request_id = 'context-request-id'
        
        result = lambda_handler(event, context)
        
        assert result['statusCode'] == 200
        assert result['headers']['Content-Type'] == 'application/json'
        
        body = json.loads(result['body'])
        assert body['message'] == 'Hello from AWS Lambda!'
        assert body['requestId'] == 'test-request-id'
        assert 'timestamp' in body
    
    def test_lambda_handler_without_request_context(self):
        """Test Lambda handler without request context"""
        event = {}
        context = Mock()
        context.aws_request_id = 'context-request-id'
        
        result = lambda_handler(event, context)
        
        assert result['statusCode'] == 200
        
        body = json.loads(result['body'])
        assert body['requestId'] == 'context-request-id'
    
    def test_lambda_handler_no_context_request_id(self):
        """Test Lambda handler with no context request ID"""
        event = {}
        context = Mock()
        # Remove aws_request_id attribute
        del context.aws_request_id
        
        result = lambda_handler(event, context)
        
        assert result['statusCode'] == 200
        
        body = json.loads(result['body'])
        assert body['requestId'] == 'N/A'