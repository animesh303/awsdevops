# Changelog:
# AWS-6 - S3 bucket outputs - 2025-01-27

output "s3_bucket_id" {
  description = "ID of the S3 bucket"
  value       = aws_s3_bucket.main.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.main.arn
}

output "s3_bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  value       = aws_s3_bucket.main.bucket_domain_name
}

output "s3_bucket_regional_domain_name" {
  description = "Regional domain name of the S3 bucket"
  value       = aws_s3_bucket.main.bucket_regional_domain_name
}

output "s3_bucket_policy_arn" {
  description = "ARN of the IAM policy for S3 bucket access"
  value       = aws_iam_policy.s3_bucket_policy.arn
}

output "access_logs_bucket_id" {
  description = "ID of the access logs S3 bucket"
  value       = var.enable_access_logging ? aws_s3_bucket.access_logs[0].id : null
}