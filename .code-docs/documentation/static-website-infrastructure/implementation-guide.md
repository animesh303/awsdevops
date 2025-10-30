# AWS-2 Implementation Guide

## Overview
Complete implementation of AWS static website infrastructure with S3, DynamoDB, and SQS.

## Architecture
- **S3 Bucket**: Static website hosting with public read access
- **DynamoDB Table**: NoSQL storage with PAY_PER_REQUEST billing
- **SQS Queue**: Message queuing with encryption
- **CloudWatch**: Monitoring and logging

## Deployment Instructions

### 1. Deploy Infrastructure
```bash
cd iac/terraform
terraform init
terraform plan -var-file=terraform.tfvars.example
terraform apply
```

### 2. Upload Website
```bash
BUCKET_NAME=$(terraform output -raw website_bucket_name)
aws s3 cp ../../src/website/ s3://$BUCKET_NAME/ --recursive
```

### 3. Access Website
```bash
terraform output website_url
```

## Security Features
- Server-side encryption for all services
- Enhanced tagging for cost management
- Least privilege access policies
- CloudWatch monitoring enabled

## Cost Optimization
- DynamoDB PAY_PER_REQUEST billing (no cost when unused)
- S3 standard storage class
- Minimal resource provisioning