# Changelog:
# AWS-6 - S3 bucket variables - 2025-01-27

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = null
}

variable "enable_versioning" {
  description = "Enable versioning for the S3 bucket"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable server-side encryption for the S3 bucket"
  type        = bool
  default     = true
}

variable "enable_access_logging" {
  description = "Enable access logging for the S3 bucket"
  type        = bool
  default     = true
}