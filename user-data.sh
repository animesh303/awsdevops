#!/bin/bash
yum update -y
yum install -y httpd

# Start and enable Apache
systemctl start httpd
systemctl enable httpd

# Create a simple HTML page
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>AWS Sample Project</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #232f3e; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AWS Sample Project</h1>
        </div>
        <div class="content">
            <h2>EC2 Instance Running Successfully!</h2>
            <p>This web server is running on an EC2 instance provisioned with Terraform.</p>
            <p><strong>Instance Details:</strong></p>
            <ul>
                <li>AMI: Amazon Linux 2</li>
                <li>Web Server: Apache HTTP Server</li>
                <li>Provisioned: $(date)</li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF

# Set proper permissions
chown apache:apache /var/www/html/index.html
chmod 644 /var/www/html/index.html