# Simple Website Implementation - AWS-4

## Overview

This implementation creates a simple static website hosted on AWS S3 with a "Hello World" page that is publicly accessible via the internet.

## Architecture

- **S3 Bucket**: Static website hosting with encryption and versioning
- **Security**: Public read-only access with proper bucket policies
- **Monitoring**: Access logging enabled
- **Content**: Responsive HTML/CSS Hello World page

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.1
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
│   ├── simple-website-main.tf
│   ├── simple-website-variables.tf
│   ├── simple-website-outputs.tf
│   ├── versions.tf
│   └── backend.tf
├── src/website/            # Static website files
│   ├── index.html
│   ├── styles.css
│   └── error.html
└── .gitignore
```

## Security Features

- Server-side encryption for S3 bucket
- S3 bucket versioning enabled
- Access logging configured
- Public read-only access (no write permissions)
- Proper IAM bucket policies

## Monitoring

- S3 access logs stored in the same bucket under `access-logs/` prefix
- CloudWatch metrics available for S3 bucket

## Cost Optimization

- S3 standard storage class
- Minimal data transfer costs
- Estimated cost: < $1 USD per month