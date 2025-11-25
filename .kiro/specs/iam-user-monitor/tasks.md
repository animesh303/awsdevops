# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create directory structure for Lambda function code and Terraform configuration
  - Create requirements.txt with boto3, hypothesis, and moto dependencies
  - Create Python package structure with separate modules for scanning, writing, metrics, and logging
  - _Requirements: 6.1, 6.2_

- [x] 2. Implement structured logging configuration
  - Create logger_config.py module that sets up structured JSON logging
  - Implement log formatter that ensures consistent field names across all log entries
  - Add configuration to read LOG_LEVEL from environment variable
  - _Requirements: 5.5_

- [x] 2.1 Write property test for structured logging consistency
  - **Property 7: Structured logging consistency**
  - **Validates: Requirements 5.5**

- [x] 3. Implement IAM user scanning logic
  - Create iam_scanner.py module with scan_iam_users() function
  - Implement pagination handling using boto3 IAM client paginator
  - Extract all required fields: user_name, user_id, arn, create_date, password_last_used
  - Handle missing optional fields (password_last_used)
  - Add error handling for IAM API failures with proper logging
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 4. Implement DynamoDB writer module
  - Create dynamodb_writer.py module with write_user_records() function
  - Format user records with all required attributes including scan_timestamp
  - Calculate and add TTL attribute based on retention period
  - Implement batch write operations (up to 25 items per batch)
  - Add error handling for DynamoDB write failures that continues processing remaining users
  - Log errors with affected user names
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 4.4_

- [x] 5. Implement CloudWatch metrics emitter
  - Create metrics_emitter.py module with emit_metrics() function
  - Emit custom metrics: UsersScanned, RecordsWritten, Errors, Duration, Success
  - Use boto3 CloudWatch client to publish metrics
  - Add error handling for metric emission failures (non-blocking)
  - _Requirements: 3.4_

- [x] 6. Implement Lambda handler with observability
  - Create lambda_function.py with lambda_handler() entry point
  - Log invocation start with timestamp and configuration parameters
  - Orchestrate: scan IAM users, write to DynamoDB, emit metrics
  - Calculate and track execution statistics (total users, records written, errors)
  - Log summary statistics on completion
  - Implement timeout detection by checking context.get_remaining_time_in_millis()
  - Log warning and exit gracefully when approaching timeout
  - Read DYNAMODB_TABLE_NAME from environment variable
  - _Requirements: 1.5, 2.5, 5.2, 5.3, 3.5_

- [x] 7. Implement concurrency control mechanism
  - Add concurrency lock using DynamoDB conditional write
  - Create lock item with execution_id and timestamp
  - Implement lock acquisition at start of lambda_handler
  - Implement lock release on completion or error
  - Set lock TTL to 10 minutes (2x Lambda timeout)
  - Exit immediately if lock acquisition fails
  - _Requirements: 3.3_

- [x] 8. Create Lambda deployment package
  - Create script to package Lambda function code and dependencies
  - Generate ZIP file with all Python modules and dependencies
  - Ensure proper file permissions and structure
  - _Requirements: 6.2_

- [x] 9. Implement Terraform DynamoDB table configuration
  - Create dynamodb.tf with DynamoDB table resource
  - Configure composite primary key (user_name as partition key, scan_timestamp as sort key)
  - Create global secondary index on scan_timestamp
  - Enable TTL on ttl attribute
  - Set billing mode to PAY_PER_REQUEST
  - Enable encryption at rest
  - _Requirements: 4.1, 4.3, 4.5, 6.2_

- [x] 10. Implement Terraform IAM roles and policies
  - Create iam.tf with Lambda execution role
  - Add trust policy for Lambda service
  - Attach AWSLambdaBasicExecutionRole managed policy
  - Create inline policy for IAM ListUsers and GetUser permissions
  - Create inline policy for DynamoDB PutItem and BatchWriteItem permissions
  - Create inline policy for CloudWatch PutMetricData permission
  - Follow least-privilege principle
  - _Requirements: 6.4_

- [x] 11. Implement Terraform Lambda function configuration
  - Create lambda.tf with Lambda function resource
  - Configure Python 3.11 runtime
  - Set handler to lambda_function.lambda_handler
  - Configure environment variables (DYNAMODB_TABLE_NAME, LOG_LEVEL)
  - Set timeout and memory from variables
  - Attach execution role
  - Configure CloudWatch Logs encryption
  - Set log retention period
  - _Requirements: 6.2_

- [x] 12. Implement Terraform EventBridge rule
  - Create eventbridge.tf with EventBridge rule resource
  - Configure schedule expression from variable
  - Set Lambda function as target
  - Add Lambda permission for EventBridge invocation
  - Enable the rule
  - _Requirements: 3.1, 6.2_

- [x] 13. Implement Terraform variables and outputs
  - Create variables.tf with input variables: monitoring_period, dynamodb_table_name, retention_days, lambda_timeout, lambda_memory, log_level
  - Set appropriate default values
  - Add variable descriptions and validation
  - Create outputs.tf with DynamoDB table name and Lambda function ARN outputs
  - _Requirements: 6.3, 6.5_

- [x] 14. Create Terraform main configuration
  - Create main.tf with provider configuration
  - Add required provider versions
  - Configure AWS provider
  - Add backend configuration for state management
  - _Requirements: 6.1, 6.2_

- [x] 15. Create documentation
  - Write README.md with deployment instructions
  - Document configuration variables and their purposes
  - Add architecture diagram
  - Include monitoring and alerting setup guide
  - Document troubleshooting steps
  - _Requirements: 6.1_
