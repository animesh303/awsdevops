# Changelog:
# AWS-3 - Initial provider version constraints for three-tier application - 2025-01-27

terraform {
  required_version = ">= 1.1"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}