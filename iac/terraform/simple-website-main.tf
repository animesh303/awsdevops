# Changelog:
# AWS-4 - Initial S3 static website infrastructure creation - 2025-01-27

# S3 bucket for static website hosting
resource "aws_s3_bucket" "website" {
  bucket = var.website_bucket_name

  tags = {
    Name        = "Simple Website Bucket"
    Environment = var.environment
    JiraId      = "AWS-4"
    ManagedBy   = "terraform"
  }
}

# S3 bucket website configuration
resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

# S3 bucket versioning
resource "aws_s3_bucket_versioning" "website" {
  bucket = aws_s3_bucket.website.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 bucket server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 bucket public access block (allow public read for website)
resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Wait for public access block changes to propagate before applying bucket policy
resource "time_sleep" "wait_for_public_access_block" {
  depends_on = [aws_s3_bucket_public_access_block.website]

  create_duration = "10s"
}

# S3 bucket policy for public read access
resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id

  # Ensure public access block is updated and propagated before applying policy
  depends_on = [
    aws_s3_bucket_public_access_block.website,
    time_sleep.wait_for_public_access_block
  ]

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
}

# S3 bucket logging
resource "aws_s3_bucket_logging" "website" {
  bucket = aws_s3_bucket.website.id

  target_bucket = aws_s3_bucket.website.id
  target_prefix = "access-logs/"
}
