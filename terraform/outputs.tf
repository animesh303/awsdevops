# Terraform output values for IAM User Monitor

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table storing IAM user records"
  value       = aws_dynamodb_table.iam_user_records.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table storing IAM user records"
  value       = aws_dynamodb_table.iam_user_records.arn
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function that monitors IAM users"
  value       = aws_lambda_function.iam_user_monitor.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function that monitors IAM users"
  value       = aws_lambda_function.iam_user_monitor.function_name
}

output "eventbridge_rule_name" {
  description = "Name of the EventBridge rule that triggers the monitoring"
  value       = aws_cloudwatch_event_rule.iam_monitor_schedule.name
}

output "eventbridge_rule_arn" {
  description = "ARN of the EventBridge rule that triggers the monitoring"
  value       = aws_cloudwatch_event_rule.iam_monitor_schedule.arn
}

output "lambda_execution_role_arn" {
  description = "ARN of the IAM role used by the Lambda function"
  value       = aws_iam_role.lambda_execution_role.arn
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch Log Group for Lambda function logs"
  value       = aws_cloudwatch_log_group.lambda_log_group.name
}
