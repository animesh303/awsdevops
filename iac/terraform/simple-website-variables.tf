# Changelog:
# AWS-4 - Initial variable definitions for simple website - 2025-01-27

variable "website_bucket_name" {
  description = "Name of the S3 bucket for static website hosting"
  type        = string
  default     = "simple-website-bucket-aws4"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}