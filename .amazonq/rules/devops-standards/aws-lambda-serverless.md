# AWS Lambda and Serverless

## Purpose

Defines best practices for AWS Lambda functions and serverless architecture to ensure optimal performance, security, and maintainability.

## Instructions

- ALWAYS use Python for Lambda functions with proper type hints and documentation (ID: LAMBDA_PYTHON)
- ALWAYS implement proper error handling and logging in Lambda functions (ID: LAMBDA_ERROR_HANDLING)
- ALWAYS use Lambda layers for shared dependencies and utilities (ID: LAMBDA_LAYERS)
- ALWAYS implement proper cold start optimization and connection pooling (ID: COLD_START_OPTIMIZATION)
- ALWAYS use proper IAM roles with least privilege for Lambda functions (ID: LAMBDA_IAM_ROLES)
- ALWAYS implement proper environment variable management using AWS Systems Manager (ID: LAMBDA_ENV_VARS)
- ALWAYS use proper Lambda function sizing and memory allocation (ID: LAMBDA_SIZING)
- ALWAYS implement proper timeout configuration and retry logic (ID: LAMBDA_TIMEOUT_RETRY)
- ALWAYS use AWS X-Ray for Lambda function tracing and debugging (ID: LAMBDA_XRAY)
- ALWAYS implement proper Lambda function testing with unit and integration tests (ID: LAMBDA_TESTING)
- ALWAYS use proper Lambda function versioning and aliases (ID: LAMBDA_VERSIONING)
- ALWAYS implement proper Lambda function monitoring using CloudWatch (ID: LAMBDA_MONITORING)
- ALWAYS use proper Lambda function packaging and deployment strategies (ID: LAMBDA_PACKAGING)
- ALWAYS implement proper Lambda function security scanning and vulnerability assessment (ID: LAMBDA_SECURITY)
- ALWAYS use proper Lambda function concurrency and throttling configuration (ID: LAMBDA_CONCURRENCY)
- ALWAYS implement proper Lambda function dead letter queues for error handling (ID: LAMBDA_DLQ)
- ALWAYS use proper Lambda function environment-specific configurations (ID: LAMBDA_ENVIRONMENT_CONFIG)
- ALWAYS implement proper Lambda function performance optimization (ID: LAMBDA_PERFORMANCE)
- ALWAYS use proper Lambda function cost optimization strategies (ID: LAMBDA_COST_OPTIMIZATION)
- ALWAYS implement proper Lambda function backup and disaster recovery (ID: LAMBDA_BACKUP)
- ALWAYS use proper Lambda function networking and VPC configuration (ID: LAMBDA_NETWORKING)
- ALWAYS implement proper Lambda function compliance and audit logging (ID: LAMBDA_COMPLIANCE)
- ALWAYS use proper Lambda function deployment automation (ID: LAMBDA_DEPLOYMENT)
- ALWAYS implement proper Lambda function monitoring and alerting (ID: LAMBDA_ALERTING)
- ALWAYS use proper Lambda function security best practices (ID: LAMBDA_SECURITY_BEST_PRACTICES)

## Priority

High

## Error Handling

- If Python is not suitable, use Node.js or TypeScript with proper linting and type checking
- If Lambda layers are not feasible, implement alternative dependency management strategies
- If X-Ray tracing cannot be implemented, use alternative monitoring and debugging tools
- If Lambda function testing cannot be implemented, document the limitation and implement basic validation
- If Lambda function security scanning is not available, implement alternative security measures
