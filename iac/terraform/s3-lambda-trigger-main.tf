# Changelog:
# AWS-5 - Initial S3 Lambda trigger infrastructure - 2025-01-27

# S3 Bucket
resource "aws_s3_bucket" "trigger_bucket" {
  bucket = var.bucket_name

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    Project     = var.project_name
    JiraId      = "AWS-5"
    ManagedBy   = "terraform"
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "trigger_bucket_versioning" {
  bucket = aws_s3_bucket.trigger_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.lambda_function_name}-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.lambda_function_name}-execution-role"
    Environment = var.environment
    Project     = var.project_name
    JiraId      = "AWS-5"
    ManagedBy   = "terraform"
  }
}

# IAM Policy for Lambda
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "${var.lambda_function_name}-s3-policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = "${aws_s3_bucket.trigger_bucket.arn}/*"
      }
    ]
  })
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 14

  tags = {
    Name        = "/aws/lambda/${var.lambda_function_name}"
    Environment = var.environment
    Project     = var.project_name
    JiraId      = "AWS-5"
    ManagedBy   = "terraform"
  }
}

# Lambda Function
resource "aws_lambda_function" "hello_world" {
  filename      = "lambda_function.zip"
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.9"
  memory_size   = 128
  timeout       = 30

  depends_on = [
    aws_iam_role_policy.lambda_s3_policy,
    aws_cloudwatch_log_group.lambda_logs,
  ]

  tags = {
    Name        = var.lambda_function_name
    Environment = var.environment
    Project     = var.project_name
    JiraId      = "AWS-5"
    ManagedBy   = "terraform"
  }
}

# Lambda Permission for S3
resource "aws_lambda_permission" "s3_invoke" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello_world.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.trigger_bucket.arn
}

# S3 Bucket Notification
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.trigger_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.hello_world.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.s3_invoke]
}