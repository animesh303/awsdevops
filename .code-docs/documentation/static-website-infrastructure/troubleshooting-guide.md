# Troubleshooting Guide - Static Website Infrastructure

## Common Issues and Solutions

### 1. Terraform Issues

#### Error: Access Denied
**Problem**: AWS credentials not configured or insufficient permissions
**Solution**:
```bash
# Configure AWS CLI
aws configure

# Verify credentials
aws sts get-caller-identity

# Check required permissions: S3, DynamoDB, SQS, CloudWatch, IAM
```

#### Error: Bucket already exists
**Problem**: S3 bucket name conflict
**Solution**: Terraform uses `bucket_prefix` to generate unique names automatically

#### Error: Provider version conflict
**Problem**: Terraform provider version mismatch
**Solution**:
```bash
terraform init -upgrade
```

### 2. Website Access Issues

#### Website returns 403 Forbidden
**Problem**: S3 bucket policy or public access settings
**Solution**:
1. Check bucket policy allows public read access
2. Verify public access block settings
3. Ensure files are uploaded to bucket

#### Website returns 404 Not Found
**Problem**: Missing index.html or incorrect configuration
**Solution**:
```bash
# Check if files exist in bucket
aws s3 ls s3://your-bucket-name/

# Re-upload if missing
aws s3 cp src/website/ s3://your-bucket-name/ --recursive
```

### 3. Resource Access Issues

#### Cannot access DynamoDB table
**Problem**: Table not created or access permissions
**Solution**:
```bash
# Verify table exists
aws dynamodb describe-table --table-name sample-data-table

# Check table status in Terraform
terraform show | grep dynamodb
```

#### Cannot access SQS queue
**Problem**: Queue not created or access permissions
**Solution**:
```bash
# List queues
aws sqs list-queues

# Get queue URL
aws sqs get-queue-url --queue-name sample-message-queue
```

### 4. Monitoring Issues

#### CloudWatch logs not appearing
**Problem**: Log group not created or no activity
**Solution**:
1. Verify log group exists in CloudWatch console
2. Check S3 access logs are being generated
3. Wait for log delivery (can take several minutes)

## Diagnostic Commands

### Check Infrastructure Status
```bash
# Terraform state
terraform show

# AWS resources
aws s3 ls
aws dynamodb list-tables
aws sqs list-queues
aws logs describe-log-groups
```

### Test Connectivity
```bash
# Test website
curl -I http://$(terraform output -raw website_url)

# Test DynamoDB
aws dynamodb scan --table-name sample-data-table --max-items 1

# Test SQS
aws sqs get-queue-attributes --queue-url $(terraform output -raw sqs_queue_url)
```

## Recovery Procedures

### Redeploy Infrastructure
```bash
# Destroy and recreate
terraform destroy
terraform apply
```

### Reset Website Content
```bash
# Clear bucket and re-upload
aws s3 rm s3://$(terraform output -raw website_bucket_name) --recursive
aws s3 cp src/website/ s3://$(terraform output -raw website_bucket_name)/ --recursive
```

## Support Resources

- AWS Documentation: https://docs.aws.amazon.com/
- Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/
- AWS CLI Reference: https://docs.aws.amazon.com/cli/