# Changelog:
# AWS-15 - Initial outputs for S3 lifecycle demo - 2025-01-28

output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.lifecycle_demo.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.lifecycle_demo.arn
}

output "bucket_region" {
  description = "Region of the S3 bucket"
  value       = aws_s3_bucket.lifecycle_demo.region
}
