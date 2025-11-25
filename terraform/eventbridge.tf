# EventBridge rule for scheduled Lambda invocation

# EventBridge rule to trigger Lambda function on schedule
resource "aws_cloudwatch_event_rule" "iam_monitor_schedule" {
  name                = "${var.dynamodb_table_name}-monitor-schedule"
  description         = "Triggers IAM user monitoring Lambda function on schedule"
  schedule_expression = var.monitoring_period
  state               = "ENABLED"

  tags = {
    Name        = "IAM User Monitor Schedule"
    ManagedBy   = "Terraform"
    Application = "iam-user-monitor"
  }
}

# EventBridge target - Lambda function
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.iam_monitor_schedule.name
  target_id = "IAMUserMonitorLambda"
  arn       = aws_lambda_function.iam_user_monitor.arn
}

# Lambda permission to allow EventBridge to invoke the function
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iam_user_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.iam_monitor_schedule.arn
}
