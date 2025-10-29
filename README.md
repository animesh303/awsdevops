# AWS EC2 and Lambda Sample Project

This project demonstrates how to provision AWS resources including an EC2 instance and Lambda function using Terraform.

## Architecture

- **EC2 Instance**: A simple web server running in a public subnet
- **Lambda Function**: A serverless function that can be triggered via API Gateway
- **VPC**: Custom VPC with public subnet for the EC2 instance
- **Security Groups**: Proper security configurations for both resources

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (version >= 1.0)
- An existing AWS key pair for EC2 access

## Quick Start

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Plan the deployment:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

4. Clean up resources:
   ```bash
   terraform destroy
   ```

## Project Structure

```
├── main.tf              # Main Terraform configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── lambda/
│   └── index.js         # Lambda function code
└── user-data.sh         # EC2 initialization script
```