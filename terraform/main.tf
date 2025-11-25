# Main Terraform configuration for IAM User Monitor

terraform {
  # Specify required Terraform version
  required_version = ">= 1.5.0"

  # Required provider versions
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # Backend configuration for state management
  # This uses S3 for state storage and DynamoDB for state locking
  # Uncomment and configure the backend block below when ready to use remote state
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "iam-user-monitor/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-state-lock"
  #   kms_key_id     = "arn:aws:kms:us-east-1:ACCOUNT_ID:key/KEY_ID"
  # }
}

# Configure the AWS Provider
provider "aws" {
  # Region can be set via AWS_REGION environment variable
  # or specified here directly
  # region = "us-east-1"

  # Default tags applied to all resources
  default_tags {
    tags = {
      Project     = "IAM User Monitor"
      ManagedBy   = "Terraform"
      Environment = terraform.workspace
    }
  }
}
