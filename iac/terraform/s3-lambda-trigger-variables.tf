# Changelog:
# AWS-5 - Initial variables for S3 Lambda trigger - 2025-01-27

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "demobucketforawsaidevops"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "hello-world-s3-trigger"
}

variable "jira_id" {
  description = "JIRA ticket ID for resource tagging"
  type        = string
  default     = "AWS-5"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}