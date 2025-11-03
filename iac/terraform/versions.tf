# Changelog:
# AWS-4 - Initial provider version constraints - 2025-01-27

terraform {
  required_version = ">= 1.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "simple-website"
      JiraId    = "AWS-4"
      ManagedBy = "terraform"
    }
  }
}