# AWS-19 - Extracted Information

## Key Requirements

1. **S3 Bucket**: Create an S3 bucket to receive file uploads
2. **S3 Event Notification**: Configure S3 bucket to send notifications on object creation (any file extension)
3. **Lambda Function**: Create a simple "Hello World" Lambda function
4. **Event Trigger**: Lambda should be triggered automatically when files are uploaded to S3

## Technical Components

- **AWS S3**: Storage bucket with event notifications enabled
- **AWS Lambda**: Python/Node.js function for processing
- **IAM Roles**: Lambda execution role with S3 read permissions
- **Event Source Mapping**: S3 → Lambda trigger configuration

## Acceptance Criteria

1. S3 bucket created and configured
2. Lambda function deployed and operational
3. S3 event notification configured to trigger Lambda
4. Lambda successfully executes when file is uploaded to S3
5. Lambda logs "Hello World" message in CloudWatch

## Dependencies

- AWS Account with appropriate permissions
- IAM role for Lambda execution
- S3 bucket permissions for Lambda

## Scope

- **In Scope**: S3 bucket, Lambda function, event notification setup
- **Out of Scope**: Complex file processing, multiple Lambda functions, advanced error handling

---

*Extracted on: 2025-01-29*
