# Terraform input variables for IAM User Monitor

variable "monitoring_period" {
  description = "Schedule expression for how often to scan IAM users (e.g., 'rate(1 hour)' or 'cron(0 * * * ? *)')"
  type        = string
  default     = "rate(1 hour)"

  validation {
    condition     = can(regex("^(rate\\([0-9]+ (minute|minutes|hour|hours|day|days)\\)|cron\\(.+\\))$", var.monitoring_period))
    error_message = "The monitoring_period must be a valid EventBridge schedule expression (rate or cron format)."
  }
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table to store IAM user records"
  type        = string
  default     = "iam-user-records"

  validation {
    condition     = can(regex("^[a-zA-Z0-9_.-]+$", var.dynamodb_table_name)) && length(var.dynamodb_table_name) >= 3 && length(var.dynamodb_table_name) <= 255
    error_message = "The dynamodb_table_name must be between 3 and 255 characters and contain only alphanumeric characters, hyphens, underscores, and periods."
  }
}

variable "retention_days" {
  description = "Number of days to retain IAM user records in DynamoDB before automatic deletion via TTL"
  type        = number
  default     = 90

  validation {
    condition     = var.retention_days > 0 && var.retention_days <= 3650
    error_message = "The retention_days must be between 1 and 3650 (10 years)."
  }
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 300

  validation {
    condition     = var.lambda_timeout >= 1 && var.lambda_timeout <= 900
    error_message = "The lambda_timeout must be between 1 and 900 seconds (15 minutes)."
  }
}

variable "lambda_memory" {
  description = "Lambda function memory allocation in MB"
  type        = number
  default     = 256

  validation {
    condition     = var.lambda_memory >= 128 && var.lambda_memory <= 10240 && var.lambda_memory % 64 == 0
    error_message = "The lambda_memory must be between 128 and 10240 MB and must be a multiple of 64."
  }
}

variable "log_level" {
  description = "Logging level for Lambda function (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
  type        = string
  default     = "INFO"

  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], var.log_level)
    error_message = "The log_level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL."
  }
}
