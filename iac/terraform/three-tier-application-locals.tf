# Changelog:
# AWS-3 - Local values and data sources for three-tier application - 2025-01-27

locals {
  common_tags = {
    JiraId      = var.jira_id
    ManagedBy   = "terraform"
    Environment = var.environment
    Project     = var.project_name
  }

  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24"]
  db_subnet_cidrs      = ["10.0.100.0/24", "10.0.200.0/24"]
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}