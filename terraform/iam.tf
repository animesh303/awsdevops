# IAM role for Lambda function execution
resource "aws_iam_role" "lambda_execution_role" {
  name               = "${var.dynamodb_table_name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = {
    Name        = "IAM User Monitor Lambda Role"
    ManagedBy   = "Terraform"
    Application = "iam-user-monitor"
  }
}

# Trust policy allowing Lambda service to assume the role
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Attach AWS managed policy for basic Lambda execution (CloudWatch Logs)
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Inline policy for IAM read permissions
resource "aws_iam_role_policy" "iam_read_policy" {
  name   = "iam-read-permissions"
  role   = aws_iam_role.lambda_execution_role.id
  policy = data.aws_iam_policy_document.iam_read.json
}

data "aws_iam_policy_document" "iam_read" {
  statement {
    effect = "Allow"

    actions = [
      "iam:ListUsers",
      "iam:GetUser"
    ]

    resources = ["*"]
  }
}

# Inline policy for DynamoDB write permissions
resource "aws_iam_role_policy" "dynamodb_write_policy" {
  name   = "dynamodb-write-permissions"
  role   = aws_iam_role.lambda_execution_role.id
  policy = data.aws_iam_policy_document.dynamodb_write.json
}

data "aws_iam_policy_document" "dynamodb_write" {
  statement {
    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:BatchWriteItem"
    ]

    resources = [
      aws_dynamodb_table.iam_user_records.arn
    ]
  }
}

# Inline policy for CloudWatch custom metrics
resource "aws_iam_role_policy" "cloudwatch_metrics_policy" {
  name   = "cloudwatch-metrics-permissions"
  role   = aws_iam_role.lambda_execution_role.id
  policy = data.aws_iam_policy_document.cloudwatch_metrics.json
}

data "aws_iam_policy_document" "cloudwatch_metrics" {
  statement {
    effect = "Allow"

    actions = [
      "cloudwatch:PutMetricData"
    ]

    resources = ["*"]
  }
}
