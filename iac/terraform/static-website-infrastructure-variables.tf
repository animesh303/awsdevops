# Changelog:
# AWS-2 - Initial variable definitions for static website infrastructure - 2025-01-27
# AWS-2 - Enhanced tagging strategy implementation - 2025-01-27

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

variable "project_name" {
  description = "Name of the project for resource tagging"
  type        = string
  default     = "static-website"
}

variable "cost_center" {
  description = "Cost center for billing and cost allocation"
  type        = string
  default     = "engineering"
}

variable "owner" {
  description = "Owner or team responsible for the resources"
  type        = string
  default     = "devops-team"
}

variable "backup_required" {
  description = "Whether resources require backup"
  type        = bool
  default     = true
}

variable "compliance_level" {
  description = "Compliance level for the resources"
  type        = string
  default     = "standard"
  validation {
    condition     = contains(["low", "standard", "high", "critical"], var.compliance_level)
    error_message = "Compliance level must be one of: low, standard, high, critical."
  }
}