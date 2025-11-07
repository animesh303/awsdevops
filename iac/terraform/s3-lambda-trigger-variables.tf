# Changelog:
# AWS-5 - Initial S3 Lambda trigger variables - 2025-01-28

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "demobucketforawsaidevops"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "hello_world"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}