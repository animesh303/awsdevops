# AWS-17 Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.1 installed
- AWS account with permissions for S3, Lambda, IAM, CloudWatch

## Deployment Steps

### 1. Initialize Terraform

```bash
cd iac/terraform
terraform init
```

### 2. Review Terraform Plan

```bash
terraform plan
```

### 3. Apply Infrastructure

```bash
terraform apply
```

Review the plan and type `yes` to confirm.

### 4. Note Outputs

After successful deployment, note the outputs:
- `s3_bucket_name` - S3 bucket name for testing
- `lambda_function_name` - Lambda function name
- `cloudwatch_log_group` - CloudWatch log group for monitoring

## Testing

### Upload Test File

```bash
# Get bucket name from Terraform output
BUCKET_NAME=$(terraform output -raw s3_bucket_name)

# Upload test file
echo "Test content" > test-file.txt
aws s3 cp test-file.txt s3://$BUCKET_NAME/
```

### Verify Lambda Execution

```bash
# Get Lambda function name
FUNCTION_NAME=$(terraform output -raw lambda_function_name)

# Check CloudWatch logs
aws logs tail /aws/lambda/$FUNCTION_NAME --follow
```

Expected log output:
```
Hello World - S3 Lambda Trigger Demo
File uploaded: s3://[bucket-name]/test-file.txt
```

## Cleanup

```bash
# Remove test files from S3
aws s3 rm s3://$BUCKET_NAME/test-file.txt

# Destroy infrastructure
terraform destroy
```

## Troubleshooting

### Lambda Not Triggered
- Verify S3 event notification is configured: Check S3 bucket properties
- Check Lambda permissions: Ensure S3 has permission to invoke Lambda
- Review CloudWatch logs for errors

### Permission Errors
- Verify IAM role has correct policies attached
- Check Lambda execution role has CloudWatch Logs permissions

## Monitoring

- **CloudWatch Logs**: `/aws/lambda/s3-lambda-trigger-hello-world`
- **CloudWatch Alarm**: `s3-lambda-trigger-errors` (triggers on >5 errors in 5 minutes)
- **Lambda Metrics**: Invocations, Duration, Errors in CloudWatch console
