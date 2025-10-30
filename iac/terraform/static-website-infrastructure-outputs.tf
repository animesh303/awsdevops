# Changelog:
# AWS-2 - Initial output definitions for static website infrastructure - 2025-01-27

output "website_bucket_name" {
  description = "Name of the S3 bucket for static website"
  value       = aws_s3_bucket.website_bucket.id
}

output "website_url" {
  description = "URL of the static website"
  value       = aws_s3_bucket_website_configuration.website_config.website_endpoint
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.sample_data_table.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.sample_data_table.arn
}

output "sqs_queue_name" {
  description = "Name of the SQS queue"
  value       = aws_sqs_queue.sample_message_queue.name
}

output "sqs_queue_url" {
  description = "URL of the SQS queue"
  value       = aws_sqs_queue.sample_message_queue.url
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.website_logs.name
}