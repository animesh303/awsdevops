# Changelog:
# AWS-15 - Initial S3 bucket with lifecycle policy - 2025-01-28

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "lifecycle_demo" {
  bucket = "s3-lifecycle-demo-bucket-${random_id.bucket_suffix.hex}"

  tags = {
    JiraId      = "AWS-15"
    ManagedBy   = "Terraform"
    Environment = "demo"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lifecycle_demo" {
  bucket = aws_s3_bucket.lifecycle_demo.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "lifecycle_demo" {
  bucket = aws_s3_bucket.lifecycle_demo.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle_demo" {
  bucket = aws_s3_bucket.lifecycle_demo.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    filter {}

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
  }

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    filter {}

    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }

  rule {
    id     = "delete-old-objects"
    status = "Enabled"

    filter {}

    expiration {
      days = 365
    }
  }
}
