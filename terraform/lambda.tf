# Lambda function for IAM user monitoring

# Data source to get current AWS region
data "aws_region" "current" {}

# Data source to get current AWS account ID
data "aws_caller_identity" "current" {}

# CloudWatch Log Group for Lambda function
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.dynamodb_table_name}-monitor"
  retention_in_days = 30
  kms_key_id        = aws_kms_key.lambda_logs.arn

  tags = {
    Name        = "IAM User Monitor Lambda Logs"
    ManagedBy   = "Terraform"
    Application = "iam-user-monitor"
  }
}

# KMS key for CloudWatch Logs encryption
resource "aws_kms_key" "lambda_logs" {
  description             = "KMS key for Lambda CloudWatch Logs encryption"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = {
    Name        = "IAM User Monitor Lambda Logs KMS Key"
    ManagedBy   = "Terraform"
    Application = "iam-user-monitor"
  }
}

# KMS key alias
resource "aws_kms_alias" "lambda_logs" {
  name          = "alias/${var.dynamodb_table_name}-lambda-logs"
  target_key_id = aws_kms_key.lambda_logs.key_id
}

# KMS key policy to allow CloudWatch Logs to use the key
resource "aws_kms_key_policy" "lambda_logs" {
  key_id = aws_kms_key.lambda_logs.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow CloudWatch Logs"
        Effect = "Allow"
        Principal = {
          Service = "logs.${data.aws_region.current.id}.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:CreateGrant",
          "kms:DescribeKey"
        ]
        Resource = "*"
        Condition = {
          ArnLike = {
            "kms:EncryptionContext:aws:logs:arn" = "arn:aws:logs:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.dynamodb_table_name}-monitor"
          }
        }
      }
    ]
  })
}

# Lambda function
resource "aws_lambda_function" "iam_user_monitor" {
  filename         = "${path.module}/../lambda/lambda_deployment.zip"
  function_name    = "${var.dynamodb_table_name}-monitor"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/../lambda/lambda_deployment.zip")
  runtime          = "python3.11"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.iam_user_records.name
      LOG_LEVEL           = var.log_level
    }
  }

  # Ensure CloudWatch Log Group is created before Lambda function
  depends_on = [
    aws_cloudwatch_log_group.lambda_log_group,
    aws_iam_role_policy_attachment.lambda_basic_execution
  ]

  tags = {
    Name        = "IAM User Monitor Lambda"
    ManagedBy   = "Terraform"
    Application = "iam-user-monitor"
  }
}
