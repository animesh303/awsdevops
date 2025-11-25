# DynamoDB table for storing IAM user records

resource "aws_dynamodb_table" "iam_user_records" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"

  # Composite primary key
  hash_key  = "user_name"
  range_key = "scan_timestamp"

  # Partition key attribute
  attribute {
    name = "user_name"
    type = "S"
  }

  # Sort key attribute
  attribute {
    name = "scan_timestamp"
    type = "S"
  }

  # Global secondary index on scan_timestamp for time-based queries
  global_secondary_index {
    name            = "scan-timestamp-index"
    hash_key        = "scan_timestamp"
    projection_type = "ALL"
  }

  # Enable TTL on ttl attribute for automatic record expiration
  ttl {
    enabled        = true
    attribute_name = "ttl"
  }

  # Enable encryption at rest using AWS managed keys
  server_side_encryption {
    enabled = true
  }

  # Enable point-in-time recovery for data protection
  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name      = "IAM User Records"
    ManagedBy = "Terraform"
    Purpose   = "IAM User Monitoring"
  }
}
