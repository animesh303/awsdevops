# Changelog:
# AWS-2 - Initial static website infrastructure creation - 2025-01-27

# S3 Bucket for static website hosting
resource "aws_s3_bucket" "website" {
  bucket = var.website_bucket_name

  tags = {
    JiraId    = var.jira_id
    ManagedBy = "terraform"
    Name      = "Static Website Bucket"
  }
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_versioning" "website" {
  bucket = aws_s3_bucket.website.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.website.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.website]
}

# DynamoDB Table
resource "aws_dynamodb_table" "sample_data" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
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

  tags = {
    JiraId    = var.jira_id
    ManagedBy = "terraform"
    Name      = "Sample Data Table"
  }
}

# SQS Queue
resource "aws_sqs_queue" "sample_queue" {
  name                       = var.sqs_queue_name
  message_retention_seconds  = 1209600
  visibility_timeout_seconds = 30

  kms_master_key_id = "alias/aws/sqs"

  tags = {
    JiraId    = var.jira_id
    ManagedBy = "terraform"
    Name      = "Sample Message Queue"
  }
}

# CloudWatch Log Group for monitoring
resource "aws_cloudwatch_log_group" "website_logs" {
  name              = "/aws/s3/${var.website_bucket_name}"
  retention_in_days = 14

  tags = {
    JiraId    = var.jira_id
    ManagedBy = "terraform"
    Name      = "Website Access Logs"
  }
}