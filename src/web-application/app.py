# Changelog:
# AWS-3 - Flask web application for three-tier architecture - 2025-01-27

from flask import Flask, request, jsonify, render_template_string
import logging
import os
import json
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Three-Tier Application</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .tier { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .web-tier { background: #e3f2fd; }
        .app-tier { background: #f3e5f5; }
        .data-tier { background: #e8f5e8; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 10px; background: #fff; border: 1px solid #ddd; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AWS Three-Tier Application</h1>
        
        <div class="tier web-tier">
            <h2>🌐 Web Tier (Presentation)</h2>
            <p>This is the presentation layer running on EC2 instances behind an Application Load Balancer.</p>
            <p><strong>Server:</strong> {{ server_info }}</p>
        </div>
        
        <div class="tier app-tier">
            <h2>⚙️ Application Tier (Logic)</h2>
            <p>Business logic processing in private subnets.</p>
            <button onclick="fetchData()">Get Data from App Tier</button>
            <button onclick="testDatabase()">Test Database Connection</button>
            <div id="app-result" class="result" style="display:none;"></div>
        </div>
        
        <div class="tier data-tier">
            <h2>🗄️ Data Tier (Storage)</h2>
            <p>RDS MySQL database and S3 storage in private subnets.</p>
            <button onclick="testS3()">Test S3 Storage</button>
            <div id="data-result" class="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        function fetchData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('app-result').style.display = 'block';
                    document.getElementById('app-result').innerHTML = '<h4>Application Tier Response:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(error => {
                    document.getElementById('app-result').style.display = 'block';
                    document.getElementById('app-result').innerHTML = '<h4>Error:</h4><p>' + error + '</p>';
                });
        }
        
        function testDatabase() {
            fetch('/api/database/test')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('app-result').style.display = 'block';
                    document.getElementById('app-result').innerHTML = '<h4>Database Test:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(error => {
                    document.getElementById('app-result').style.display = 'block';
                    document.getElementById('app-result').innerHTML = '<h4>Database Error:</h4><p>' + error + '</p>';
                });
        }
        
        function testS3() {
            fetch('/api/s3/test')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('data-result').style.display = 'block';
                    document.getElementById('data-result').innerHTML = '<h4>S3 Test:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                })
                .catch(error => {
                    document.getElementById('data-result').style.display = 'block';
                    document.getElementById('data-result').innerHTML = '<h4>S3 Error:</h4><p>' + error + '</p>';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main web page showing three-tier architecture."""
    server_info = f"EC2 Instance - Region: {os.environ.get('AWS_REGION', 'us-east-1')}"
    return render_template_string(HTML_TEMPLATE, server_info=server_info)

@app.route('/health')
def health_check():
    """Health check endpoint for load balancer."""
    return jsonify({
        'status': 'healthy',
        'service': 'three-tier-web-application',
        'version': '1.0.0',
        'tier': 'web'
    })

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get data from application tier (simulated)."""
    try:
        # In a real application, this would query the database
        sample_data = {
            'items': [
                {'id': 1, 'name': 'Product A', 'description': 'High-quality product A', 'price': 29.99},
                {'id': 2, 'name': 'Product B', 'description': 'Premium product B', 'price': 49.99},
                {'id': 3, 'name': 'Product C', 'description': 'Essential product C', 'price': 19.99}
            ],
            'total': 3,
            'source': 'application-tier'
        }
        
        logger.info("Retrieved data from application tier")
        return jsonify(sample_data)
        
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        return jsonify({'error': 'Failed to retrieve data'}), 500

@app.route('/api/data', methods=['POST'])
def create_data():
    """Create new data via application tier."""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # In a real application, this would save to the database
        new_item = {
            'id': 4,  # Would be generated by database
            'name': data['name'],
            'description': data.get('description', ''),
            'price': data.get('price', 0.0),
            'created_at': '2025-01-27T00:00:00Z'
        }
        
        logger.info(f"Created new item: {new_item}")
        return jsonify(new_item), 201
        
    except Exception as e:
        logger.error(f"Error creating data: {str(e)}")
        return jsonify({'error': 'Failed to create data'}), 500

@app.route('/api/database/test')
def test_database():
    """Test database connection."""
    try:
        # Simulate database connection test
        db_status = {
            'status': 'connected',
            'host': os.environ.get('DB_HOST', 'three-tier-app-database.region.rds.amazonaws.com'),
            'database': os.environ.get('DB_NAME', 'threetierdb'),
            'engine': 'MySQL 8.0',
            'multi_az': True,
            'encrypted': True
        }
        
        logger.info("Database connection test successful")
        return jsonify(db_status)
        
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return jsonify({'error': 'Database connection failed'}), 500

@app.route('/api/s3/test')
def test_s3():
    """Test S3 storage connection."""
    try:
        # Simulate S3 connection test
        s3_status = {
            'status': 'connected',
            'bucket': os.environ.get('S3_BUCKET', 'three-tier-app-dev-bucket'),
            'region': os.environ.get('AWS_REGION', 'us-east-1'),
            'encryption': 'AES256',
            'versioning': 'enabled',
            'public_access': 'blocked'
        }
        
        logger.info("S3 connection test successful")
        return jsonify(s3_status)
        
    except Exception as e:
        logger.error(f"S3 connection test failed: {str(e)}")
        return jsonify({'error': 'S3 connection failed'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)