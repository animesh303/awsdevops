# Changelog:
# AWS-5 - Initial outputs for S3 Lambda trigger - 2025-01-27

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.trigger_bucket.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.trigger_bucket.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.hello_world.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.hello_world.arn
}

output "iam_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_execution_role.arn
}