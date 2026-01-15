# AWS-17 - Extracted Information

## Key Requirements

**Objective**: Implement AWS S3 bucket notification demo with Lambda trigger

**Core Functionality**:
- S3 bucket that accepts file uploads (any extension)
- Lambda function triggered on file upload
- Lambda function executes simple "hello world" logic

## Technical Components

**AWS Services Required**:
- Amazon S3 (bucket with event notifications)
- AWS Lambda (Python/Node.js function)
- IAM (roles and permissions)

**Event Flow**:
1. User uploads file to S3 bucket
2. S3 event notification triggers Lambda
3. Lambda executes hello world function

## Acceptance Criteria

- [ ] S3 bucket created and configured
- [ ] Lambda function created with hello world code
- [ ] S3 event notification configured to trigger Lambda
- [ ] Lambda has proper IAM permissions to be invoked by S3
- [ ] Test: Upload file to S3 triggers Lambda successfully
- [ ] Lambda execution logs visible in CloudWatch

## Dependencies

- AWS account with appropriate permissions
- IAM role for Lambda execution
- S3 bucket permissions for event notifications

## Scope

**In Scope**:
- S3 bucket creation
- Lambda function (hello world)
- Event notification configuration
- IAM roles and permissions

**Out of Scope**:
- File processing logic beyond hello world
- Multiple Lambda functions
- Complex event filtering
- Cross-region replication
