# Changelog:
# AWS-17 - Terraform outputs for S3 Lambda trigger - 2025-01-28

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.trigger_bucket.id
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.s3_trigger.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.s3_trigger.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}
