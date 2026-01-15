import pytest
import json
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/lambda-python-s3-trigger'))
from lambda_handler import lambda_handler

def test_lambda_handler_should_return_success():
    # Arrange
    event = {
        'Records': [{
            's3': {
                'bucket': {'name': 'test-bucket'},
                'object': {'key': 'test-file.txt'}
            }
        }]
    }
    context = Mock()
    
    # Act
    result = lambda_handler(event, context)
    
    # Assert
    assert result['statusCode'] == 200
    assert 'Hello World' in result['body']

def test_lambda_handler_should_handle_empty_records():
    # Arrange
    event = {'Records': []}
    context = Mock()
    
    # Act
    result = lambda_handler(event, context)
    
    # Assert
    assert result['statusCode'] == 200
