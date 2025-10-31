# Changelog:
# AWS-2 - Initial variable definitions for static website infrastructure - 2025-01-27

variable "jira_id" {
  description = "JIRA ticket ID for resource tagging"
  type        = string
  default     = "AWS-2"
}

variable "website_bucket_name" {
  description = "Name of the S3 bucket for static website hosting"
  type        = string
  default     = "aws-static-website-bucket-unique-12345"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "sample-data-table"
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue"
  type        = string
  default     = "sample-message-queue"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}