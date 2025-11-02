# AWS-3 Requirements Analysis for Code Generation

## Feature Name
**two-tier-web-app**

## AWS Services to Implement

### Core Infrastructure
- **VPC**: Custom VPC with public/private subnets across 2 AZs
- **EC2**: Web tier and App tier instances with Auto Scaling Groups
- **S3**: Bucket for data storage, static assets, backups, and logs
- **ALB**: Application Load Balancer for web tier traffic distribution

### Security & Access
- **IAM**: Roles and policies for EC2 instances
- **Security Groups**: Tier-specific security groups with least privilege
- **KMS**: Encryption keys for data at rest

### Monitoring
- **CloudWatch**: Monitoring and logging for all services
- **CloudTrail**: Audit logging

## Programming Language Requirements
- **Primary**: Python for application logic
- **Web Server**: Apache/Nginx configuration
- **Data Storage**: S3 for file-based data storage

## Infrastructure Requirements (Terraform)
- VPC with 4 subnets (2 public, 2 private) across 2 AZs
- Internet Gateway and NAT Gateway
- Route tables and associations
- Security groups for each tier
- EC2 instances with Auto Scaling Groups
- S3 bucket with versioning and encryption
- Application Load Balancer
- IAM roles and policies
- CloudWatch log groups

## Testing Requirements
- Infrastructure validation tests
- Application unit tests
- Integration tests for tier communication
- Security compliance tests

## Key Technical Specifications
- **Web Tier**: t3.medium instances (minimum 2 for HA)
- **App Tier**: t3.large instances (minimum 2 for HA)
- **Storage**: S3 Standard with lifecycle policies for data and static assets
- **Network**: Custom VPC with proper subnet segmentation
- **Security**: Encryption at rest and in transit
- **Monitoring**: CloudWatch metrics and logs for all components