# Changelog:
# AWS-2 - Initial variable definitions for static website infrastructure - 2025-01-27

variable "environment" {
  description = "Environment name for resource tagging"
  type        = string
  default     = "production"
}

variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
}