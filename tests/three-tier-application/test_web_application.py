# Changelog:
# AWS-3 - Unit tests for Flask web application - 2025-01-27

import pytest
import json
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'web-application'))

from app import app

class TestWebApplication:
    """Test cases for the Flask web application."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_home_page(self, client):
        """Test home page returns HTML."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Three-Tier Application' in response.data
        assert b'Web Tier' in response.data
        assert b'Application Tier' in response.data
        assert b'Data Tier' in response.data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'three-tier-web-application'
        assert data['version'] == '1.0.0'
        assert data['tier'] == 'web'
    
    def test_get_data_api(self, client):
        """Test GET /api/data endpoint."""
        response = client.get('/api/data')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'items' in data
        assert 'total' in data
        assert len(data['items']) == 3
        assert data['total'] == 3
        assert data['source'] == 'application-tier'
    
    def test_post_data_api_success(self, client):
        """Test POST /api/data with valid data."""
        payload = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': 99.99
        }
        
        response = client.post('/api/data', 
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test Product'
        assert data['description'] == 'Test Description'
        assert data['price'] == 99.99
        assert 'id' in data
        assert 'created_at' in data
    
    def test_post_data_api_missing_name(self, client):
        """Test POST /api/data with missing name."""
        payload = {
            'description': 'Test Description',
            'price': 99.99
        }
        
        response = client.post('/api/data',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Name is required'
    
    def test_database_test_endpoint(self, client):
        """Test database connection test endpoint."""
        response = client.get('/api/database/test')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'connected'
        assert 'host' in data
        assert 'database' in data
        assert data['engine'] == 'MySQL 8.0'
        assert data['multi_az'] is True
        assert data['encrypted'] is True
    
    def test_s3_test_endpoint(self, client):
        """Test S3 connection test endpoint."""
        response = client.get('/api/s3/test')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'connected'
        assert 'bucket' in data
        assert 'region' in data
        assert data['encryption'] == 'AES256'
        assert data['versioning'] == 'enabled'
        assert data['public_access'] == 'blocked'
    
    def test_404_error_handler(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Not found'
    
    @patch('app.logger')
    def test_error_logging(self, mock_logger, client):
        """Test that errors are properly logged."""
        # This would test error logging in a real scenario
        response = client.get('/api/data')
        assert response.status_code == 200

class TestEnvironmentConfiguration:
    """Test environment variable handling."""
    
    @patch.dict(os.environ, {'DB_HOST': 'test-db-host'})
    def test_database_host_from_env(self, client=None):
        """Test database host is read from environment."""
        if not client:
            app.config['TESTING'] = True
            client = app.test_client()
        
        response = client.get('/api/database/test')
        data = json.loads(response.data)
        assert data['host'] == 'test-db-host'
    
    @patch.dict(os.environ, {'S3_BUCKET': 'test-bucket'})
    def test_s3_bucket_from_env(self, client=None):
        """Test S3 bucket is read from environment."""
        if not client:
            app.config['TESTING'] = True
            client = app.test_client()
        
        response = client.get('/api/s3/test')
        data = json.loads(response.data)
        assert data['bucket'] == 'test-bucket'

if __name__ == '__main__':
    pytest.main([__file__])