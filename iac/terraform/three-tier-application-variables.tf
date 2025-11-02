# Changelog:
# AWS-3 - Initial three-tier application variables - 2025-01-27

variable "web_instance_type" {
  description = "Instance type for web tier"
  type        = string
  default     = "t3.medium"
}

variable "app_instance_type" {
  description = "Instance type for application tier"
  type        = string
  default     = "t3.large"
}