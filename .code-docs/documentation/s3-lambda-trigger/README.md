# S3 Lambda Trigger - AWS-5

## Overview
This implementation creates an S3 bucket that automatically triggers a Lambda function when files are uploaded. The Lambda function logs a "Hello World" message to demonstrate the event-driven integration.

## Architecture
- **S3 Bucket**: Receives file uploads and generates events
- **Lambda Function**: Python function triggered by S3 events
- **IAM Role**: Execution role with minimal S3 permissions
- **CloudWatch Logs**: Stores Lambda execution logs

## Prerequisites
- AWS CLI configured with appropriate permissions
- Terraform >= 1.1
- Python 3.9+

## Deployment

### 1. Deploy Infrastructure
```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 2. Package Lambda Function
```bash
cd src/lambda-s3-lambda-trigger
zip -r ../../iac/terraform/lambda_function.zip .
```

### 3. Update Lambda Function
```bash
cd iac/terraform
terraform apply
```

## Testing

### Upload Test File
```bash
aws s3 cp test-file.txt s3://aws-s3-lambda-trigger-demo/
```

### Check Lambda Logs
```bash
aws logs tail /aws/lambda/s3-lambda-trigger-hello-world --follow
```

## Resources Created
- S3 bucket: `aws-s3-lambda-trigger-demo`
- Lambda function: `s3-lambda-trigger-hello-world`
- IAM role: `s3-lambda-trigger-hello-world-execution-role`
- CloudWatch log group: `/aws/lambda/s3-lambda-trigger-hello-world`

## Security
- Lambda execution role follows least privilege principle
- S3 bucket has versioning enabled
- CloudWatch logs have 14-day retention policy