# Deployment Guide

## Prerequisites

1. **AWS Account**: Ensure you have AWS account access
2. **Terraform Cloud**: Configure workspace in Terraform Cloud
3. **AWS CLI**: Install and configure AWS CLI
4. **Terraform**: Install Terraform >= 1.1

## Step-by-Step Deployment

### 1. Configure Backend

Update `iac/terraform/backend.tf` with your Terraform Cloud settings:

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

### 2. Set Variables

Create `terraform.tfvars` file:

```hcl
aws_region = "us-east-1"
environment = "dev"
project_name = "two-tier-web-app"
vpc_cidr = "10.0.0.0/16"
web_instance_type = "t3.medium"
app_instance_type = "t3.large"
```

### 3. Deploy Infrastructure

```bash
cd iac/terraform
terraform init
terraform plan
terraform apply
```

### 4. Verify Deployment

```bash
# Check outputs
terraform output

# Test load balancer
curl $(terraform output -raw load_balancer_url)
```

## Environment-Specific Deployments

### Development
```bash
terraform workspace new dev
terraform apply -var="environment=dev"
```

### Production
```bash
terraform workspace new prod
terraform apply -var="environment=prod" -var="web_instance_type=t3.large"
```

## Cleanup

```bash
terraform destroy
```