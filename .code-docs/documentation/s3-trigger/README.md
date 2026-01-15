# S3 Lambda Trigger Demo (AWS-17)

Event-driven serverless architecture demonstrating S3 bucket notifications triggering AWS Lambda function execution.

## Architecture

- **S3 Bucket**: Accepts file uploads, triggers Lambda on object creation
- **Lambda Function**: Python 3.12 runtime, logs "Hello World" + event details
- **IAM Role**: Least privilege permissions for Lambda execution and S3 read
- **CloudWatch**: Logs (7-day retention) and error alarms

## Quick Start

```bash
cd iac/terraform
terraform init
terraform apply
```

See [Deployment Guide](.code-docs/documentation/s3-trigger/deployment-guide.md) for detailed instructions.

## Testing

```bash
BUCKET_NAME=$(cd iac/terraform && terraform output -raw s3_bucket_name)
echo "Test" > test.txt
aws s3 cp test.txt s3://$BUCKET_NAME/
aws logs tail /aws/lambda/s3-lambda-trigger-hello-world --follow
```

## Files

- `iac/terraform/` - Terraform infrastructure code
- `src/lambda-python-s3-trigger/` - Lambda function code
- `tests/s3-trigger/` - Unit tests

## Tags

- JiraId: AWS-17
- ManagedBy: Terraform
