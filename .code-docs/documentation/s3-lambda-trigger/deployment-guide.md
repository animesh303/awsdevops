# Deployment Guide - S3 Lambda Trigger

## Step-by-Step Deployment

### 1. Prepare Environment
```bash
# Ensure AWS credentials are configured
aws sts get-caller-identity

# Navigate to project directory
cd /path/to/awsdevops
```

### 2. Deploy Infrastructure
```bash
# Navigate to Terraform directory
cd iac/terraform

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure changes
terraform apply
```

### 3. Package and Deploy Lambda Code
```bash
# Navigate to Lambda source directory
cd ../../src/lambda-s3-lambda-trigger

# Create deployment package
zip -r ../../iac/terraform/lambda_function.zip .

# Return to Terraform directory and update Lambda
cd ../../iac/terraform
terraform apply
```

### 4. Verify Deployment
```bash
# Check S3 bucket exists
aws s3 ls | grep aws-s3-lambda-trigger-demo

# Check Lambda function exists
aws lambda get-function --function-name s3-lambda-trigger-hello-world

# Check CloudWatch log group exists
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/s3-lambda-trigger-hello-world"
```

### 5. Test the Integration
```bash
# Create a test file
echo "Hello World Test" > test-file.txt

# Upload to S3 bucket
aws s3 cp test-file.txt s3://aws-s3-lambda-trigger-demo/

# Check Lambda logs
aws logs tail /aws/lambda/s3-lambda-trigger-hello-world --follow
```

## Troubleshooting

### Common Issues
1. **Lambda function not triggered**: Check S3 event notification configuration
2. **Permission denied**: Verify IAM role has correct policies
3. **Function timeout**: Check Lambda timeout settings (default: 30s)

### Cleanup
```bash
# Remove test files from S3
aws s3 rm s3://aws-s3-lambda-trigger-demo/ --recursive

# Destroy infrastructure
terraform destroy
```