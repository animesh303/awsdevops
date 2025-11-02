# Two-Tier Web Application Infrastructure

## Overview

This infrastructure implements AWS-3 requirements: a two-tier web application architecture using EC2, S3, and supporting AWS services.

## Architecture

- **Web Tier**: EC2 instances with Application Load Balancer in public subnets
- **Application Tier**: EC2 instances in private subnets
- **Storage**: S3 bucket with encryption and versioning
- **Network**: Custom VPC with public/private subnets across 2 AZs

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.1
- Terraform Cloud workspace configured

## Quick Start

### 1. Deploy Infrastructure

```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 2. Access Resources

```bash
# Get load balancer URL
terraform output load_balancer_url

# Get S3 bucket name
terraform output s3_bucket_name
```

## Infrastructure Components

### Networking
- VPC with CIDR 10.0.0.0/16
- 2 public subnets (10.0.1.0/24, 10.0.2.0/24)
- 2 private subnets (10.0.10.0/24, 10.0.11.0/24)
- Internet Gateway and NAT Gateway
- Route tables with proper associations

### Compute
- Web tier: t3.medium instances (Auto Scaling 2-4)
- App tier: t3.large instances (Auto Scaling 2-4)
- Application Load Balancer with health checks

### Storage
- S3 bucket with server-side encryption
- Versioning enabled
- IAM roles for EC2 S3 access

### Security
- Security groups with least privilege access
- IAM roles and policies
- All resources tagged with JiraId and ManagedBy

## Outputs

- `vpc_id`: VPC identifier
- `load_balancer_dns`: ALB DNS name
- `load_balancer_url`: Complete ALB URL
- `s3_bucket_name`: S3 bucket name
- `s3_bucket_arn`: S3 bucket ARN

## Customization

Modify variables in `two-tier-web-app-variables.tf`:
- `aws_region`: Target AWS region
- `environment`: Environment name
- `vpc_cidr`: VPC CIDR block
- `web_instance_type`: Web tier instance type
- `app_instance_type`: App tier instance type