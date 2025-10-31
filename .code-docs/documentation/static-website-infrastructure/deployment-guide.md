# Deployment Guide - AWS Static Website Infrastructure

## Prerequisites

1. **AWS CLI**: Configured with appropriate credentials
2. **Terraform**: Version >= 1.0 installed
3. **Backend Configuration**: Update `iac/terraform/backend.tf` with your Terraform Cloud settings

## Step-by-Step Deployment

### 1. Configure Backend

Update `iac/terraform/backend.tf`:
```hcl
terraform {
  cloud {
    organization = "your-org-name"
    workspaces {
      name = "your-workspace-name"
    }
  }
}
```

### 2. Deploy Infrastructure

```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 3. Upload Website Content

```bash
# Get bucket name
BUCKET_NAME=$(terraform output -raw website_bucket_name)

# Upload files
aws s3 cp ../../src/website/ s3://$BUCKET_NAME/ --recursive
```

### 4. Verify Deployment

```bash
# Get website URL
terraform output website_url

# Test DynamoDB table
aws dynamodb describe-table --table-name $(terraform output -raw dynamodb_table_name)

# Test SQS queue
aws sqs get-queue-attributes --queue-url $(terraform output -raw sqs_queue_url)
```

## Troubleshooting

- **Backend Error**: Ensure Terraform Cloud organization and workspace exist
- **Permission Error**: Verify AWS credentials have required permissions
- **Website Not Loading**: Check S3 bucket policy and public access settings