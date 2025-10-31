# Changelog:
# AWS-2 - Initial output definitions for static website infrastructure - 2025-01-27

output "website_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.website.bucket
}

output "website_url" {
  description = "URL of the static website"
  value       = "http://${aws_s3_bucket.website.bucket}.s3-website-${data.aws_region.current.name}.amazonaws.com"
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.sample_data.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.sample_data.arn
}

output "sqs_queue_name" {
  description = "Name of the SQS queue"
  value       = aws_sqs_queue.sample_queue.name
}

output "sqs_queue_url" {
  description = "URL of the SQS queue"
  value       = aws_sqs_queue.sample_queue.url
}

data "aws_region" "current" {}