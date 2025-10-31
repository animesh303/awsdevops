# Changelog:
# AWS-3 - Initial backend configuration for three-tier application - 2025-01-27

terraform {
  cloud {
    organization = "aws-devops-ai"
    workspaces {
      name = "ws-terraform"
    }
  }
}