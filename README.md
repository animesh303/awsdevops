# AWS Static Website Infrastructure

## Overview

This project implements AWS-2 requirements: a static website hosted on S3 with supporting AWS services including DynamoDB and SQS.

## Architecture

- **S3 Bucket**: Static website hosting with encryption and versioning
- **DynamoDB Table**: NoSQL data storage with on-demand billing
- **SQS Queue**: Message queuing with encryption
- **CloudWatch**: Monitoring and logging

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- AWS Provider ~> 5.0

## Quick Start

### 1. Deploy Infrastructure

```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 2. Upload Website Files

```bash
# Get bucket name from Terraform output
BUCKET_NAME=$(terraform output -raw website_bucket_name)

# Upload website files
aws s3 cp ../../src/website/ s3://$BUCKET_NAME/ --recursive
```

### 3. Access Website

```bash
# Get website URL
terraform output website_url
```

## Project Structure

```
├── iac/terraform/          # Infrastructure as Code
│   ├── static-website-infrastructure-main.tf
│   ├── static-website-infrastructure-variables.tf
│   ├── static-website-infrastructure-outputs.tf
│   └── versions.tf
├── src/website/            # Static website files
│   ├── index.html
│   ├── styles.css
│   └── error.html
└── README.md
```

## Security Features

- Server-side encryption for all services
- S3 bucket versioning enabled
- Access logging configured
- Least privilege IAM policies
- Public access limited to website content only

## Monitoring

- CloudWatch logs for S3 access
- DynamoDB and SQS metrics available in CloudWatch console

## Cost Optimization

- DynamoDB on-demand billing
- S3 standard storage class
- No unnecessary data transfer costs