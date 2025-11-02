# Changelog:
# AWS-3 - Initial variable definitions for two-tier web app - 2025-01-27

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "two-tier-web-app"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "web_instance_type" {
  description = "Instance type for web tier"
  type        = string
  default     = "t3.medium"
}

variable "app_instance_type" {
  description = "Instance type for app tier"
  type        = string
  default     = "t3.large"
}