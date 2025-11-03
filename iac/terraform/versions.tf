# Changelog:
# AWS-5 - Initial provider version constraints - 2025-01-27

terraform {
  required_version = ">= 1.1"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}