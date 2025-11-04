# S3 Bucket Implementation - AWS-6

## Overview
This implementation creates a secure AWS S3 bucket following best practices for storage, security, and monitoring as specified in JIRA ticket AWS-6.

## Architecture
- **Primary Bucket**: Secure S3 bucket with encryption and versioning
- **Access Logs Bucket**: Dedicated bucket for access logging
- **IAM Policy**: Least privilege access policy
- **Security**: Public access blocked, encryption enabled

## Features
- ✅ Server-side encryption (AES-256)
- ✅ Bucket versioning enabled
- ✅ Public access blocked
- ✅ Access logging configured
- ✅ IAM policy with least privilege
- ✅ Comprehensive resource tagging

## Deployment

### Prerequisites
- AWS CLI configured with appropriate permissions
- Terraform >= 1.1 installed
- Access to Terraform Cloud workspace (if using remote backend)

### Steps
1. **Initialize Terraform**:
   ```bash
   cd iac/terraform
   terraform init
   ```

2. **Plan Deployment**:
   ```bash
   terraform plan
   ```

3. **Apply Configuration**:
   ```bash
   terraform apply
   ```

### Configuration Variables
- `environment`: Environment name (default: "dev")
- `project_name`: Project name (default: "aws-devops-ai")
- `aws_region`: AWS region (default: "us-east-1")
- `bucket_name`: Custom bucket name (optional, auto-generated if not provided)
- `enable_versioning`: Enable bucket versioning (default: true)
- `enable_encryption`: Enable server-side encryption (default: true)
- `enable_access_logging`: Enable access logging (default: true)

## Outputs
- `s3_bucket_id`: ID of the created S3 bucket
- `s3_bucket_arn`: ARN of the S3 bucket
- `s3_bucket_domain_name`: Domain name of the S3 bucket
- `s3_bucket_policy_arn`: ARN of the IAM policy

## Security Considerations
- All public access is blocked by default
- Server-side encryption is enabled
- Access logging captures all bucket operations
- IAM policy follows least privilege principle
- Resource tagging includes JiraId for tracking

## Monitoring
- CloudWatch metrics automatically enabled for S3
- Access logs stored in dedicated bucket
- CloudTrail integration for API call logging

## Troubleshooting
- Ensure AWS credentials are properly configured
- Verify Terraform backend configuration is correct
- Check IAM permissions for S3 and IAM operations
- Review CloudWatch logs for any deployment issues