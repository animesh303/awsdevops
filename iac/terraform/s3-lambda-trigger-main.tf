# Changelog:
# AWS-17 - Initial S3 bucket and Lambda function infrastructure - 2025-01-28

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "trigger_bucket" {
  bucket = "s3-lambda-trigger-demo-${random_id.bucket_suffix.hex}"

  tags = {
    Name      = "s3-lambda-trigger-demo"
    JiraId    = "AWS-17"
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "trigger_bucket" {
  bucket = aws_s3_bucket.trigger_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "trigger_bucket" {
  bucket = aws_s3_bucket.trigger_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "lambda_role" {
  name = "s3-lambda-trigger-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    JiraId    = "AWS-17"
    ManagedBy = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_s3_read" {
  name = "s3-read-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.trigger_bucket.arn,
        "${aws_s3_bucket.trigger_bucket.arn}/*"
      ]
    }]
  })
}

resource "aws_lambda_function" "s3_trigger" {
  filename         = "${path.module}/lambda_function.zip"
  function_name    = "s3-lambda-trigger-hello-world"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_handler.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/lambda_function.zip")
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 128

  tags = {
    JiraId    = "AWS-17"
    ManagedBy = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.s3_trigger.function_name}"
  retention_in_days = 7

  tags = {
    JiraId    = "AWS-17"
    ManagedBy = "Terraform"
  }
}

resource "aws_lambda_permission" "s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.trigger_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.trigger_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_trigger.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.s3_invoke]
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "s3-lambda-trigger-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Alert when Lambda errors exceed 5 in 5 minutes"

  dimensions = {
    FunctionName = aws_lambda_function.s3_trigger.function_name
  }

  tags = {
    JiraId    = "AWS-17"
    ManagedBy = "Terraform"
  }
}
