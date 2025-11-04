# Extracted Information: AWS-5

## Key Information for Requirements Generation

### Ticket Summary
- **Title**: AWS S3 Bucket trigger Lambda function
- **Type**: Task
- **Description**: I want to new S3 bucket. If I upload any file to the S3 bucket a demo 'hello world' lambda function should get triggered.

### Technical Scope
- **Primary Components**: 
  - S3 Bucket creation
  - Lambda function (Hello World demo)
  - S3 event trigger configuration
- **Integration**: S3 bucket event → Lambda function trigger
- **Trigger Event**: File upload to S3 bucket

### Acceptance Criteria (Inferred)
- S3 bucket must be created
- Lambda function must be deployed with "Hello World" functionality
- S3 bucket must trigger Lambda function on file upload
- Integration between S3 and Lambda must be functional

### Dependencies
- None explicitly mentioned in ticket

### Missing Information (Potential Questions)
- S3 bucket naming requirements
- Lambda function runtime/language preference
- Specific file types or all files should trigger
- AWS region preferences
- IAM permissions and security requirements
- Logging and monitoring requirements