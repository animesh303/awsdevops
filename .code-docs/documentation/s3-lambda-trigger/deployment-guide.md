# Deployment Guide - S3 Lambda Trigger

## Step-by-Step Deployment

### 1. Prepare Environment

```bash
# Navigate to project root
cd /path/to/genai-devops

# Verify Terraform installation
terraform version  # Should be >= 1.1

# Configure AWS credentials (if not already done)
aws configure
```

### 2. Package Lambda Function

```bash
# Navigate to Lambda source directory
cd src/lambda-python-s3-lambda-trigger

# Create deployment package
zip -r lambda_function.zip lambda_handler.py

# Copy to Terraform directory
cp lambda_function.zip ../../iac/terraform/
```

### 3. Deploy Infrastructure

```bash
# Navigate to Terraform directory
cd iac/terraform

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply infrastructure changes
terraform apply
# Type 'yes' when prompted
```

### 4. Verify Deployment

```bash
# Check S3 bucket creation
aws s3 ls | grep demobucketforawsaidevops

# Check Lambda function
aws lambda get-function --function-name hello-world-s3-trigger

# Check CloudWatch log group
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/hello-world-s3-trigger"
```

### 5. Test the Integration

```bash
# Create a test file
echo "Hello World Test" > test-upload.txt

# Upload to S3 bucket
aws s3 cp test-upload.txt s3://demobucketforawsaidevops/

# Monitor Lambda logs (in separate terminal)
aws logs tail /aws/lambda/hello-world-s3-trigger --follow
```

## Troubleshooting

### Common Issues

1. **Terraform Cloud Authentication**
   - Ensure TFC_TOKEN is set in environment
   - Verify workspace permissions

2. **Lambda Package Missing**
   - Ensure lambda_function.zip exists in iac/terraform/
   - Re-run packaging steps if needed

3. **S3 Permissions**
   - Verify AWS credentials have S3 and Lambda permissions
   - Check IAM policies are correctly applied