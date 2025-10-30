# Changelog:
# AWS-2 - Initial static website infrastructure creation - 2025-01-27
# AWS-2 - Enhanced tagging strategy implementation - 2025-01-27

# S3 Bucket for static website hosting
resource "aws_s3_bucket" "website_bucket" {
  bucket_prefix = "static-website-"

  tags = merge(local.s3_tags, {
    Name = "Static Website Bucket"
  })
}

# S3 Bucket website configuration
resource "aws_s3_bucket_website_configuration" "website_config" {
  bucket = aws_s3_bucket.website_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

# S3 Bucket versioning
resource "aws_s3_bucket_versioning" "website_versioning" {
  bucket = aws_s3_bucket.website_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "website_encryption" {
  bucket = aws_s3_bucket.website_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket public access block (allow public read for website)
resource "aws_s3_bucket_public_access_block" "website_pab" {
  bucket = aws_s3_bucket.website_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# S3 Bucket policy for public read access
resource "aws_s3_bucket_policy" "website_policy" {
  bucket     = aws_s3_bucket.website_bucket.id
  depends_on = [aws_s3_bucket_public_access_block.website_pab]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.website_bucket.arn}/*"
      }
    ]
  })
}

# S3 Bucket logging
resource "aws_s3_bucket_logging" "website_logging" {
  bucket = aws_s3_bucket.website_bucket.id

  target_bucket = aws_s3_bucket.website_bucket.id
  target_prefix = "access-logs/"
}

# DynamoDB Table
resource "aws_dynamodb_table" "sample_data_table" {
  name         = "sample-data-table"
  billing_mode = "ON_DEMAND"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = merge(local.dynamodb_tags, {
    Name = "Sample Data Table"
  })
}

# SQS Queue
resource "aws_sqs_queue" "sample_message_queue" {
  name                       = "sample-message-queue"
  message_retention_seconds  = 1209600 # 14 days
  visibility_timeout_seconds = 30

  kms_master_key_id = "alias/aws/sqs"

  tags = merge(local.sqs_tags, {
    Name = "Sample Message Queue"
  })
}

# CloudWatch Log Group for monitoring
resource "aws_cloudwatch_log_group" "website_logs" {
  name              = "/aws/s3/static-website"
  retention_in_days = 14

  tags = merge(local.cloudwatch_tags, {
    Name = "Static Website Logs"
  })
}