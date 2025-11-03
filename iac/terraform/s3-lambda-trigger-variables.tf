# Changelog:
# AWS-5 - Initial variables for S3 Lambda trigger - 2025-01-27

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "aws-s3-lambda-trigger-demo"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "s3-lambda-trigger-hello-world"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for tagging"
  type        = string
  default     = "s3-lambda-trigger"
}