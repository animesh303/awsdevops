# Changelog:
# AWS-2 - Initial backend configuration - 2025-01-27

terraform {
  cloud {
    organization = "aws-devops-ai"
    workspaces {
      name = "ws-terraform"
    }
  }
}