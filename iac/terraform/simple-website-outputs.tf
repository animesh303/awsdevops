# Changelog:
# AWS-4 - Initial output definitions for simple website - 2025-01-27

output "website_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.website.bucket
}

output "website_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.website.arn
}

output "website_url" {
  description = "Website URL"
  value       = "http://${aws_s3_bucket_website_configuration.website.website_endpoint}"
}

output "website_domain" {
  description = "Website domain"
  value       = aws_s3_bucket_website_configuration.website.website_domain
}