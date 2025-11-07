# S3 Lambda Trigger Implementation

## Overview

This implementation creates an event-driven serverless architecture that automatically processes files uploaded to an S3 bucket using AWS Lambda.

## Architecture

- **S3 Bucket**: `demobucketforawsaidevops` - Receives file uploads
- **Lambda Function**: `hello_world` - Processes S3 events with "Hello World" demo
- **IAM Role**: Least privilege access for Lambda execution
- **CloudWatch**: Logging and monitoring

## Quick Start

### Prerequisites

- AWS CLI configured
- Terraform >= 1.1
- Python 3.12

### Deployment

1. **Deploy Infrastructure**:
   ```bash
   cd iac/terraform
   terraform init
   terraform plan
   terraform apply
   ```

2. **Package Lambda Function**:
   ```bash
   cd src/lambda-python-s3-lambda-trigger
   zip -r ../../iac/terraform/lambda_function.zip .
   ```

3. **Test the Implementation**:
   ```bash
   aws s3 cp test-file.txt s3://demobucketforawsaidevops/
   aws logs tail /aws/lambda/hello_world --follow
   ```

## Configuration

### Environment Variables

- `bucket_name`: S3 bucket name (default: demobucketforawsaidevops)
- `lambda_function_name`: Lambda function name (default: hello_world)
- `environment`: Environment name (default: dev)

### AWS Resources

- S3 Bucket with encryption and security settings
- Lambda function with Python 3.12 runtime
- IAM role with S3 read permissions
- CloudWatch log group with 14-day retention

## Monitoring

- **CloudWatch Logs**: `/aws/lambda/hello_world`
- **Metrics**: Lambda execution metrics in CloudWatch
- **Events**: S3 event notifications trigger Lambda execution

## Security

- Private S3 bucket with public access blocked
- IAM least privilege principles
- Server-side encryption enabled
- No hardcoded credentials