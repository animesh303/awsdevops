# Deployment Guide - Static Website Infrastructure

## Prerequisites

1. **AWS CLI**: Configured with appropriate credentials
2. **Terraform**: Version >= 1.0 installed
3. **AWS Permissions**: Required permissions for S3, DynamoDB, SQS, CloudWatch

## Step-by-Step Deployment

### 1. Initialize Terraform

```bash
cd iac/terraform
terraform init
```

### 2. Review Configuration

```bash
# Review variables (optional)
cat static-website-infrastructure-variables.tf

# Customize if needed
export TF_VAR_environment="production"
export TF_VAR_aws_region="us-east-1"
```

### 3. Plan Deployment

```bash
terraform plan
```

### 4. Deploy Infrastructure

```bash
terraform apply
# Type 'yes' when prompted
```

### 5. Upload Website Content

```bash
# Get bucket name
BUCKET_NAME=$(terraform output -raw website_bucket_name)

# Upload files
aws s3 cp ../../src/website/ s3://$BUCKET_NAME/ --recursive

# Verify upload
aws s3 ls s3://$BUCKET_NAME/
```

### 6. Test Website

```bash
# Get website URL
WEBSITE_URL=$(terraform output -raw website_url)
echo "Website URL: http://$WEBSITE_URL"

# Test in browser or curl
curl http://$WEBSITE_URL
```

## Verification Steps

### 1. S3 Bucket
- Bucket created with website hosting enabled
- Public read access configured
- Versioning enabled
- Encryption enabled

### 2. DynamoDB Table
- Table created with on-demand billing
- Encryption at rest enabled
- Point-in-time recovery enabled

### 3. SQS Queue
- Queue created with encryption
- 14-day message retention
- 30-second visibility timeout

### 4. CloudWatch
- Log group created for monitoring

## Troubleshooting

### Common Issues

1. **Access Denied**: Check AWS credentials and permissions
2. **Bucket Name Conflict**: Terraform will generate unique name with prefix
3. **Website Not Loading**: Verify S3 bucket policy and public access settings

### Useful Commands

```bash
# Check Terraform state
terraform show

# View outputs
terraform output

# Destroy infrastructure (if needed)
terraform destroy
```