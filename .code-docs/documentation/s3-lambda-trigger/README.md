# S3 Lambda Trigger - Hello World Demo

## Overview

This implementation creates an event-driven serverless architecture that automatically processes files uploaded to an S3 bucket by triggering a Lambda function that outputs "Hello World".

## Architecture

- **S3 Bucket**: `demobucketforawsaidevops` - Receives file uploads
- **Lambda Function**: `hello-world-s3-trigger` - Processes S3 events and logs "Hello World"
- **IAM Role**: Lambda execution role with minimal S3 read permissions
- **CloudWatch**: Logging and monitoring for Lambda execution

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.1 installed
- Python 3.12 for local development/testing

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
cd src/lambda-python-s3-lambda-trigger
zip -r lambda_function.zip lambda_handler.py
cp lambda_function.zip ../../iac/terraform/
```

### 3. Update Lambda Function (if needed)

```bash
cd iac/terraform
terraform apply -replace=aws_lambda_function.hello_world
```

## Testing

1. Upload a file to the S3 bucket:
```bash
aws s3 cp test-file.txt s3://demobucketforawsaidevops/
```

2. Check CloudWatch logs:
```bash
aws logs tail /aws/lambda/hello-world-s3-trigger --follow
```

## Expected Output

When a file is uploaded, the Lambda function will log:
- "Hello World! Lambda function triggered by S3 event"
- S3 event details (bucket name, object key, event name)
- Success message with processed record count

## Cleanup

```bash
cd iac/terraform
terraform destroy
```